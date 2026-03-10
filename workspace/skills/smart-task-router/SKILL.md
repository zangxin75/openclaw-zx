# Smart Task Router (STR)

智能任务路由系统 - 基于 oh-my-claudecode 架构启示实现

## 功能特性

- **关键词触发**: 检测 `并行:` `团队:` `深度:` `自动:` 前缀
- **复杂度评估**: 自动判断任务难度选择模型层级
- **多模式执行**: 直接执行 / 并行代理 / 深度规划+验证
- **验证循环**: 结果质量检查，不合格自动修复

## 使用方法

在消息中使用以下前缀：

```
并行: 分析这3个文件的内容差异
团队: 帮我设计一个用户认证系统
深度: 重构这个项目的API架构
自动: 修复所有TypeScript错误
```

## 安装

1. 复制本 skill 目录到目标 OpenClaw 的 `~/.openclaw/workspace/skills/`
2. 确保依赖已安装: `pip install pyyaml`
3. 开始使用

## 执行模式详解

### Auto Mode (自动:)
自动评估任务复杂度：
- 简单任务 → 直接执行
- 中等任务 → 单代理执行
- 复杂任务 → 走完整 Team Mode

### Parallel Mode (并行:)
启动多个子代理并行处理：
- 自动分解任务为多个子任务
- 并行执行
- 结果汇总

### Team Mode (团队:)
完整分阶段管道：
```
规划(plan) → 执行(exec) → 验证(verify) → 修复(fix)
```

### Deep Mode (深度:)
深度分析+执行：
```
分析(analysis) → 执行(exec) → 验证(verify)
```

## 模型分层

| 复杂度 | 模型配置 | 适用场景 |
|--------|----------|----------|
| 低 | kimi-coding/k2p5-fast | 简单查询、文件查找 |
| 中 | kimi-coding/k2p5 | 常规编码、文档撰写 |
| 高 | kimi-coding/k2p5-deep | 架构设计、复杂重构 |

## 文件说明

- `router.py` - 核心路由逻辑
- `executor.py` - 执行引擎
- `validator.py` - 验证模块
- `complexity.py` - 复杂度评估
- `test_suite.py` - 功能测试套件

## 配置

在 `~/.openclaw/workspace/skills/smart-task-router/config.yaml` 中可配置：
- 默认执行模式
- 模型映射
- 验证阈值
- 重试次数
