"""
Red/Green TDD 助手 - 编程任务检测与提醒

在 OpenClaw 会话中自动检测编程任务并提醒使用 TDD
"""

import re
from typing import Dict, List, Tuple

class TDDAssistant:
    """TDD 助手 - 检测编程任务并提供提醒"""
    
    # 编程任务关键词
    CODING_KEYWORDS = [
        # 开发
        r"(写|编写|开发|实现|create|write|implement|develop)",
        r"(功能|函数|模块|类|接口|feature|function|module|class)",
        r"(代码|code|编程|programming)",
        # 修改
        r"(修改|更新|重构|修复|modify|update|refactor|fix)",
        r"(bug|错误|问题|error|issue)",
        # 添加
        r"(添加|新增|增加|add|new)",
        r"(api|接口|endpoint|route)",
    ]
    
    # 文件扩展名提示
    CODE_EXTENSIONS = [
        r"\.py\b",
        r"\.js\b", r"\.ts\b",
        r"\.java\b",
        r"\.go\b",
        r"\.rs\b",
        r"\.cpp\b", r"\.c\b",
    ]
    
    def __init__(self):
        self.reminder_count = 0
        self.accepted_count = 0
    
    def is_coding_task(self, text: str) -> Tuple[bool, List[str], float]:
        """
        检测是否为编程任务
        
        Returns:
            (is_coding, reasons, confidence)
        """
        reasons = []
        confidence = 0.0
        
        # 1. 检测编程关键词
        coding_matches = 0
        for pattern in self.CODING_KEYWORDS:
            if re.search(pattern, text, re.IGNORECASE):
                coding_matches += 1
        
        if coding_matches >= 2:
            confidence += 0.4
            reasons.append(f"检测到{coding_matches}个编程相关关键词")
        elif coding_matches >= 1:
            confidence += 0.2
            reasons.append("检测到编程相关关键词")
        
        # 2. 检测代码文件引用
        file_matches = 0
        for pattern in self.CODE_EXTENSIONS:
            if re.search(pattern, text, re.IGNORECASE):
                file_matches += 1
        
        if file_matches > 0:
            confidence += 0.3
            reasons.append(f"检测到{file_matches}个代码文件引用")
        
        # 3. 检测技术术语
        tech_terms = [
            r"\b(api|rest|http|json|xml)\b",
            r"\b(database|db|sql|nosql)\b",
            r"\b(frontend|backend|server|client)\b",
            r"\b(test|testing|pytest|unittest|jest)\b",
            r"\b(git|github|commit|pr|merge)\b",
        ]
        
        tech_matches = 0
        for pattern in tech_terms:
            if re.search(pattern, text, re.IGNORECASE):
                tech_matches += 1
        
        if tech_matches >= 2:
            confidence += 0.2
            reasons.append("检测到技术术语")
        
        # 4. 任务长度（编程任务通常有一定长度）
        if 20 < len(text) < 500:
            confidence += 0.1
        
        # 判断是否编程任务
        is_coding = confidence >= 0.5
        
        return is_coding, reasons, confidence
    
    def get_reminder(self, task_type: str = "new_feature") -> str:
        """
        获取 TDD 提醒消息
        
        Args:
            task_type: new_feature | bug_fix | refactor | modify
        """
        reminders = {
            "new_feature": """💡 **建议采用 Red/Green TDD 保障代码质量**

作为你的编程助手，我建议按以下步骤进行：

**Step 1: 🔴 先写测试**
- 先让我为你的功能写测试用例
- 明确输入输出、边界条件、异常处理

**Step 2: 🟡 确认红灯**
- 运行测试，确保测试失败（证明测试有效）

**Step 3: 🟢 实现功能**
- 编写功能代码，直到测试通过
- 不通过就重写，直到绿灯

**要我帮你开始写测试用例吗？** 回复"开始TDD"或"先写测试""",

            "bug_fix": """🐛 **Bug 修复建议采用 TDD**

**Red/Green 流程：**
1. **先写复现测试** - 写一个测试用例复现这个 bug
2. **确认红灯** - 运行测试，确认失败（复现成功）
3. **修复代码** - 修改代码让测试通过
4. **验证绿灯** - 确认修复成功且没破坏其他功能

这样确保：
- Bug 被准确复现和修复
- 不会引入新的问题
- 有回归测试防止再次发生

**要我帮你写复现测试吗？**""",

            "refactor": """🔧 **重构必须使用 TDD 保护**

重构时不改变功能，但必须确保不改变功能：

**流程：**
1. **运行现有测试** - 确保全部通过（基准线）
2. **开始重构** - 修改代码结构
3. **频繁运行测试** - 每次修改后都跑测试
4. **保持绿灯** - 测试始终通过才算重构成功

**提示：先运行现有测试确认状态？**""",

            "modify": """✏️ **修改代码前先跑测试**

建议先执行：
1. **运行现有测试** - 确保当前代码状态正常
2. **进行修改** - 实施你的修改
3. **再次运行测试** - 验证修改没破坏功能

**要我先帮你运行测试吗？**""",
        }
        
        return reminders.get(task_type, reminders["new_feature"])
    
    def classify_task(self, text: str) -> str:
        """分类任务类型"""
        if re.search(r"(bug|错误|问题|修复|fix|broken)", text, re.IGNORECASE):
            return "bug_fix"
        elif re.search(r"(重构|refactor|重构|优化|improve)", text, re.IGNORECASE):
            return "refactor"
        elif re.search(r"(修改|更新|change|update|调整)", text, re.IGNORECASE):
            return "modify"
        else:
            return "new_feature"
    
    def should_remind(self, text: str, user_preference: str = "auto") -> Tuple[bool, str]:
        """
        判断是否应该提醒用户使用 TDD
        
        Args:
            text: 用户输入
            user_preference: always | auto | never
            
        Returns:
            (should_remind, reminder_message)
        """
        if user_preference == "never":
            return False, ""
        
        is_coding, reasons, confidence = self.is_coding_task(text)
        
        if not is_coding:
            return False, ""
        
        # 如果是明确的新功能或bug修复，强烈建议
        task_type = self.classify_task(text)
        
        if user_preference == "always":
            return True, self.get_reminder(task_type)
        
        # auto 模式：根据置信度决定
        if confidence >= 0.7 or task_type in ["bug_fix", "refactor"]:
            return True, self.get_reminder(task_type)
        
        return False, ""
    
    def generate_test_template(self, description: str, language: str = "python") -> str:
        """
        根据需求生成测试用例模板
        
        Args:
            description: 功能描述
            language: 编程语言
        """
        templates = {
            "python": f'''"""
测试用例 - {description}
"""
import pytest

# TODO: 导入要测试的功能
# from my_module import my_function

class TestFeature:
    """测试 {description}"""
    
    def test_basic_case(self):
        """基本场景"""
        # Arrange
        input_data = None  # TODO: 设置输入
        expected = None    # TODO: 设置预期输出
        
        # Act
        result = None      # TODO: 调用功能
        
        # Assert
        assert result == expected
    
    def test_empty_input(self):
        """空输入/边界情况"""
        pass  # TODO: 实现
    
    def test_invalid_input(self):
        """无效输入/异常处理"""
        pass  # TODO: 实现
    
    def test_edge_cases(self):
        """边界条件"""
        pass  # TODO: 实现
''',
            "javascript": f'''/**
 * 测试用例 - {description}
 */

// TODO: 导入要测试的功能
// const {{ myFunction }} = require('./myModule');

describe('{description}', () => {{
  test('基本场景', () => {{
    // Arrange
    const input = null;  // TODO: 设置输入
    const expected = null;  // TODO: 设置预期
    
    // Act
    const result = null;  // TODO: 调用功能
    
    // Assert
    expect(result).toEqual(expected);
  }});
  
  test('空输入处理', () => {{
    // TODO: 实现
  }});
  
  test('无效输入处理', () => {{
    // TODO: 实现
  }});
  
  test('边界条件', () => {{
    // TODO: 实现
  }});
}});
''',
        }
        
        return templates.get(language, templates["python"])


# 便捷函数
_assistant = None

def get_tdd_assistant() -> TDDAssistant:
    """获取 TDD 助手单例"""
    global _assistant
    if _assistant is None:
        _assistant = TDDAssistant()
    return _assistant


def check_and_remind(user_input: str, preference: str = "auto") -> Tuple[bool, str]:
    """
    检查用户输入并返回提醒
    
    Returns:
        (should_remind, message)
    """
    assistant = get_tdd_assistant()
    return assistant.should_remind(user_input, preference)


def is_coding_task(text: str) -> bool:
    """快速检测是否为编程任务"""
    assistant = get_tdd_assistant()
    is_coding, _, _ = assistant.is_coding_task(text)
    return is_coding


# 测试
if __name__ == "__main__":
    test_cases = [
        "帮我写一个提取标题的函数",
        "修复登录模块的bug",
        "重构用户认证代码",
        "今天天气怎么样",
        "帮我修改一下这个文件",
    ]
    
    assistant = TDDAssistant()
    
    print("TDD 任务检测测试:")
    print("=" * 60)
    
    for text in test_cases:
        is_coding, reasons, confidence = assistant.is_coding_task(text)
        should_remind, reminder = assistant.should_remind(text)
        
        status = "🟢 编程任务" if is_coding else "⚪ 非编程"
        remind = "💡 会提醒" if should_remind else ""
        
        print(f"\n{status} {remind}")
        print(f"输入: {text}")
        print(f"置信度: {confidence:.2f}")
        if reasons:
            print(f"原因: {', '.join(reasons)}")
