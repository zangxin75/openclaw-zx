# OpenClaw 多智能体团队架构设计方案

## 1. 架构概述

### 设计理念
- **隔离性**: 每个 Agent 运行在独立 Docker 容器，互不干扰
- **协作性**: 通过共享目录和消息总线实现通信
- **可扩展性**: 支持动态添加/移除 Agent
- **可观测性**: 统一日志收集和监控

### 核心组件
```
┌─────────────────────────────────────────────────────────────┐
│                    OpenClaw Multi-Agent Team                 │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│  │  PM Agent│  │ Dev Agent│  │ QA Agent │  │ Ops Agent│       │
│  │  (oc-pm) │  │ (oc-dev) │  │ (oc-qa)  │  │ (oc-ops) │       │
│  │  Docker  │  │  Docker  │  │  Docker  │  │  Docker  │       │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘       │
│       │            │            │            │              │
│       └────────────┴────────────┴────────────┘              │
│                      │                                      │
│              ┌───────┴───────┐                              │
│              │  Shared Workspace                              │
│              │  (/shared)     │                              │
│              └───────┬───────┘                              │
│                      │                                      │
│              ┌───────┴───────┐                              │
│              │  Message Bus   │                              │
│              │  (Redis/NATS)  │                              │
│              └───────────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 目录结构设计

### 根目录布局
```
/mnt/d/openclaw-home/
├── README.md                     # 项目说明
├── docker-compose.yml            # 编排配置
├── .env                          # 环境变量
├── config/                       # 全局配置
│   ├── nginx.conf               # 反向代理
│   ├── redis.conf               # 消息总线
│   └── shared/                  # 共享配置模板
│
├── agents/                       # 各 Agent 工作目录
│   ├── oc-pm/                   # 项目经理 Agent
│   ├── oc-dev/                  # 开发 Agent
│   ├── oc-qa/                   # 测试 Agent
│   ├── oc-ops/                  # 运维 Agent
│   └── oc-research/             # 研究 Agent (可选)
│
├── shared/                       # 共享工作空间
│   ├── projects/                # 项目文件
│   ├── knowledge/               # 知识库
│   ├── memory/                  # 共享记忆
│   └── logs/                    # 统一日志
│
├── infrastructure/               # 基础设施
│   ├── redis/                   # 消息总线数据
│   ├── postgres/                # 共享数据库 (可选)
│   └── monitoring/              # 监控配置
│
└── scripts/                      # 管理脚本
    ├── init.sh                  # 初始化
    ├── agent.sh                 # Agent 管理
    ├── backup.sh                # 备份
    └── status.sh                # 状态检查
```

### 单个 Agent 目录结构（以 oc-dev 为例）
```
agents/oc-dev/
├── docker-compose.yml           # Agent 专属编排
├── Dockerfile                   # 自定义镜像 (可选)
├── .env                         # Agent 环境变量
├── config/                      # Agent 配置
│   ├── openclaw/               # OpenClaw 配置
│   │   ├── config.json
│   │   └── skills/
│   ├── ai-profile/             # AI 人设
│   │   ├── SOUL.md
│   │   ├── IDENTITY.md
│   │   └── USER.md
│   └── workspace/              # 工作空间模板
│       ├── AGENTS.md
│       ├── TOOLS.md
│       └── MEMORY.md
│
├── workspace/                   # 实际工作目录 (挂载)
│   ├── memory/                 # 每日记忆
│   ├── skills/                 # 已安装技能
│   ├── projects/               # 项目文件
│   └── temp/                   # 临时文件
│
├── logs/                        # Agent 日志
└── data/                        # 持久化数据
```

---

## 3. Agent 角色定义

### Agent 1: oc-pm (项目经理)
```yaml
name: oc-pm
role: Project Manager
responsibilities:
  - 需求分析和拆解
  - 任务分配和调度
  - 进度跟踪和同步
  - 质量把控
skills:
  - 项目管理
  - 需求文档撰写
  - 任务分解
communication:
  - 接收用户指令
  - 分发给其他 Agent
  - 汇总结果汇报
```

### Agent 2: oc-dev (开发工程师)
```yaml
name: oc-dev
role: Developer
responsibilities:
  - 代码实现
  - 技术方案设计
  - Code Review
  - 技术文档编写
skills:
  - 多语言开发
  - 架构设计
  - 代码审查
communication:
  - 接收开发任务
  - 与 QA 协作修复 Bug
  - 向 PM 汇报进度
```

### Agent 3: oc-qa (测试工程师)
```yaml
name: oc-qa
role: Quality Assurance
responsibilities:
  - 测试用例设计
  - 自动化测试
  - Bug 报告和验证
  - 性能测试
skills:
  - 测试框架
  - 自动化测试
  - 性能分析
communication:
  - 接收测试任务
  - 向 Dev 反馈 Bug
  - 向 PM 报告质量状态
```

### Agent 4: oc-ops (运维工程师)
```yaml
name: oc-ops
role: DevOps
responsibilities:
  - 环境部署
  - CI/CD 配置
  - 监控告警
  - 故障排查
skills:
  - Docker/K8s
  - CI/CD 工具
  - 监控系统
communication:
  - 部署应用
  - 监控服务状态
  - 处理告警
```

### Agent 5: oc-research (研究员) - 可选
```yaml
name: oc-research
role: Researcher
responsibilities:
  - 技术调研
  - 方案评估
  - 新技术引入
skills:
  - 快速学习
  - 技术评估
  - 文档整理
```

---

## 4. 通信机制设计

### 4.1 通信方式

#### 方式 1: 共享文件系统 (主要)
```
/shared/memory/
├── inbox/                      # 收件箱
│   ├── oc-pm/                 # PM 的消息
│   ├── oc-dev/                # Dev 的消息
│   └── ...
├── tasks/                      # 任务队列
│   ├── pending/               # 待处理
│   ├── active/                # 进行中
│   └── completed/             # 已完成
└── status/                     # 状态同步
    ├── oc-pm.status
    ├── oc-dev.status
    └── ...
```

#### 方式 2: Redis 消息总线 (实时)
```
Channels:
  - agent:broadcast            # 广播消息
  - agent:pm:dev               # PM -> Dev 私聊
  - agent:dev:qa               # Dev -> QA 私聊
  - tasks:new                  # 新任务通知
  - tasks:completed            # 任务完成通知
```

#### 方式 3: OpenClaw Sessions (原生)
```bash
# 通过 OpenClaw 的 session 机制
openclaw sessions_send --session "oc-dev" "请完成用户登录功能"
```

### 4.2 消息格式
```json
{
  "message_id": "msg_20240320_001",
  "timestamp": "2024-03-20T14:30:00Z",
  "from": "oc-pm",
  "to": "oc-dev",
  "type": "task_assignment",
  "priority": "high",
  "content": {
    "task_id": "task_001",
    "title": "实现用户登录功能",
    "description": "...",
    "requirements": ["..."],
    "deadline": "2024-03-21T18:00:00Z",
    "attachments": ["/shared/projects/auth-module/spec.md"]
  },
  "reply_to": "msg_20240320_001"
}
```

---

## 5. 协作流程设计

### 典型工作流程

```
用户 -> PM Agent -> 任务拆解
                -> Dev Agent (并行开发)
                -> QA Agent (并行测试准备)
                -> Ops Agent (并行环境准备)
                
Dev 完成 -> QA 测试 -> 发现 Bug -> Dev 修复
         -> 测试通过 -> Ops 部署
         -> 全部完成 -> PM 汇报给用户
```

### 状态流转
```
[Created] -> [Assigned] -> [In Progress] -> [Review]
                                           -> [Testing]
                                           -> [Bug Fix]
                -> [Completed] -> [Deployed]
```

---

## 6. Docker 配置

### 基础镜像
```dockerfile
# Dockerfile.base
FROM node:20-slim

# 安装 OpenClaw
RUN npm install -g openclaw

# 安装常用工具
RUN apt-get update && apt-get install -y \
    git curl jq vim \
    python3 python3-pip \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# 创建 Agent 用户
RUN useradd -m -s /bin/bash agent
WORKDIR /home/agent
USER agent

# 默认配置
ENV OPENCLAW_STATE_DIR=/home/agent/.openclaw
ENV OPENCLAW_CONFIG_PATH=/home/agent/.openclaw/config.json
```

### Agent Docker Compose 模板
```yaml
# agents/oc-dev/docker-compose.yml
version: '3.8'

services:
  oc-dev:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: oc-dev
    hostname: oc-dev
    
    environment:
      - AGENT_NAME=oc-dev
      - AGENT_ROLE=developer
      - OPENCLAW_STATE_DIR=/home/agent/.openclaw
      - REDIS_URL=redis://redis:6379
    
    volumes:
      # 工作空间
      - ./workspace:/home/agent/workspace
      # 共享目录
      - ../shared:/shared:rw
      # 持久化数据
      - ./data:/home/agent/.openclaw
      # 配置
      - ./config:/home/agent/config:ro
    
    networks:
      - agent-network
    
    depends_on:
      - redis
    
    restart: unless-stopped
    
    # 资源限制
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '0.5'
          memory: 512M

networks:
  agent-network:
    external: true
```

### 根级 Docker Compose
```yaml
# /mnt/d/openclaw-home/docker-compose.yml
version: '3.8'

services:
  # 消息总线
  redis:
    image: redis:7-alpine
    container_name: oc-redis
    volumes:
      - ./infrastructure/redis:/data
    ports:
      - "6379:6379"
    networks:
      - agent-network
    restart: unless-stopped

  # 反向代理 (可选)
  nginx:
    image: nginx:alpine
    container_name: oc-nginx
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./shared:/usr/share/nginx/html/shared:ro
    ports:
      - "8080:80"
    networks:
      - agent-network
    restart: unless-stopped

  # 监控 (可选)
  prometheus:
    image: prom/prometheus
    container_name: oc-prometheus
    volumes:
      - ./infrastructure/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml:ro
    ports:
      - "9090:9090"
    networks:
      - agent-network
    restart: unless-stopped

networks:
  agent-network:
    driver: bridge
    name: agent-network

volumes:
  redis-data:
  shared-data:
```

---

## 7. 管理脚本

### 初始化脚本
```bash
#!/bin/bash
# scripts/init.sh

set -e

BASE_DIR="/mnt/d/openclaw-home"
AGENTS=("oc-pm" "oc-dev" "oc-qa" "oc-ops" "oc-research")

echo "🚀 Initializing OpenClaw Multi-Agent Team..."

# 创建目录结构
mkdir -p $BASE_DIR/{config,shared/{projects,knowledge,memory,logs},infrastructure/{redis,postgres,monitoring},scripts}

# 初始化每个 Agent
for agent in "${AGENTS[@]}"; do
    echo "Setting up $agent..."
    mkdir -p $BASE_DIR/agents/$agent/{workspace/{memory,skills,projects,temp},logs,data,config/openclaw}
    
    # 复制模板配置
    cp templates/agent-docker-compose.yml $BASE_DIR/agents/$agent/docker-compose.yml
    cp templates/agent-env $BASE_DIR/agents/$agent/.env
    
    # 创建 AI 人设文件
    cat > $BASE_DIR/agents/$agent/config/IDENTITY.md << EOF
# IDENTITY.md - $agent
name: $agent
role: ${agent/oc-/}
created_at: $(date -Iseconds)
EOF
done

# 启动基础设施
docker-compose up -d redis nginx

echo "✅ Initialization complete!"
echo "Start agents with: ./scripts/agent.sh start all"
```

### Agent 管理脚本
```bash
#!/bin/bash
# scripts/agent.sh

COMMAND=$1
TARGET=$2
BASE_DIR="/mnt/d/openclaw-home"
AGENTS=("oc-pm" "oc-dev" "oc-qa" "oc-ops")

case $COMMAND in
    start)
        if [ "$TARGET" == "all" ]; then
            for agent in "${AGENTS[@]}"; do
                echo "Starting $agent..."
                cd $BASE_DIR/agents/$agent && docker-compose up -d
            done
        else
            cd $BASE_DIR/agents/$TARGET && docker-compose up -d
        fi
        ;;
    stop)
        if [ "$TARGET" == "all" ]; then
            for agent in "${AGENTS[@]}"; do
                echo "Stopping $agent..."
                cd $BASE_DIR/agents/$agent && docker-compose down
            done
        else
            cd $BASE_DIR/agents/$TARGET && docker-compose down
        fi
        ;;
    status)
        docker ps --filter "name=oc-" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
        ;;
    logs)
        docker logs -f $TARGET
        ;;
    exec)
        docker exec -it $TARGET bash
        ;;
    *)
        echo "Usage: $0 {start|stop|status|logs|exec} {agent-name|all}"
        ;;
esac
```

---

## 8. 部署步骤

### Step 1: 环境准备
```bash
# 1. 确保 Docker 和 Docker Compose 已安装
docker --version
docker-compose --version

# 2. 创建工作目录
mkdir -p /mnt/d/openclaw-home
cd /mnt/d/openclaw-home

# 3. 克隆配置模板
git clone <repo-url> . || echo "使用本地模板"
```

### Step 2: 初始化
```bash
# 运行初始化脚本
chmod +x scripts/*.sh
./scripts/init.sh
```

### Step 3: 配置 Agent
```bash
# 编辑每个 Agent 的配置
vim agents/oc-pm/config/SOUL.md
vim agents/oc-dev/config/SOUL.md
# ... 其他 Agent
```

### Step 4: 启动基础设施
```bash
docker-compose up -d redis nginx
```

### Step 5: 启动 Agents
```bash
# 启动所有 Agent
./scripts/agent.sh start all

# 或者逐个启动
./scripts/agent.sh start oc-pm
./scripts/agent.sh start oc-dev
```

### Step 6: 验证
```bash
# 查看状态
./scripts/agent.sh status

# 测试通信
docker exec oc-pm redis-cli PING
```

---

## 9. 使用示例

### 示例 1: 分配开发任务
```bash
# 用户向 PM Agent 提交需求
docker exec -it oc-pm openclaw agent "需要开发一个用户认证模块"

# PM Agent 自动：
# 1. 分析需求
# 2. 创建任务文档到 /shared/tasks/task_001.md
# 3. 通知 Dev Agent
# 4. 等待结果
```

### 示例 2: Dev 完成任务
```bash
# Dev Agent 完成开发后
docker exec -it oc-dev openclaw agent "用户认证模块已完成，代码在 /shared/projects/auth/"

# 自动通知 QA 进行测试
```

### 示例 3: 查看协作状态
```bash
# 查看所有 Agent 状态
./scripts/status.sh

# 查看共享任务板
cat /shared/tasks/active/*.md
```

---

## 10. 扩展计划

### Phase 1: 基础版 (MVP)
- [x] 4 个核心 Agent (PM, Dev, QA, Ops)
- [x] 共享文件系统通信
- [x] 基础任务管理

### Phase 2: 增强版
- [ ] Web UI 管理面板
- [ ] 实时消息通知
- [ ] 知识图谱集成

### Phase 3: 高级版
- [ ] 自动任务分解
- [ ] 智能负载均衡
- [ ] A/B 测试框架

---

## 11. 附录

### 目录权限参考
```
/mnt/d/openclaw-home/
├── 755 root:root  config/
├── 777 root:root  shared/          # 所有 Agent 可读写
├── 755 root:root  agents/
│   └── 755 root:root  oc-*/
│       ├── 644 root:root  docker-compose.yml
│       ├── 600 root:root  .env
│       ├── 755 root:root  workspace/
│       └── 755 root:root  data/
```

### 环境变量参考
```bash
# .env 模板
AGENT_NAME=oc-dev
AGENT_ROLE=developer
OPENCLAW_MODEL=kimi-coding/k2p5
OPENCLAW_LOG_LEVEL=info
REDIS_URL=redis://redis:6379
SHARED_DIR=/shared
```

### 故障排查
```bash
# Agent 无法启动
docker logs oc-dev

# 网络不通
docker network inspect agent-network

# 权限问题
ls -la /mnt/d/openclaw-home/shared/
```

---

**文档版本**: v1.0  
**创建时间**: 2026-03-20  
**作者**: risen (oc-zx)  
**状态**: 设计方案待评审
