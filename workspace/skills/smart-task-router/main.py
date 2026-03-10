"""
Smart Task Router - 主入口

使用方法:
    python main.py "并行: 分析这3个文件"
    python main.py "团队: 设计用户认证系统"
    python main.py --test  # 运行测试
"""

import sys
import json
import argparse
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from router import route_task, ExecutionMode
from executor import TaskExecutor, ValidationEngine


def format_routing_result(result):
    """格式化路由结果"""
    mode_names = {
        ExecutionMode.AUTO: "🤖 自动模式",
        ExecutionMode.DIRECT: "⚡ 直接执行",
        ExecutionMode.PARALLEL: "🔄 并行执行",
        ExecutionMode.TEAM: "👥 团队协作",
        ExecutionMode.DEEP: "🔍 深度分析",
    }
    
    output = f"""
╔══════════════════════════════════════════════════════════════╗
║           Smart Task Router - 路由决策结果                    ║
╠══════════════════════════════════════════════════════════════╣
  执行模式: {mode_names.get(result.mode, result.mode.value)}
  复杂度: {result.complexity.value} (评分: {result.config.get('complexity_score', 'N/A')}/100)
  推荐模型: {result.model}
  子任务数: {len(result.subtasks)}
╠══════════════════════════════════════════════════════════════╣
{result.reasoning}
╚══════════════════════════════════════════════════════════════╝
"""
    return output


def format_execution_summary(summary):
    """格式化执行摘要"""
    status_icons = {
        "success": "✅",
        "partial": "⚠️",
        "failed": "❌",
        "no_execution": "⏸️",
    }
    
    output = f"""
╔══════════════════════════════════════════════════════════════╗
║              执行结果摘要                                     ║
╠══════════════════════════════════════════════════════════════╣
  状态: {status_icons.get(summary['status'], '❓')} {summary['status'].upper()}
  总任务: {summary['total_tasks']}
  成功: {summary['success_count']} | 失败: {summary['failed_count']}
  总耗时: {summary.get('total_execution_time', 0)}s
╚══════════════════════════════════════════════════════════════╝
"""
    return output


def format_validation_result(validation):
    """格式化验证结果"""
    if validation["passed"]:
        status = "✅ 通过"
    elif validation["valid"]:
        status = "⚠️ 基本通过"
    else:
        status = "❌ 未通过"
    
    output = f"""
╔══════════════════════════════════════════════════════════════╗
║              质量验证结果                                     ║
╠══════════════════════════════════════════════════════════════╣
  状态: {status}
  评分: {validation['score']}/100
"""
    if validation["issues"]:
        output += "  问题:\n"
        for issue in validation["issues"]:
            output += f"    • {issue}\n"
    else:
        output += "  问题: 无\n"
    
    output += "╚══════════════════════════════════════════════════════════════╝"
    return output


def main():
    parser = argparse.ArgumentParser(
        description="Smart Task Router - 智能任务路由系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py "并行: 分析多个文件"
  python main.py "团队: 设计系统架构"
  python main.py "深度: 重构API"
  python main.py --test           # 运行测试
  python main.py --demo           # 运行演示
        """
    )
    
    parser.add_argument("task", nargs="?", help="要执行的任务")
    parser.add_argument("--test", action="store_true", help="运行测试套件")
    parser.add_argument("--demo", action="store_true", help="运行演示模式")
    parser.add_argument("--json", action="store_true", help="输出JSON格式")
    parser.add_argument("--dry-run", action="store_true", help="仅路由不执行")
    
    args = parser.parse_args()
    
    # 运行测试
    if args.test:
        from test_suite import run_tests
        success = run_tests()
        sys.exit(0 if success else 1)
    
    # 运行演示
    if args.demo:
        run_demo()
        return
    
    # 检查任务参数
    if not args.task:
        parser.print_help()
        print("\n错误: 请提供任务描述或使用 --test/--demo")
        sys.exit(1)
    
    # 执行任务路由
    try:
        result = route_task(args.task)
        
        # JSON输出
        if args.json:
            output = {
                "mode": result.mode.value,
                "complexity": result.complexity.value,
                "model": result.model,
                "subtasks": result.subtasks,
                "config": result.config,
                "reasoning": result.reasoning,
            }
            print(json.dumps(output, indent=2, ensure_ascii=False))
            return
        
        # 格式化输出路由结果
        print(format_routing_result(result))
        
        # 如果仅路由不执行
        if args.dry_run:
            print("\n[干运行模式] 任务未实际执行")
            return
        
        # 执行子任务
        print("\n开始执行任务...")
        executor = TaskExecutor(spawn_func=mock_spawn)
        execution_results = executor.execute(result.subtasks, result.config)
        
        # 显示执行摘要
        summary = executor.get_summary()
        print(format_execution_summary(summary))
        
        # 验证结果
        if result.config.get("verify_result"):
            print("\n正在验证结果质量...")
            validator = ValidationEngine()
            validation = validator.validate(execution_results, args.task)
            print(format_validation_result(validation))
            
            # 如果需要修复
            if validation.get("needs_fix"):
                print("\n⚠️ 结果需要改进，建议重新执行任务")
        
        print("\n✅ 任务处理完成!")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def mock_spawn(task: str) -> str:
    """
    模拟 spawn 函数
    实际环境中会调用 sessions_spawn
    """
    return f"[模拟执行完成] {task[:50]}..."


def run_demo():
    """运行演示模式"""
    demo_tasks = [
        ("查看 README.md 内容", "简单任务 - 应该走直接模式"),
        ("并行: 分析 file1.py, file2.py, file3.py", "并行任务 - 多文件分析"),
        ("深度: 重构API架构并优化性能", "复杂任务 - 深度分析模式"),
        ("团队: 设计用户认证系统", "团队任务 - 完整管道"),
    ]
    
    print("""
╔══════════════════════════════════════════════════════════════╗
║        Smart Task Router - 功能演示                          ║
║  基于 oh-my-claudecode 架构启示实现                           ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    for task, description in demo_tasks:
        print(f"\n{'='*60}")
        print(f"示例: {description}")
        print(f"任务: {task}")
        print('='*60)
        
        result = route_task(task)
        print(format_routing_result(result))


if __name__ == "__main__":
    main()
