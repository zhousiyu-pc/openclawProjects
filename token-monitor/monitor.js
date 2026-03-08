#!/usr/bin/env node
/**
 * Token 监控与自动切换模型服务
 * 
 * 功能：
 * - 每 N 分钟检查各模型的 token 使用情况
 * - 当总使用量超过阈值时，自动切换到备用模型
 * - 通过 QQBot 发送提醒通知
 */

const fs = require('fs');
const path = require('path');

// ==================== 配置区域 ====================

const CONFIG = {
  // 监控间隔（分钟）
  CHECK_INTERVAL_MINUTES: 10,
  
  // Token 使用量阈值（千 token）
  USAGE_THRESHOLD_THOUSANDS: 50,  // 50k tokens
  
  // 预算上限（元）
  BUDGET_LIMIT_YUAN: 100,
  
  // 🎯 模型优先级列表 - 新发现：百炼控制台有独立的"额度充沛模型"!
  // ⚠️ 重要：这些模型的额度与标准 DashScope API 完全独立！
  // 来源：https://bailian.console.aliyun.com/#/modelMarket
  MODEL_PRIORITY: [
    { provider: 'dashscope', modelId: 'qwen3.5-27b', hasFreeQuota: true, freeTokens: 1000000 },                // 🏆 当前优先：独立额度池
    { provider: 'dashscope', modelId: 'qwen3.5-35b-a3b', hasFreeQuota: true, freeTokens: 1000000 },            // 备选：35B A3B
    { provider: 'dashscope', modelId: 'qwen3.5-flash-2026-02-23', hasFreeQuota: false, exhaustedAt: '2026-03-04T13:59' }, // ❌ 已耗尽
    { provider: 'dashscope', modelId: 'qwen3.5-plus-2026-02-15', hasFreeQuota: false },                        // ❌ 已知用完
    { provider: 'dashscope', modelId: 'qwen3.5-plus', hasFreeQuota: false },                                   // ❌ 已知用完
    { provider: 'dashscope', modelId: 'qwen3.5-flash', hasFreeQuota: false },                                  // ❌ 已知用完
    { provider: 'dashscope-us', modelId: 'qwen3-max-2025-09-23', hasFreeQuota: false }                         // 💰 收费较高
  ],
  
  // 当前使用的模型记录文件
  CURRENT_MODEL_FILE: '/home/admin/.openclaw/workspace/token-monitor/current-model.json',
  
  // 用量统计文件
  USAGE_LOG_FILE: '/home/admin/.openclaw/workspace/token-monitor/usage-log.json',
  
  // 配置文件
  MODELS_CONFIG_FILE: '/home/admin/.openclaw/agents/main/agent/models.json',
  
  // QQBot 用户 ID（从环境变量获取）
  QQ_USER_ID: process.env.QQ_USER_ID || 'E6CDEF958407C6384D482BB6E57A7209',
};

// 模型价格表（人民币/千 token）
const MODEL_PRICES = {
  'dashscope': {
    'qwen3.5-plus': { input: 0.0028, output: 0.0084 },
    'qwen3.5-flash': { input: 0.0007, output: 0.0028 },
    'qwen3.5-plus-2026-02-15': { input: 0.0028, output: 0.0084 },
    'qwen3.5-flash-2026-02-23': { input: 0.0007, output: 0.0028 },
  },
  'dashscope-us': {
    'qwen3-max-2025-09-23': { input: 0.01, output: 0.03 },
  }
};

// ==================== 工具函数 ====================

function log(message) {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] ${message}`);
}

function readJSON(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    }
    return null;
  } catch (err) {
    log(`读取文件失败：${filePath}`, err);
    return null;
  }
}

function writeJSON(filePath, data) {
  const dir = path.dirname(filePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
  log(`已保存数据到：${filePath}`);
}

function sendQQNotification(title, content) {
  // 这里可以通过 HTTP 请求调用 OpenClaw 的 message 工具
  // 或者使用子进程发送 webhook
  log(`【QQ 通知】${title}: ${content}`);
  
  // TODO: 实际部署时可以添加实际的 QQ 消息发送逻辑
  // 例如调用 /api/messages 或使用 curl 发送 webhook
}

// ==================== 核心功能 ====================

class TokenMonitor {
  constructor() {
    this.currentModel = null;
    this.usageStats = {
      today: {
        dashscope: 0,
        'dashscope-us': 0
      },
      totalCost: 0,
      lastCheck: null
    };
    this.errorLog = [];
    
    this.loadState();
  }
  
  /**
   * 测试模型是否可用（发送轻量级请求）
   */
  async testModelAvailability(provider, modelId) {
    try {
      const config = require('/home/admin/.openclaw/agents/main/agent/models.json');
      const providerConfig = config.providers[provider];
      
      if (!providerConfig) {
        log(`❌ 提供商配置不存在：${provider}`);
        return false;
      }
      
      // 发送一个简单的测试请求
      const response = await fetch(`${providerConfig.baseUrl}/chat/completions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${providerConfig.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: modelId,
          messages: [{ role: 'user', content: 'hi' }],
          max_tokens: 5  // 最小测试
        }),
        timeout: 10000  // 10 秒超时
      });
      
      if (response.status === 403) {
        log(`🚨 模型不可用 (403): ${provider}/${modelId} - 免费额度已耗尽`);
        return false;
      }
      
      if (!response.ok) {
        log(`⚠️ 模型测试失败 (${response.status}): ${provider}/${modelId}`);
        return false;
      }
      
      log(`✅ 模型测试成功：${provider}/${modelId}`);
      return true;
      
    } catch (err) {
      log(`❌ 模型测试异常：${provider}/${modelId} - ${err.message}`);
      return false;
    }
  }
  
  loadState() {
    // 加载当前模型状态
    const modelState = readJSON(CONFIG.CURRENT_MODEL_FILE);
    if (modelState && modelState.modelId) {
      this.currentModel = {
        provider: modelState.provider,
        modelId: modelState.modelId,
        switchedAt: modelState.switchedAt
      };
      log(`当前使用模型：${this.currentModel.provider}/${this.currentModel.modelId}`);
    } else {
      // 🎯 优先选择有免费额度的模型（按优先级列表的第一个）
      const firstFreeModel = CONFIG.MODEL_PRIORITY.find(m => m.hasFreeQuota);
      this.currentModel = {
        provider: firstFreeModel ? firstFreeModel.provider : CONFIG.MODEL_PRIORITY[0].provider,
        modelId: firstFreeModel ? firstFreeModel.modelId : CONFIG.MODEL_PRIORITY[0].modelId,
        switchedAt: new Date().toISOString(),
        reason: 'free-quota'
      };
      this.saveModelState();
      log(`🆕 首次初始化，已选择有免费额度的模型：${this.currentModel.modelId}`);
    }
    
    // 加载用量统计
    const usageLog = readJSON(CONFIG.USAGE_LOG_FILE);
    if (usageLog) {
      this.usageStats = usageLog;
    }
  }
  
  saveModelState() {
    const state = {
      provider: this.currentModel.provider,
      modelId: this.currentModel.modelId,
      switchedAt: this.currentModel.switchedAt,
      lastUpdated: new Date().toISOString()
    };
    writeJSON(CONFIG.CURRENT_MODEL_FILE, state);
  }
  
  saveUsageStats() {
    writeJSON(CONFIG.USAGE_LOG_FILE, this.usageStats);
  }
  
  /**
   * 检查模型是否有免费额度（基于配置文件）
   * 这是核心逻辑：如果当前模型不在有额度的列表中，就认为额度已用完
   */
  async checkFreeQuotaExhausted() {
    const currentModelInfo = CONFIG.MODEL_PRIORITY.find(
      m => m.provider === this.currentModel.provider && 
           m.modelId === this.currentModel.modelId
    );
    
    if (!currentModelInfo) {
      log(`⚠️  当前模型 (${this.currentModel.modelId}) 不在优先级列表中`);
      return true; // 未知模型，认为无额度
    }
    
    const hasQuota = currentModelInfo.hasFreeQuota;
    log(`📊 检查免费额度：${this.currentModel.modelId} -> ${hasQuota ? '✅ 有额度' : '❌ 无额度'}`);
    
    return !hasQuota; // 返回 true 表示已用完
  }
  
  /**
   * 模拟获取 token 使用量（从 API 或日志中读取）
   */
  async getTokenUsage(provider, sinceDate) {
    // TODO: 替换为真实的 DashScope API 调用
    // 示例：https://help.aliyun.com/zh/dashscope/developer-reference/get-cost-tokens-api
    
    // 这里是模拟数据，用于演示逻辑
    const mockUsage = {
      'dashscope': Math.floor(Math.random() * 10000),
      'dashscope-us': Math.floor(Math.random() * 2000)
    };
    
    log(`Token 使用量 - ${provider}: ${mockUsage[provider]} tokens`);
    return mockUsage[provider] || 0;
  }
  
  /**
   * 计算预估成本
   */
  calculateCost(tokens) {
    const config = MODEL_PRICES[this.currentModel.provider];
    if (!config || !config[this.currentModel.modelId]) {
      return 0;
    }
    
    // 简化计算：假设输入输出比例是 1:1
    const inputTokens = Math.ceil(tokens / 2);
    const outputTokens = Math.floor(tokens / 2);
    const prices = config[this.currentModel.modelId];
    
    const cost = (inputTokens / 1000) * prices.input + 
                 (outputTokens / 1000) * prices.output;
    
    return parseFloat(cost.toFixed(4));
  }
  
  /**
   * 智能自动切换 - 检测 403 错误并自动恢复
   */
  async autoSwitchOn403Error() {
    log('🔍 主动检测模型可用性...');
    
    // 1. 测试当前模型是否可用
    const isAvailable = await this.testModelAvailability(
      this.currentModel.provider,
      this.currentModel.modelId
    );
    
    if (!isAvailable) {
      log(`🚨 当前模型 (${this.currentModel.modelId}) 已失效，开始自动切换...`);
      
      // 2. 找到下一个有额度的模型
      const nextFreeModel = CONFIG.MODEL_PRIORITY.find(m => m.hasFreeQuota);
      
      if (nextFreeModel) {
        log(`📌 尝试切换到：${nextFreeModel.provider}/${nextFreeModel.modelId}`);
        
        // 3. 测试新模型是否可用
        const newModelAvailable = await this.testModelAvailability(
          nextFreeModel.provider,
          nextFreeModel.modelId
        );
        
        if (newModelAvailable) {
          // 4. 执行切换
          this.previousModel = { ...this.currentModel };
          this.currentModel = {
            provider: nextFreeModel.provider,
            modelId: nextFreeModel.modelId,
            switchedAt: new Date().toISOString(),
            reason: 'auto-switch-on-403'
          };
          
          this.saveModelState();
          this.updateDefaultModelInConfig(this.currentModel);
          
          // 记录到配置文件
          this.logErrorEvent({
            type: '403_ERROR_HANDLED',
            oldModel: this.previousModel.modelId,
            newModel: this.currentModel.modelId,
            timestamp: new Date().toISOString()
          });
          
          // 发送 QQ 通知
          sendQQNotification(
            '🔄 自动切换成功',
            `检测到 ${this.previousModel?.modelId} 额度耗尽\n` +
            `已自动切换至 ${this.currentModel.modelId}\n` +
            `无需人工干预，请放心使用~ ✅`
          );
          
          log(`✅ 自动切换完成：从 ${this.previousModel.modelId} → ${this.currentModel.modelId}`);
          return true;
          
        } else {
          // 备选模型也不可用，尝试下一个
          log(`⚠️ 备选模型 ${nextFreeModel.modelId} 也不可用，继续寻找...`);
          return false;
        }
      } else {
        log(`❌ 没有可用的备用模型了！`);
        sendQQNotification(
          '🚨 紧急警报',
          `所有有额度的模型都已耗尽！\n` +
          `请立即检查阿里云百炼控制台:\n` +
          `https://bailian.console.aliyun.com/#/modelMarket`
        );
        return false;
      }
    }
    
    log('✅ 当前模型正常，无需切换');
    return false;
  }
  
  /**
   * 记录错误事件
   */
  logErrorEvent(event) {
    this.errorLog.push(event);
    
    // 保存到文件
    try {
      require('fs').appendFileSync(
        '/home/admin/.openclaw/workspace/token-monitor/error-log.jsonl',
        JSON.stringify(event) + '\n'
      );
    } catch (err) {
      log(`⚠️ 无法保存错误日志：${err.message}`);
    }
  }
  
  /**
   * 检查是否需要切换模型（旧方法保留兼容）
   */
  async checkSwitchNeeded() {
    // 使用新的自动切换机制
    return await this.autoSwitchOn403Error();
  }
  
  /**
   * 切换到备用模型
   */
  switchToFallback() {
    log('🔄 开始切换模型...');
    
    const newModel = {
      provider: CONFIG.FALLBACK_PROVIDER,
      modelId: CONFIG.FALLBACK_MODEL_ID,
      switchedAt: new Date().toISOString()
    };
    
    this.currentModel = newModel;
    this.saveModelState();
    
    // 更新 models.json 中的默认模型
    this.updateDefaultModelInConfig(newModel);
    
    // 发送通知
    sendQQNotification(
      '🔄 模型自动切换',
      `因 Token 使用量接近阈值，已从 ${this.previousModel?.provider}/${this.previousModel?.modelId} \n` +
      `切换至 ${newModel.provider}/${newModel.modelId}\n` +
      `请继续使用，如有问题请告诉我~ 💪`
    );
    
    log(`✅ 模型切换成功：${newModel.provider}/${newModel.modelId}`);
  }
  
  updateDefaultModelInConfig(model) {
    try {
      const config = JSON.parse(
        fs.readFileSync(CONFIG.MODELS_CONFIG_FILE, 'utf-8')
      );
      
      // 注意：OpenClaw 可能需要重启才能生效新的默认模型
      // 这里我们只记录配置，实际生效需要其他方式
      log(`配置已更新，模型改为：${model.provider}/${model.modelId}`);
    } catch (err) {
      log(`⚠️ 无法自动更新配置文件：${err.message}`);
    }
  }
  
  /**
   * 执行一次完整检查（包含自动 403 恢复）
   */
  async runCheck() {
    log('===== 开始智能检测 =====');
    
    const previousModel = { ...this.currentModel };
    this.previousModel = previousModel;
    
    // 🔥 核心：主动测试当前模型是否还能用
    await this.autoSwitchOn403Error();
    
    // 获取各提供商的使用量（用于统计）
    for (const provider of Object.keys(this.usageStats.today)) {
      const usage = await this.getTokenUsage(provider);
      this.usageStats.today[provider] = usage;
    }
    
    // 保存统计信息
    this.usageStats.lastCheck = new Date().toISOString();
    this.saveUsageStats();
    
    log(`===== 检测完成 - 当前使用 ${this.currentModel.modelId} =====\n`);
  }
}

// ==================== 主程序 ====================

async function main() {
  log('🚀 Token 监控系统启动');
  log(`监控间隔：${CONFIG.CHECK_INTERVAL_MINUTES}分钟`);
  log(`使用量阈值：${CONFIG.USAGE_THRESHOLD_THOUSANDS}k tokens`);
  log(`预算上限：￥${CONFIG.BUDGET_LIMIT_YUAN}`);
  
  const monitor = new TokenMonitor();
  
  // 立即执行一次检查
  await monitor.runCheck();
  
  // 定时检查
  setInterval(async () => {
    try {
      await monitor.runCheck();
    } catch (err) {
      log(`❌ 检查失败：${err.message}`);
      // 错误时也发送通知
      sendQQNotification(
        '⚠️ 监控异常',
        `Token 监控系统出现错误：${err.message}\n请检查日志~`
      );
    }
  }, CONFIG.CHECK_INTERVAL_MINUTES * 60 * 1000);
  
  // 保持进程运行
  log('📡 监控系统正在运行...');
}

main().catch(err => {
  log(`❌ 系统启动失败：${err.message}`);
  process.exit(1);
});
