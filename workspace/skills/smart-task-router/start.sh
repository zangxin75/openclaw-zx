#!/bin/bash
#
# Smart Task Router - 快速启动脚本
# Usage: ./start.sh [task]
#

set -e

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SKILL_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           Smart Task Router v1.0.0                           ║"
echo "║     基于 oh-my-claudecode 架构启示实现                        ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 Python3${NC}"
    exit 1
fi

# 功能选择
if [ $# -eq 0 ]; then
    echo ""
    echo "请选择操作:"
    echo "  1) 运行测试"
    echo "  2) 功能演示"
    echo "  3) 交互模式"
    echo "  4) 查看文档"
    echo "  q) 退出"
    echo ""
    read -p "输入选项 (1-4/q): " choice
    
    case $choice in
        1)
            echo -e "\n${YELLOW}运行功能测试...${NC}"
            python3 test_suite.py
            ;;
        2)
            echo -e "\n${YELLOW}运行功能演示...${NC}"
            python3 main.py --demo
            ;;
        3)
            echo -e "\n${YELLOW}进入交互模式...${NC}"
            echo "提示: 使用 并行:/团队:/深度: 前缀触发不同模式"
            echo "输入 'quit' 退出"
            echo ""
            while true; do
                read -p "任务> " task
                if [ "$task" = "quit" ]; then
                    break
                fi
                if [ -n "$task" ]; then
                    python3 main.py "$task"
                    echo ""
                fi
            done
            ;;
        4)
            echo -e "\n${YELLOW}文档列表:${NC}"
            echo "  - SKILL.md: 技能文档"
            echo "  - INSTALL.md: 安装指南"
            echo "  - ASSET.md: 资产清单"
            echo "  - README.md: 项目说明"
            ;;
        q|Q)
            echo "再见!"
            exit 0
            ;;
        *)
            echo -e "${RED}无效选项${NC}"
            exit 1
            ;;
    esac
else
    # 直接执行任务
    python3 main.py "$@"
fi

echo ""
echo -e "${GREEN}完成!${NC}"
