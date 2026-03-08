#!/bin/bash
# OpenClaw 配置恢复脚本
# 系统升级/重装后运行此脚本恢复所有配置

set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
WORKSPACE_DIR="/home/admin/.openclaw/workspace"
DATA_DIR="/data/openclaw"
CONFIG_DIR=~/.openclaw

echo "🦞 OpenClaw 配置恢复脚本"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}✓${NC} $1"; }
log_warn() { echo -e "${YELLOW}⚠${NC} $1"; }
log_error() { echo -e "${RED}✗${NC} $1"; }

# 恢复模型配置
restore_model_config() {
    echo ""
    echo "🧠 恢复模型配置..."
    
    mkdir -p "${CONFIG_DIR}"
    
    if [ -f "${DATA_DIR}/models.json" ]; then
        cp "${DATA_DIR}/models.json" "${CONFIG_DIR}/models.json"
        log_info "恢复 models.json"
    else
        cat > "${CONFIG_DIR}/models.json" << 'EOF'
{
  "default_model": "dashscope/qwen3.5-plus-2026-02-15"
}
EOF
        log_info "创建默认 models.json"
    fi
    
    if [ -f "${DATA_DIR}/model_state.json" ]; then
        cp "${DATA_DIR}/model_state.json" "${CONFIG_DIR}/model_state.json"
        log_info "恢复 model_state.json"
    fi
}

# 恢复 cron 任务
restore_cron_jobs() {
    echo ""
    echo "⏰ 恢复 Cron 任务..."
    
    local existing_cron=$(crontab -l 2>/dev/null || echo "")
    local backup_job="0 3 * * * ${WORKSPACE_DIR}/scripts/backup_workspace.sh >> /var/log/openclaw-backup.log 2>&1"
    local monitor_job="0 */6 * * * ${WORKSPACE_DIR}/scripts/token_monitor.sh >> /var/log/openclaw-token-monitor.log 2>&1"
    
    local has_backup=false
    local has_monitor=false
    
    echo "${existing_cron}" | grep -q "backup_workspace.sh" && has_backup=true
    echo "${existing_cron}" | grep -q "token_monitor.sh" && has_monitor=true
    
    if [ "${has_backup}" = true ]; then
        log_info "备份任务已存在"
    fi
    
    if [ "${has_monitor}" = true ]; then
        log_info "监控任务已存在"
    fi
    
    if [ "${has_backup}" = false ] || [ "${has_monitor}" = false ]; then
        local new_cron="${existing_cron}"
        
        if [ "${has_backup}" = false ]; then
            new_cron="${new_cron}"$'\n'"${backup_job}"
            log_info "添加备份任务"
        fi
        
        if [ "${has_monitor}" = false ]; then
            new_cron="${new_cron}"$'\n'"${monitor_job}"
            log_info "添加监控任务"
        fi
        
        echo "${new_cron}" | crontab -
        log_info "Cron 任务更新完成"
    fi
}

# 设置脚本权限
set_script_permissions() {
    echo ""
    echo "🔐 设置脚本权限..."
    
    if [ -d "${WORKSPACE_DIR}/scripts" ]; then
        chmod +x "${WORKSPACE_DIR}/scripts"/*.sh 2>/dev/null || true
        log_info "脚本权限设置完成"
    else
        log_warn "脚本目录不存在"
    fi
}

# 创建日志文件
setup_log_files() {
    echo ""
    echo "📝 创建日志文件..."
    
    local log_files=(
        "/var/log/openclaw-backup.log"
        "/var/log/openclaw-token-monitor.log"
        "/var/log/openclaw-model-switch.log"
    )
    
    for log_file in "${log_files[@]}"; do
        if [ ! -f "${log_file}" ]; then
            touch "${log_file}" 2>/dev/null || sudo touch "${log_file}" 2>/dev/null || true
            chmod 666 "${log_file}" 2>/dev/null || sudo chmod 666 "${log_file}" 2>/dev/null || true
            log_info "创建日志：${log_file}"
        fi
    done
}

# 备份配置到独立数据区
backup_config_to_data() {
    echo ""
    echo "💾 备份配置到独立数据区..."
    
    mkdir -p "${DATA_DIR}"
    
    if [ -f "${CONFIG_DIR}/models.json" ]; then
        cp "${CONFIG_DIR}/models.json" "${DATA_DIR}/models.json"
        log_info "备份 models.json"
    fi
    
    if [ -f "${CONFIG_DIR}/model_state.json" ]; then
        cp "${CONFIG_DIR}/model_state.json" "${DATA_DIR}/model_state.json"
        log_info "备份 model_state.json"
    fi
}

# 验证恢复
verify_restoration() {
    echo ""
    echo "🔍 验证恢复结果..."
    echo ""
    
    local errors=0
    
    if [ -d "${WORKSPACE_DIR}/scripts" ]; then
        log_info "Workspace 目录正常"
    else
        log_error "Workspace 目录缺失"
        ((errors++)) || true
    fi
    
    if [ -f "${CONFIG_DIR}/models.json" ]; then
        local model=$(cat "${CONFIG_DIR}/models.json" | grep -oP '"default_model":\s*"\K[^"]+' || echo "未知")
        log_info "模型配置：${model}"
    else
        log_error "模型配置缺失"
        ((errors++)) || true
    fi
    
    if crontab -l 2>/dev/null | grep -q "openclaw"; then
        log_info "Cron 任务已配置"
    else
        log_warn "Cron 任务未配置"
    fi
    
    if [ -x "${WORKSPACE_DIR}/scripts/backup_workspace.sh" ]; then
        log_info "脚本权限正常"
    else
        log_warn "脚本权限可能有问题"
    fi
    
    echo ""
    if [ ${errors} -eq 0 ]; then
        log_info "✅ 所有检查通过！配置恢复完成"
    else
        log_error "发现 ${errors} 个问题，请手动检查"
    fi
}

# 显示使用指南
show_guide() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📚 快速参考"
    echo ""
    echo "查看状态:"
    echo "  openclaw status"
    echo "  ${WORKSPACE_DIR}/scripts/token_monitor.sh"
    echo ""
    echo "手动切换模型:"
    echo "  ${WORKSPACE_DIR}/scripts/auto_switch_model.sh switch"
    echo ""
    echo "查看日志:"
    echo "  tail -f /var/log/openclaw-token-monitor.log"
    echo ""
    echo "文档:"
    echo "  ${WORKSPACE_DIR}/scripts/MODEL_MANAGEMENT.md"
    echo ""
}

# 主流程
main() {
    echo "开始时间：$(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    restore_model_config
    restore_cron_jobs
    set_script_permissions
    setup_log_files
    backup_config_to_data
    verify_restoration
    show_guide
    
    echo "完成时间：$(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    log_info "🎉 配置恢复完成！"
}

main "$@"
