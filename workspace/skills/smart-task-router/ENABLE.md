# Smart Task Router - 启用指南

## 当前状态

✅ **核心模块已就绪** - 所有功能验证通过 (25项测试)  
⚠️ **需要手动激活** - 尚未设置为自动检测模式

## 使用方式

### 方式 1: 直接使用 (立即可用)

在当前 OpenClaw 会话中直接调用：

```python
# 导入并执行
import sys
sys.path.insert(0, '/home/zx/.openclaw/workspace/skills/smart-task-router')

from openclaw_integration import smart_execute

# 执行任务
result = smart_execute("并行: 分析代码")
```

### 方式 2: CLI 使用

```bash
cd ~/.openclaw/workspace/skills/smart-task-router
python3 main.py "并行: 分析文件"
```

### 方式 3: 交互式菜单

```bash
cd ~/.openclaw/workspace/skills/smart-task-router
./start.sh
```

## 启用自动检测

要让 STR 自动检测所有用户输入，需要将其集成到 OpenClaw 的消息处理流程中。

### 方法 A: 修改 SOUL.md (推荐)

在 `~/.openclaw/workspace/SOUL.md` 中添加：

```markdown
## 智能任务路由 (Smart Task Router)

我已经集成了 Smart Task Router，可以智能识别任务类型并选择最佳执行策略。

### 使用方法

用户可以直接在消息中使用以下前缀：

- `并行:` - 启动多代理并行处理 (如：分析多个文件)
- `团队:` - 启动完整规划→执行→验证→修复管道 (如：系统设计)
- `深度:` - 启动深度分析模式 (如：重构、架构优化)
- `自动:` - 让我自动判断最佳执行方式

### 示例

用户说：
> 并行: 分析 src/app.py, src/utils.py, src/models.py

我会：
1. 自动识别为"并行模式"
2. 启动多个子代理并行分析
3. 汇总结果给用户

用户说：
> 团队: 设计用户认证系统

我会：
1. 自动识别为"团队模式"
2. 执行规划→执行→验证→修复完整流程
3. 确保高质量交付

### 实现

相关代码位于：`~/.openclaw/workspace/skills/smart-task-router/`

使用方式：
```python
from smart_task_router.openclaw_integration import smart_execute
result = smart_execute(user_message)
```
```

### 方法 B: 创建 AGENTS.md 说明

在 `~/.openclaw/workspace/AGENTS.md` 中添加技能说明：

```markdown
## Smart Task Router 技能

位置：`~/.openclaw/workspace/skills/smart-task-router/`

使用方式：
1. 用户输入含 `并行:` / `团队:` / `深度:` 前缀时
2. 调用 `openclaw_integration.smart_execute()`
3. 系统会自动路由到合适的执行模式

测试命令：
```bash
cd ~/.openclaw/workspace/skills/smart-task-router
python3 test_suite.py  # 应显示 25项测试 OK
```
```

## 验证 STR 是否工作

### 测试 1: 模块导入

```python
import sys
sys.path.insert(0, '/home/zx/.openclaw/workspace/skills/smart-task-router')

from router import route_task
result = route_task("并行: 测试")
print(result.mode)  # 应显示 ExecutionMode.PARALLEL
```

### 测试 2: CLI 运行

```bash
cd ~/.openclaw/workspace/skills/smart-task-router
python3 main.py --test  # 运行 25项测试
```

### 测试 3: 集成测试

```bash
cd ~/.openclaw/workspace/skills/smart-task-router
python3 main.py "并行: 分析 README.md 和 SKILL.md" --dry-run
```

## 当前限制

目前 STR 作为**独立技能模块**运行，需要：

1. ✅ 手动调用 `smart_execute()` 函数
2. ✅ 或通过 CLI `python3 main.py "任务"`
3. ❌ 尚未集成到 OpenClaw 的自动消息处理流程中

要完全自动化（自动检测每条消息），需要 OpenClaw Gateway 层面的 hook 支持。

## 下一步

1. **立即可用**: 使用方式 1/2/3 直接调用
2. **半自动**: 在 SOUL.md 中添加说明，识别到关键词时手动调用
3. **全自动**: 等待 OpenClaw Gateway 支持消息预处理 hook

## 文件位置

```
~/.openclaw/workspace/skills/smart-task-router/
├── main.py                    # CLI 入口
├── openclaw_integration.py    # OpenClaw 集成 API
├── router.py                  # 路由核心
├── complexity.py              # 复杂度评估
├── executor.py                # 执行引擎
├── test_suite.py              # 测试套件
├── start.sh                   # 启动脚本
├── SKILL.md                   # 技能文档
├── INSTALL.md                 # 安装指南
├── ASSET.md                   # 资产清单
└── ENABLE.md                  # 本文件
```

## 快速测试

在当前会话中测试 STR：
