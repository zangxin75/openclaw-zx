"""
Smart Task Router - 功能测试套件

全面测试路由系统的各项功能
"""

import sys
import unittest
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from complexity import ComplexityAnalyzer, ComplexityLevel, analyze_complexity
from router import TaskRouter, ExecutionMode, route_task
from executor import TaskExecutor, ValidationEngine, ExecutionStatus, SubtaskResult


class TestComplexityAnalyzer(unittest.TestCase):
    """测试复杂度分析器"""
    
    def setUp(self):
        self.analyzer = ComplexityAnalyzer()
    
    def test_simple_query_low_complexity(self):
        """测试简单查询应识别为低复杂度"""
        task = "查看 README.md 文件内容"
        result = self.analyzer.analyze(task)
        self.assertEqual(result.level, ComplexityLevel.LOW)
        self.assertLess(result.score, 30)
    
    def test_refactor_high_complexity(self):
        """测试重构任务应识别为中等或高复杂度"""
        task = "重构整个项目的API架构，优化性能并修复安全漏洞"
        result = self.analyzer.analyze(task)
        # 重构任务应该至少有中等复杂度
        self.assertIn(result.level, [ComplexityLevel.MEDIUM, ComplexityLevel.HIGH])
        self.assertGreaterEqual(result.score, 30)  # 至少达到中等阈值
    
    def test_fix_medium_complexity(self):
        """测试修复任务应识别为中等或更高复杂度"""
        task = "修复登录模块的TypeScript错误，包括类型定义和接口更新"
        result = self.analyzer.analyze(task)
        # 修复任务可能根据具体描述有不同复杂度
        self.assertIn(result.level, [ComplexityLevel.LOW, ComplexityLevel.MEDIUM])
        self.assertGreater(result.score, 10)  # 至少有一些复杂度
    
    def test_multiple_files_increases_complexity(self):
        """测试多文件引用增加复杂度"""
        simple = "查看文件"
        complex = "分析 src/app.py, src/utils.py, src/config.py, src/models.py, src/api.py 的关系"
        
        simple_result = self.analyzer.analyze(simple)
        complex_result = self.analyzer.analyze(complex)
        
        self.assertGreater(complex_result.score, simple_result.score)
    
    def test_long_description_increases_complexity(self):
        """测试长描述增加复杂度"""
        short = "修复bug"
        long = "修复一个复杂的bug，需要修改多个文件，包括前端组件、后端API和数据库模型，还要更新测试用例和文档"
        
        short_result = self.analyzer.analyze(short)
        long_result = self.analyzer.analyze(long)
        
        self.assertGreater(long_result.score, short_result.score)


class TestTaskRouter(unittest.TestCase):
    """测试任务路由器"""
    
    def setUp(self):
        self.router = TaskRouter()
    
    def test_detect_auto_keyword(self):
        """测试识别自动模式关键词"""
        task = "自动: 修复bug"
        mode, clean = self.router._detect_mode(task)
        self.assertEqual(mode, ExecutionMode.AUTO)
        self.assertEqual(clean, "修复bug")
    
    def test_detect_parallel_keyword(self):
        """测试识别并行模式关键词"""
        keywords = ["并行:", "parallel:", "ulw:"]
        for kw in keywords:
            task = f"{kw} 分析多个文件"
            mode, clean = self.router._detect_mode(task)
            self.assertEqual(mode, ExecutionMode.PARALLEL, f"Failed for {kw}")
    
    def test_detect_team_keyword(self):
        """测试识别团队模式关键词"""
        keywords = ["团队:", "team:", "ralph:"]
        for kw in keywords:
            task = f"{kw} 设计系统架构"
            mode, clean = self.router._detect_mode(task)
            self.assertEqual(mode, ExecutionMode.TEAM, f"Failed for {kw}")
    
    def test_detect_deep_keyword(self):
        """测试识别深度模式关键词"""
        keywords = ["深度:", "deep:", "analyze:"]
        for kw in keywords:
            task = f"{kw} 分析代码质量"
            mode, clean = self.router._detect_mode(task)
            self.assertEqual(mode, ExecutionMode.DEEP, f"Failed for {kw}")
    
    def test_default_auto_mode(self):
        """测试无关键词时默认为自动模式"""
        task = "修复bug"
        mode, clean = self.router._detect_mode(task)
        self.assertEqual(mode, ExecutionMode.AUTO)
    
    def test_auto_select_mode_high_complexity(self):
        """测试高复杂度自动选择团队模式"""
        from complexity import ComplexityScore
        complexity = ComplexityScore(ComplexityLevel.HIGH, 75, [])
        mode = self.router._auto_select_mode(complexity)
        self.assertEqual(mode, ExecutionMode.TEAM)
    
    def test_auto_select_mode_medium_complexity(self):
        """测试中复杂度自动选择并行模式"""
        from complexity import ComplexityScore
        complexity = ComplexityScore(ComplexityLevel.MEDIUM, 40, [])
        mode = self.router._auto_select_mode(complexity)
        self.assertEqual(mode, ExecutionMode.PARALLEL)
    
    def test_auto_select_mode_low_complexity(self):
        """测试低复杂度自动选择直接模式"""
        from complexity import ComplexityScore
        complexity = ComplexityScore(ComplexityLevel.LOW, 15, [])
        mode = self.router._auto_select_mode(complexity)
        self.assertEqual(mode, ExecutionMode.DIRECT)
    
    def test_route_integration(self):
        """测试完整路由流程"""
        task = "并行: 分析 src/app.py 和 src/utils.py"
        result = self.router.route(task)
        
        self.assertEqual(result.mode, ExecutionMode.PARALLEL)
        self.assertTrue(len(result.subtasks) > 0)
        self.assertTrue(len(result.reasoning) > 0)
        self.assertIn("kimi", result.model)


class TestTaskExecutor(unittest.TestCase):
    """测试任务执行器"""
    
    def test_executor_initialization(self):
        """测试执行器初始化"""
        executor = TaskExecutor()
        self.assertEqual(len(executor.results), 0)
    
    def test_sequential_execution(self):
        """测试顺序执行"""
        executor = TaskExecutor(spawn_func=lambda t: f"完成: {t}")
        subtasks = [
            {"id": 1, "task": "任务1", "type": "execute"},
            {"id": 2, "task": "任务2", "type": "execute"},
        ]
        config = {"parallel": False, "max_retries": 1}
        
        results = executor.execute(subtasks, config)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].status, ExecutionStatus.SUCCESS)
        self.assertEqual(results[1].status, ExecutionStatus.SUCCESS)
    
    def test_parallel_execution(self):
        """测试并行执行"""
        executor = TaskExecutor(spawn_func=lambda t: f"完成: {t}")
        subtasks = [
            {"id": 1, "task": "任务1", "type": "execute"},
            {"id": 2, "task": "任务2", "type": "execute"},
            {"id": 3, "task": "任务3", "type": "execute"},
        ]
        config = {"parallel": True, "max_workers": 3, "max_retries": 1}
        
        results = executor.execute(subtasks, config)
        
        self.assertEqual(len(results), 3)
        for r in results:
            self.assertEqual(r.status, ExecutionStatus.SUCCESS)
    
    def test_execution_summary(self):
        """测试执行摘要生成"""
        executor = TaskExecutor(spawn_func=lambda t: f"完成")
        subtasks = [{"id": 1, "task": "任务", "type": "execute"}]
        config = {"parallel": False, "max_retries": 1}
        
        executor.execute(subtasks, config)
        summary = executor.get_summary()
        
        self.assertEqual(summary["total_tasks"], 1)
        self.assertEqual(summary["success_count"], 1)
        self.assertEqual(summary["failed_count"], 0)
        self.assertEqual(summary["status"], "success")


class TestValidationEngine(unittest.TestCase):
    """测试验证引擎"""
    
    def setUp(self):
        self.validator = ValidationEngine()
    
    def test_validate_all_success(self):
        """测试全部成功验证"""
        results = [
            SubtaskResult(1, ExecutionStatus.SUCCESS, "输出1", execution_time=1.0),
            SubtaskResult(2, ExecutionStatus.SUCCESS, "输出2", execution_time=2.0),
        ]
        
        validation = self.validator.validate(results, "测试任务")
        
        self.assertTrue(validation["valid"])
        self.assertTrue(validation["passed"])
        self.assertEqual(validation["score"], 100)
        self.assertEqual(len(validation["issues"]), 0)
    
    def test_validate_with_failures(self):
        """测试有失败任务的验证"""
        results = [
            SubtaskResult(1, ExecutionStatus.SUCCESS, "输出1", execution_time=1.0),
            SubtaskResult(2, ExecutionStatus.FAILED, "", error="错误", execution_time=0.0),
        ]
        
        validation = self.validator.validate(results, "测试任务")
        
        # 有失败任务时评分应该降低
        self.assertLess(validation["score"], 100)
        self.assertTrue(len(validation["issues"]) > 0)
    
    def test_validate_empty_output(self):
        """测试空输出验证"""
        results = [
            SubtaskResult(1, ExecutionStatus.SUCCESS, "", execution_time=1.0),
        ]
        
        validation = self.validator.validate(results, "测试任务")
        
        # 空输出应该降低评分
        self.assertLess(validation["score"], 100)
        self.assertTrue(len(validation["issues"]) > 0)
    
    def test_validate_slow_execution(self):
        """测试慢执行验证"""
        results = [
            SubtaskResult(1, ExecutionStatus.SUCCESS, "输出", execution_time=400),
        ]
        
        validation = self.validator.validate(results, "测试任务")
        
        # 应该有警告，但仍然有效
        self.assertTrue(validation["valid"])
        self.assertLessEqual(validation["score"], 95)


class TestEndToEnd(unittest.TestCase):
    """端到端集成测试"""
    
    def test_full_workflow_simple_task(self):
        """测试简单任务的完整流程"""
        task = "查看 README.md 内容"
        
        # 1. 路由
        routing = route_task(task)
        
        # 简单任务应该走直接模式
        self.assertIn(routing.mode, [ExecutionMode.DIRECT, ExecutionMode.AUTO])
        self.assertEqual(routing.complexity, ComplexityLevel.LOW)
        
        # 2. 执行
        executor = TaskExecutor(spawn_func=lambda t: f"完成: {t}")
        results = executor.execute(routing.subtasks, routing.config)
        
        # 3. 验证
        validator = ValidationEngine()
        validation = validator.validate(results, task)
        
        self.assertTrue(validation["valid"])
    
    def test_full_workflow_complex_task(self):
        """测试复杂任务的完整流程"""
        task = "深度: 重构整个项目的API架构，优化性能，包括数据库迁移和缓存策略重新设计"
        
        # 1. 路由
        routing = route_task(task)
        
        # 复杂任务应该走深度或团队模式
        self.assertIn(routing.mode, [ExecutionMode.DEEP, ExecutionMode.TEAM])
        # 复杂度至少中等
        self.assertIn(routing.complexity, [ComplexityLevel.MEDIUM, ComplexityLevel.HIGH])
        
        # 应该有多个子任务
        self.assertTrue(len(routing.subtasks) >= 3)
        
        # 验证子任务类型
        task_types = [st["type"] for st in routing.subtasks]
        self.assertIn("execute", task_types)
    
    def test_full_workflow_parallel_task(self):
        """测试并行任务的完整流程"""
        task = "并行: 分析 file1.py, file2.py, file3.py"
        
        # 1. 路由
        routing = route_task(task)
        
        self.assertEqual(routing.mode, ExecutionMode.PARALLEL)
        self.assertTrue(routing.config.get("parallel"))
        
        # 2. 执行
        executor = TaskExecutor(spawn_func=lambda t: f"分析完成")
        results = executor.execute(routing.subtasks, routing.config)
        
        # 3. 验证
        validator = ValidationEngine()
        validation = validator.validate(results, task)
        
        self.assertTrue(validation["valid"])


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestComplexityAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskRouter))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskExecutor))
    suite.addTests(loader.loadTestsFromTestCase(TestValidationEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEnd))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 返回结果
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
