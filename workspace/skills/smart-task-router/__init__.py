"""
Smart Task Router (STR)

智能任务路由系统 - 基于 oh-my-claudecode 架构启示实现

主要功能:
- 关键词触发执行模式
- 自动复杂度评估
- 多模式任务执行
- 结果验证循环

示例:
    >>> from smart_task_router import route_task, execute_task
    >>> result = route_task("并行: 分析多个文件")
    >>> output = execute_task(result)
"""

__version__ = "1.0.0"
__author__ = "OpenClaw"

from .router import TaskRouter, ExecutionMode, RoutingResult, route_task
from .complexity import ComplexityAnalyzer, ComplexityLevel, analyze_complexity
from .executor import TaskExecutor, ValidationEngine, ExecutionStatus

__all__ = [
    # Router
    "TaskRouter",
    "ExecutionMode", 
    "RoutingResult",
    "route_task",
    # Complexity
    "ComplexityAnalyzer",
    "ComplexityLevel",
    "analyze_complexity",
    # Executor
    "TaskExecutor",
    "ValidationEngine",
    "ExecutionStatus",
]
