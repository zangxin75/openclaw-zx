"""
OpenClaw 集成入口 - Smart Task Router

在 OpenClaw 会话中使用此模块进行智能任务路由

使用示例:
    from smart_task_router.openclaw_integration import smart_execute
    result = smart_execute("并行: 分析代码")
"""

import sys
from pathlib import Path

# 添加技能目录到路径
SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

from router import route_task, ExecutionMode
from executor import TaskExecutor, ValidationEngine


def smart_execute(task: str, context: dict = None):
    """
    智能执行任务 - OpenClaw 主要入口
    
    Args:
        task: 用户输入的任务描述
        context: 可选的上下文信息
        
    Returns:
        dict: 包含路由、执行和验证结果的字典
    
    使用示例:
        result = smart_execute("并行: 分析 src/app.py 和 src/utils.py")
        
        # 查看路由决策
        print(result['routing']['reasoning'])
        
        # 查看执行结果
        print(result['execution']['summary'])
        
        # 查看验证结果
        print(result['validation']['score'])
    """
    print(f"🎯 任务: {task[:80]}...")
    
    # 1. 路由任务
    routing = route_task(task)
    
    mode_icons = {
        ExecutionMode.DIRECT: "⚡",
        ExecutionMode.PARALLEL: "🔄",
        ExecutionMode.TEAM: "👥",
        ExecutionMode.DEEP: "🔍",
        ExecutionMode.AUTO: "🤖",
    }
    
    icon = mode_icons.get(routing.mode, "▶️")
    print(f"{icon} 执行模式: {routing.mode.value}")
    print(f"📊 复杂度: {routing.complexity.value}")
    print(f"📋 子任务: {len(routing.subtasks)} 个")
    
    if context and context.get('verbose'):
        print(f"\n{routing.reasoning}")
    
    # 2. 准备执行函数
    # 在实际 OpenClaw 环境中，这会调用 sessions_spawn
    def default_spawn(subtask_desc: str) -> str:
        """
        默认执行函数 - 模拟执行
        实际使用时应该调用:
        - sessions_spawn(task=subtask_desc, runtime="subagent")
        - 或其他实际执行机制
        """
        return f"[执行完成] {subtask_desc[:50]}..."
    
    # 使用上下文中的 spawn 函数或默认函数
    spawn_func = context.get('spawn_func') if context else None
    if spawn_func is None:
        spawn_func = default_spawn
    
    # 3. 执行子任务
    print("\n▶️ 开始执行...")
    executor = TaskExecutor(spawn_func=spawn_func)
    results = executor.execute(routing.subtasks, routing.config)
    
    # 4. 获取执行摘要
    summary = executor.get_summary()
    
    status_icons = {
        "success": "✅",
        "partial": "⚠️",
        "failed": "❌",
    }
    icon = status_icons.get(summary['status'], "❓")
    print(f"\n{icon} 执行状态: {summary['status']}")
    print(f"   成功: {summary['success_count']} | 失败: {summary['failed_count']}")
    print(f"   耗时: {summary.get('total_execution_time', 0)}s")
    
    # 5. 验证结果
    validation_result = None
    if routing.config.get("verify_result"):
        print("\n🔍 验证结果质量...")
        validator = ValidationEngine()
        validation = validator.validate(results, task)
        
        if validation["passed"]:
            print(f"✅ 质量验证通过 (评分: {validation['score']}/100)")
        elif validation["valid"]:
            print(f"⚠️ 质量基本通过 (评分: {validation['score']}/100)")
            if validation["issues"]:
                print("   问题:", "; ".join(validation["issues"]))
        else:
            print(f"❌ 质量验证未通过 (评分: {validation['score']}/100)")
            print("   问题:", "; ".join(validation["issues"]))
        
        if validation.get("needs_fix"):
            print("\n💡 建议：结果可以进一步优化")
        
        validation_result = validation
    
    return {
        "routing": {
            "mode": routing.mode.value,
            "complexity": routing.complexity.value,
            "model": routing.model,
            "subtasks": routing.subtasks,
            "config": routing.config,
            "reasoning": routing.reasoning,
        },
        "execution": {
            "summary": summary,
            "results": [
                {
                    "id": r.subtask_id,
                    "status": r.status.value,
                    "output": r.output,
                    "error": r.error,
                    "time": r.execution_time,
                    "retries": r.retry_count,
                }
                for r in results
            ]
        },
        "validation": validation_result,
    }


def detect_and_route(user_input: str) -> dict:
    """
    检测用户输入是否需要智能路由
    
    Returns:
        dict with keys:
            - should_route: bool - 是否需要路由
            - mode: str - 检测到的模式
            - clean_task: str - 清理后的任务
    """
    from router import TaskRouter
    
    router = TaskRouter()
    mode, clean_task = router._detect_mode(user_input)
    
    return {
        "should_route": mode != ExecutionMode.AUTO or len(clean_task) > 20,
        "mode": mode.value,
        "clean_task": clean_task,
    }


# 便捷函数
def parallel(task: str, **kwargs):
    """并行模式快捷入口"""
    return smart_execute(f"并行: {task}", **kwargs)

def team(task: str, **kwargs):
    """团队模式快捷入口"""
    return smart_execute(f"团队: {task}", **kwargs)

def deep(task: str, **kwargs):
    """深度模式快捷入口"""
    return smart_execute(f"深度: {task}", **kwargs)


if __name__ == "__main__":
    # 测试运行
    import json
    
    if len(sys.argv) > 1:
        task = sys.argv[1]
    else:
        task = "并行: 分析 README.md 和 SKILL.md"
    
    print("=" * 60)
    print("Smart Task Router - OpenClaw 集成测试")
    print("=" * 60)
    
    result = smart_execute(task, context={"verbose": True})
    
    print("\n" + "=" * 60)
    print("完整结果 (JSON):")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))
