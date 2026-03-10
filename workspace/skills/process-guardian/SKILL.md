---
name: process-guardian
description: |
  守护 OpenClaw Gateway 进程，确保服务始终在线。自动检查进程状态，发现 Gateway 停止时自动重启。
---

# Process Guardian Skill

守护 OpenClaw Gateway 进程，确保服务始终在线

## 使用方法

### 启动守护
```bash
~/.openclaw/workspace/skills/process-guardian/guardian.sh start
```

### 停止守护
```bash
~/.openclaw/workspace/skills/process-guardian/guardian.sh stop
```

### 查看状态
```bash
~/.openclaw/workspace/skills/process-guardian/guardian.sh status
```

## 原理
- 使用 `pgrep` 检查 Gateway 进程
- 如果进程不存在，自动启动
- 每 10 秒检查一次
- 日志记录在 `/tmp/guardian.log`

## WSL 兼容性
在 WSL 环境下，使用 Python 实现更稳定的进程管理
