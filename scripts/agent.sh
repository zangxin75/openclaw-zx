#!/bin/bash
# OpenClaw Multi-Agent Team Manager
# Usage: ./agent.sh {init|start|stop|restart|status|logs|exec} [agent-name|all]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="/mnt/d/openclaw-home"
AGENTS=("oc-tdd-tester" "oc-tdd-coder" "oc-tdd-lead" "oc-architect" "oc-researcher" "oc-reviewer" "oc-security" "oc-ops" "oc-perf")

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 初始化环境
init_env() {
    log_info "Initializing OpenClaw Multi-Agent Team environment..."
    
    # 创建 Docker 网络
    if ! docker network ls | grep -q "agent-network"; then
        docker network create agent-network
        log_success "Created Docker network: agent-network"
    else
        log_warn "Docker network 'agent-network' already exists"
    fi
    
    # 启动基础设施
    cd "$BASE_DIR"
    docker-compose up -d redis
    log_success "Started infrastructure services"
    
    # 为每个 Agent 创建工作目录
    for agent in "${AGENTS[@]}"; do
        mkdir -p "$BASE_DIR/agents/$agent"/{workspace,data,logs}
        log_info "Created workspace for $agent"
    done
    
    log_success "Environment initialization complete!"
}

# 启动 Agent
start_agent() {
    local agent=$1
    
    if [ "$agent" == "all" ]; then
        log_info "Starting all agents..."
        for a in "${AGENTS[@]}"; do
            start_single_agent "$a"
        done
    else
        start_single_agent "$agent"
    fi
}

start_single_agent() {
    local agent=$1
    local agent_dir="$BASE_DIR/agents/$agent"
    
    if [ ! -d "$agent_dir" ]; then
        log_error "Agent '$agent' not found"
        return 1
    fi
    
    cd "$agent_dir"
    
    if docker ps --format "{{.Names}}" | grep -q "^${agent}$"; then
        log_warn "Agent '$agent' is already running"
        return 0
    fi
    
    log_info "Starting $agent..."
    docker-compose up -d
    log_success "$agent started successfully"
}

# 停止 Agent
stop_agent() {
    local agent=$1
    
    if [ "$agent" == "all" ]; then
        log_info "Stopping all agents..."
        for a in "${AGENTS[@]}"; do
            stop_single_agent "$a"
        done
        
        # 停止基础设施
        cd "$BASE_DIR"
        docker-compose down
        log_success "Infrastructure stopped"
    else
        stop_single_agent "$agent"
    fi
}

stop_single_agent() {
    local agent=$1
    local agent_dir="$BASE_DIR/agents/$agent"
    
    if [ ! -d "$agent_dir" ]; then
        log_error "Agent '$agent' not found"
        return 1
    fi
    
    cd "$agent_dir"
    
    if ! docker ps --format "{{.Names}}" | grep -q "^${agent}$"; then
        log_warn "Agent '$agent' is not running"
        return 0
    fi
    
    log_info "Stopping $agent..."
    docker-compose down
    log_success "$agent stopped successfully"
}

# 查看状态
status() {
    echo -e "\n${BLUE}=== OpenClaw Multi-Agent Team Status ===${NC}\n"
    
    # 基础设施状态
    echo -e "${YELLOW}Infrastructure:${NC}"
    docker ps --filter "name=oc-redis" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "  No infrastructure running"
    
    echo ""
    
    # Agent 状态
    echo -e "${YELLOW}Agents:${NC}"
    docker ps --filter "name=oc-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" 2>/dev/null || echo "  No agents running"
    
    echo ""
}

# 查看日志
logs() {
    local agent=$1
    
    if [ -z "$agent" ] || [ "$agent" == "all" ]; then
        log_error "Please specify an agent name for logs"
        echo "Usage: $0 logs {agent-name}"
        return 1
    fi
    
    docker logs -f "$agent" 2>&1 || log_error "Agent '$agent' not found or not running"
}

# 进入 Agent 容器
exec_agent() {
    local agent=$1
    
    if [ -z "$agent" ]; then
        log_error "Please specify an agent name"
        echo "Usage: $0 exec {agent-name}"
        return 1
    fi
    
    docker exec -it "$agent" bash 2>&1 || log_error "Agent '$agent' not found or not running"
}

# 重启 Agent
restart_agent() {
    local agent=$1
    
    if [ "$agent" == "all" ]; then
        stop_agent "all"
        start_agent "all"
    else
        stop_single_agent "$agent"
        start_single_agent "$agent"
    fi
}

# 主命令处理
case "${1:-}" in
    init)
        init_env
        ;;
    start)
        start_agent "${2:-all}"
        ;;
    stop)
        stop_agent "${2:-all}"
        ;;
    restart)
        restart_agent "${2:-all}"
        ;;
    status)
        status
        ;;
    logs)
        logs "${2:-}"
        ;;
    exec)
        exec_agent "${2:-}"
        ;;
    *)
        echo "OpenClaw Multi-Agent Team Manager"
        echo ""
        echo "Usage: $0 {command} [options]"
        echo ""
        echo "Commands:"
        echo "  init              Initialize environment"
        echo "  start [agent|all] Start agent(s)"
        echo "  stop [agent|all]  Stop agent(s)"
        echo "  restart [agent]   Restart agent(s)"
        echo "  status            Show status"
        echo "  logs {agent}      Show agent logs"
        echo "  exec {agent}      Enter agent container"
        echo ""
        echo "Agents:"
        for a in "${AGENTS[@]}"; do
            echo "  - $a"
        done
        echo ""
        echo "Examples:"
        echo "  $0 init                    # Initialize environment"
        echo "  $0 start all               # Start all agents"
        echo "  $0 start oc-tdd-tester     # Start specific agent"
        echo "  $0 status                  # Check status"
        echo "  $0 logs oc-tdd-tester      # View logs"
        exit 1
        ;;
esac
