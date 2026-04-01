#!/bin/bash
# Quick Start Guide for OpenClaw Multi-Agent Team

echo "🚀 OpenClaw 多智能体团队 - 快速启动"
echo "=================================="
echo ""

# 检查 Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

echo "✅ Docker 环境检查通过"
echo ""

# 初始化
echo "步骤 1/4: 初始化环境..."
./scripts/agent.sh init

echo ""
echo "步骤 2/4: 启动核心 TDD Trio..."
./scripts/agent.sh start oc-tdd-tester
./scripts/agent.sh start oc-tdd-coder
./scripts/agent.sh start oc-tdd-lead

echo ""
echo "步骤 3/4: 启动按需专家..."
./scripts/agent.sh start oc-architect
./scripts/agent.sh start oc-reviewer
./scripts/agent.sh start oc-ops

echo ""
echo "步骤 4/4: 验证状态..."
sleep 3
./scripts/agent.sh status

echo ""
echo "=================================="
echo "✅ 多智能体团队启动完成!"
echo ""
echo "核心智能体 (已启动):"
echo "  - oc-tdd-tester (RED 阶段)"
echo "  - oc-tdd-coder (GREEN/REFACTOR)"
echo "  - oc-tdd-lead (技术负责人)"
echo ""
echo "按需专家 (已启动):"
echo "  - oc-architect (架构师)"
echo "  - oc-reviewer (代码审查)"
echo "  - oc-ops (运维)"
echo ""
echo "待命专家 (可随时启动):"
echo "  - oc-researcher (研究员)"
echo "  - oc-security (安全专家)"
echo "  - oc-perf (性能专家)"
echo ""
echo "常用命令:"
echo "  ./scripts/agent.sh status          # 查看状态"
echo "  ./scripts/agent.sh logs oc-tdd-tester  # 查看日志"
echo "  ./scripts/agent.sh stop all        # 停止所有"
echo ""
echo "开始你的第一个 TDD 循环:"
echo "  1. 在 /shared/tasks/BACKLOG/ 创建任务"
echo "  2. oc-tdd-tester 会自动进入 RED 阶段"
echo "  3. 观察智能体协作完成开发"
echo ""
