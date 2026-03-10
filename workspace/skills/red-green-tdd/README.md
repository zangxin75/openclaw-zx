# Red/Green TDD Skill

AI 编程时代的代码质量保障方法论

## 快速开始

```python
from red_green_tdd import check_and_remind

# 检测用户输入
should_remind, message = check_and_remind("帮我写一个登录函数")
if should_remind:
    print(message)  # 输出 TDD 提醒
```

## 文件结构

```
red-green-tdd/
├── SKILL.md          # 技能文档
├── assistant.py      # TDD 助手核心
└── __init__.py       # 包初始化
```

## 使用方式

### 在 OpenClaw 中自动提醒

当用户发送编程任务时，自动提醒使用 Red/Green TDD：

```python
from red_green_tdd.assistant import check_and_remind

def on_user_message(message):
    should_remind, reminder = check_and_remind(message)
    if should_remind:
        # 在回复中加入 TDD 提醒
        return reminder + "\n\n" + process_message(message)
```

### 生成测试模板

```python
from red_green_tdd.assistant import get_tdd_assistant

assistant = get_tdd_assistant()
template = assistant.generate_test_template(
    description="用户登录功能",
    language="python"
)
print(template)
```

## 核心理念

1. **🔴 Red** - 先写测试，定义需求
2. **🟡 Verify** - 运行测试，确认失败
3. **🟢 Green** - 实现功能，测试通过

## 提醒触发条件

- 新功能开发 → 建议完整 TDD 流程
- Bug 修复 → 建议先写复现测试
- 代码重构 → 强调测试保护
- 代码修改 → 建议先跑现有测试

## 参考

- 作者：Simon Willison (Django 创始人)
- 理念：Egoistic Engineering Patterns
