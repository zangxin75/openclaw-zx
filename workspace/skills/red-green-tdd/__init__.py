"""
Red/Green TDD - AI编程代码质量保障

基于 Simon Willison 的 Red/Green TDD 方法论
"""

from .assistant import (
    TDDAssistant,
    get_tdd_assistant,
    check_and_remind,
    is_coding_task,
)

__version__ = "1.0.0"
__author__ = "OpenClaw"

__all__ = [
    "TDDAssistant",
    "get_tdd_assistant",
    "check_and_remind",
    "is_coding_task",
]
