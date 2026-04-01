"""
Smart Task Router - OpenClaw 自动集成

将此文件内容添加到 OpenClaw 的启动配置中，实现自动检测和路由
"""

import sys
from pathlib import Path

# 添加 STR 到路径
STR_PATH = Path.home() / ".openclaw/workspace/skills/smart-task-router"
if str(STR_PATH) not in sys.path:
    sys.path.insert(0, str(STR_PATH))

def smart_task_router_hook(user_input: str, context: dict = None):
    """
    Smart Task Router 自动检测钩子
    
    检测用户输入中的关键词前缀，自动路由到合适的执行模式
    
    Returns:
        dict or None: 如果需要路由返回路由结果，否则返回 None
    """
    try:
        from router import TaskRouter, ExecutionMode
        
        router = TaskRouter()
        mode, clean_task = router._detect_mode(user_input)
        
        # 如果没有关键词前缀且不是 AUTO 模式，不处理
        if mode == ExecutionMode.AUTO and len(user_input) < 30:
            return None
        
        # 检测到有路由需求
        return {
            "should_route": True,
            "mode": mode,
            "clean_task": clean_task,
            "original_input": user_input,
        }
        
    except Exception as e:
        # 如果 STR 未安装，静默失败
        return None


def is_smart_routed(user_input: str) -> bool:
    """检查输入是否应该被智能路由"""
    result = smart_task_router_hook(user_input)
    return result is not None and result.get("should_route", False)


# 导出的便捷函数
__all__ = ["smart_task_router_hook", "is_smart_routed"]
