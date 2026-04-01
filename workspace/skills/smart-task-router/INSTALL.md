# Smart Task Router - 快速搭建指南

## 功能概述

基于 oh-my-claudecode 架构启示实现的智能任务路由系统，为 OpenClaw 提供：

1. **关键词触发执行模式** - `并行:` `团队:` `深度:` `自动:`
2. **自动复杂度评估** - 智能判断任务难度
3. **多模式任务执行** - 直接/并行/团队/深度 四种模式
4. **结果验证循环** - 自动质量检查

---

## 快速搭建步骤

### 方式一：一键安装脚本（推荐）

```bash
# 1. 下载安装脚本
curl -fsSL https://raw.githubusercontent.com/your-repo/smart-task-router/main/install.sh | bash

# 2. 验证安装
python3 ~/.openclaw/workspace/skills/smart-task-router/main.py --test
```

### 方式二：手动安装

```bash
# 1. 进入 OpenClaw 工作目录
cd ~/.openclaw/workspace/skills/

# 2. 克隆或复制本技能目录
mkdir -p smart-task-router
cp -r /path/to/smart-task-router/* smart-task-router/

# 3. 验证安装
cd smart-task-router
python3 test_suite.py
```

### 方式三：Docker 安装

```bash
# 1. 构建镜像
docker build -t smart-task-router .

# 2. 运行测试
docker run --rm smart-task-router --test

# 3. 使用
docker run --rm smart-task-router "并行: 分析代码"
```

---

## OpenClaw 集成

### 步骤 1：创建集成脚本

在 `~/.openclaw/workspace/skills/smart-task-router/openclaw_integration.py` 创建集成：

```python
"""OpenClaw 集成入口"""
import sys
sys.path.insert(0, '/home/zx/.openclaw/workspace/skills/smart-task-router')

from router import route_task
from executor import TaskExecutor, ValidationEngine

def smart_route_and_execute(task: str, spawn_func=None):
    """
    智能路由并执行任务
    
    在 OpenClaw 中使用:
        result = smart_route_and_execute(
            "并行: 分析多个文件",
            spawn_func=lambda t: sessions_spawn(task=t, runtime="subagent")
        )
    """
    # 1. 路由任务
    routing = route_task(task)
    
    print(f"路由决策: {routing.mode.value}")
    print(f"复杂度: {routing.complexity.value}")
    print(f"子任务: {len(routing.subtasks)} 个")
    
    # 2. 执行
    executor = TaskExecutor(spawn_func=spawn_func)
    results = executor.execute(routing.subtasks, routing.config)
    
    # 3. 验证
    if routing.config.get("verify_result"):
        validator = ValidationEngine()
        validation = validator.validate(results, task)
        
        if validation["needs_fix"]:
            print("结果需要改进，建议重试")
    
    return {
        "routing": routing,
        "execution": executor.get_summary(),
        "validation": validation if routing.config.get("verify_result") else None
    }
```

### 步骤 2：修改 SKILL.md 添加使用说明

在 `~/.openclaw/workspace/skills/smart-task-router/SKILL.md` 中添加：

```markdown
## OpenClaw 使用方式

直接在对话中使用关键词前缀：

自动: 修复所有 TypeScript 错误
并行: 分析 src/app.py, src/utils.py, src/models.py
深度: 重构用户认证模块
团队: 设计一个新的API系统
```

### 步骤 3：添加到 OpenClaw 可用技能列表

在 `~/.openclaw/workspace/AGENTS.md` 或 `~/.openclaw/workspace/SOUL.md` 中添加：

```markdown
## 可用技能

- smart-task-router: 智能任务路由系统
  - 使用: `并行:`, `团队:`, `深度:`, `自动:` 前缀触发
  - 位置: `~/.openclaw/workspace/skills/smart-task-router/`
```

---

## 使用示例

### 示例 1：简单查询（直接模式）

```
查看 README.md 文件内容
```
→ 自动识别为低复杂度，直接执行

### 示例 2：多文件分析（并行模式）

```
并行: 分析 src/app.py, src/utils.py, src/models.py 的依赖关系
```
→ 启动3个子代理并行分析每个文件

### 示例 3：系统设计（团队模式）

```
团队: 设计一个完整的用户认证系统，包括登录、注册、权限管理
```
→ 完整管道：规划 → 执行 → 验证 → 修复

### 示例 4：深度重构（深度模式）

```
深度: 重构数据库访问层，优化查询性能，添加缓存策略
```
→ 深度分析 → 执行 → 验证

---

## 配置说明

编辑 `config.yaml` 自定义配置：

```yaml
# 模型映射
models:
  low: "kimi-coding/k2p5"      # 轻量模型
  medium: "kimi-coding/k2p5"   # 标准模型
  high: "kimi-coding/k2p5"     # 强力模型

# 执行配置
execution:
  max_retries: 2        # 最大重试次数
  max_workers: 3        # 并行模式最大工作线程
  timeout: 300          # 默认超时（秒）
  verify_results: true  # 是否验证结果
```

---

## 故障排除

### 问题：测试失败

```bash
# 运行详细测试
python3 test_suite.py -v

# 检查依赖
python3 -c "import complexity, router, executor"
```

### 问题：路由模式不符合预期

```bash
# 使用干运行模式查看路由决策
python3 main.py "你的任务" --dry-run
```

### 问题：复杂度评估不准确

编辑 `complexity.py` 调整信号权重：
- `HIGH_COMPLEXITY_SIGNALS` - 高复杂度关键词
- `MEDIUM_COMPLEXITY_SIGNALS` - 中复杂度关键词
- `WEIGHTS` - 各项评分权重

---

## 文件结构

```
smart-task-router/
├── SKILL.md              # 技能文档
├── README.md             # 项目说明
├── config.yaml           # 配置文件
├── main.py               # 主入口
├── complexity.py         # 复杂度评估模块
├── router.py             # 路由核心
├── executor.py           # 执行引擎
├── test_suite.py         # 测试套件
├── __init__.py           # 包初始化
└── INSTALL.md            # 本安装指南
```

---

## 更新日志

### v1.0.0 (2026-03-07)
- 初始版本发布
- 支持4种执行模式
- 25项功能测试全部通过
- OpenClaw 集成完成

---

## 参考

- 灵感来源: [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode)
- OpenClaw 文档: https://docs.openclaw.ai
