# OpenClaw 多智能体团队 (TDD-OMC 版)

基于 TDD + Oh-my-Claudecode + OpenClaw 整合的多智能体协作开发团队。

## 架构设计

查看完整设计文档:
- [基础架构](DESIGN.md)
- [TDD 版本](DESIGN-TDD.md)  
- [整合版本](DESIGN-TDD-OMC.md) ⭐

## 8 个智能体角色

### 核心 TDD Trio (始终运行)
1. **oc-tdd-tester** - RED 阶段: 编写失败的测试
2. **oc-tdd-coder** - GREEN/REFACTOR 阶段: 实现和重构
3. **oc-tdd-lead** - 技术负责人: 协调和质量把控

### 按需激活专家
4. **oc-architect** - 架构师: 系统架构设计
5. **oc-researcher** - 研究员: 技术调研
6. **oc-reviewer** - 代码审查员: 代码质量
7. **oc-security** - 安全专家: 安全审计
8. **oc-ops** - 运维工程师: CI/CD 和部署
9. **oc-perf** - 性能专家: 性能优化

## 快速开始

### 1. 初始化环境
```bash
cd /mnt/d/openclaw-home
./scripts/agent.sh init
```

### 2. 启动智能体
```bash
# 启动所有智能体
./scripts/agent.sh start all

# 或只启动核心 Trio
./scripts/agent.sh start oc-tdd-tester
./scripts/agent.sh start oc-tdd-coder
./scripts/agent.sh start oc-tdd-lead
```

### 3. 查看状态
```bash
./scripts/agent.sh status
```

### 4. 查看日志
```bash
./scripts/agent.sh logs oc-tdd-tester
```

## 目录结构

```
/mnt/d/openclaw-home/
├── agents/              # 8 个智能体配置
│   ├── oc-tdd-tester/
│   ├── oc-tdd-coder/
│   ├── oc-tdd-lead/
│   └── ...
├── shared/              # 共享工作空间
│   ├── projects/        # 项目代码
│   ├── tasks/           # 任务队列
│   └── omc-assets/      # 能力资产
├── scripts/             # 管理脚本
│   └── agent.sh         # 智能体管理
├── docker-compose.yml   # 基础设施编排
└── README.md           # 本文件
```

## 使用方式

### 方式 1: 通过共享文件系统
智能体通过 `/shared` 目录协作:
- `/shared/tasks/BACKLOG/` - 待办任务
- `/shared/tasks/RED/` - 测试中
- `/shared/tasks/GREEN/` - 实现中
- `/shared/projects/` - 项目代码

### 方式 2: 通过 Redis 消息总线
```bash
# 发送消息给智能体
redis-cli PUBLISH agent:oc-tdd-tester "新任务来了"
```

### 方式 3: 直接操作容器
```bash
# 进入智能体容器
./scripts/agent.sh exec oc-tdd-tester

# 在容器内执行命令
docker exec oc-tdd-tester node --version
```

## TDD 工作流程

1. **PM** 在 `/shared/tasks/BACKLOG/` 创建任务
2. **oc-tdd-tester** 接收任务，进入 RED 阶段，编写测试
3. **oc-tdd-coder** 接收测试，进入 GREEN 阶段，实现功能
4. **oc-tdd-lead** 协调审查和验证
5. **oc-tdd-coder** 进入 REFACTOR 阶段，优化代码
6. 任务完成，移动到 `/shared/tasks/DONE/`

## 监控和维护

### 查看所有智能体状态
```bash
./scripts/agent.sh status
```

### 重启智能体
```bash
./scripts/agent.sh restart oc-tdd-tester
```

### 停止所有智能体
```bash
./scripts/agent.sh stop all
```

## 扩展指南

### 添加新的专家智能体

1. 复制模板:
```bash
cp -r agents/oc-researcher agents/oc-new-expert
```

2. 修改配置:
   - 更新 `config/SOUL.md`
   - 更新 `config/IDENTITY.md`
   - 更新 `docker-compose.yml`

3. 添加到 agent.sh:
   - 在 `AGENTS` 数组中添加新智能体

4. 启动:
```bash
./scripts/agent.sh start oc-new-expert
```

## 设计理念

> "Don't learn TDD. Don't learn OpenClaw. Just describe what you want.
> The TDD-OMC team handles everything."

核心理念:
- **测试先行**: 每个功能都经过 Red-Green-Refactor
- **专业分工**: 按需激活最适合的专家
- **协作优先**: 智能体通过共享空间和消息总线协作
- **资产复用**: 积累的模式和模板可复用

## 问题排查

### 智能体无法启动
```bash
# 检查 Docker 网络
docker network ls | grep agent-network

# 检查日志
docker logs oc-tdd-tester
```

### Redis 连接失败
```bash
# 检查 Redis 状态
docker ps | grep redis

# 测试连接
redis-cli -h localhost -p 6379 ping
```

### 共享目录权限问题
```bash
# 修复权限
chmod -R 755 /mnt/d/openclaw-home/shared
```

## 版本历史

- **v1.0** (2026-03-20) - 初始版本，8 个智能体

## 贡献

欢迎提交 PR 扩展新的专家智能体或改进工作流程!

---
**Created**: 2026-03-20  
**Author**: risen (oc-zx)  
**License**: MIT
