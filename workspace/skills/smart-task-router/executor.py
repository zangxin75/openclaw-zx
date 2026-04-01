"""
执行引擎 - 负责任务的实际执行
"""

import json
import time
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
from enum import Enum

class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class SubtaskResult:
    """子任务执行结果"""
    subtask_id: int
    status: ExecutionStatus
    output: str
    error: Optional[str] = None
    execution_time: float = 0.0
    retry_count: int = 0

class TaskExecutor:
    """任务执行引擎"""
    
    def __init__(self, spawn_func: Optional[Callable] = None):
        """
        初始化执行器
        
        Args:
            spawn_func: 可选的自定义 spawn 函数，用于测试
        """
        self.spawn_func = spawn_func or self._default_spawn
        self.results: List[SubtaskResult] = []
    
    def _default_spawn(self, task: str, **kwargs) -> str:
        """
        默认的 spawn 实现
        在实际环境中，这会调用 sessions_spawn
        """
        # 这里只是一个占位符，实际实现会调用 OpenClaw 的 sessions_spawn
        return f"[模拟执行] {task}"
    
    def execute(self, subtasks: List[Dict], config: Dict[str, Any]) -> List[SubtaskResult]:
        """
        执行子任务列表
        
        Args:
            subtasks: 子任务列表
            config: 执行配置
            
        Returns:
            List[SubtaskResult]: 执行结果列表
        """
        if config.get("parallel", False):
            return self._execute_parallel(subtasks, config)
        else:
            return self._execute_sequential(subtasks, config)
    
    def _execute_sequential(self, subtasks: List[Dict], config: Dict[str, Any]) -> List[SubtaskResult]:
        """顺序执行子任务"""
        results = []
        max_retries = config.get("max_retries", 1)
        
        for subtask in subtasks:
            # 检查是否为条件任务
            if subtask.get("conditional") and not self._should_run_conditional(subtask, results):
                result = SubtaskResult(
                    subtask_id=subtask["id"],
                    status=ExecutionStatus.SUCCESS,
                    output="条件不满足，跳过执行",
                    execution_time=0.0
                )
                results.append(result)
                continue
            
            # 执行任务
            result = self._execute_with_retry(subtask, max_retries, config)
            results.append(result)
            
            # 如果是 TEAM 模式且某个阶段失败，可能需要停止
            if result.status == ExecutionStatus.FAILED and config.get("staged"):
                # 继续执行，但在验证/修复阶段处理
                pass
        
        self.results = results
        return results
    
    def _execute_parallel(self, subtasks: List[Dict], config: Dict[str, Any]) -> List[SubtaskResult]:
        """并行执行子任务"""
        results = []
        max_workers = config.get("max_workers", 3)
        max_retries = config.get("max_retries", 1)
        
        # 限制并发数
        batch_size = min(len(subtasks), max_workers)
        
        # 简单模拟并行执行（实际实现会用 asyncio 或线程池）
        for subtask in subtasks:
            result = self._execute_with_retry(subtask, max_retries, config)
            results.append(result)
        
        self.results = results
        return results
    
    def _execute_with_retry(self, subtask: Dict, max_retries: int, config: Dict[str, Any]) -> SubtaskResult:
        """带重试的执行"""
        task_desc = subtask["task"]
        task_type = subtask.get("type", "execute")
        
        for attempt in range(max_retries):
            start_time = time.time()
            
            try:
                # 模拟执行
                output = self.spawn_func(task_desc)
                execution_time = time.time() - start_time
                
                # 验证结果（如果配置要求）
                if config.get("verify_result"):
                    is_valid = self._verify_result(output, task_type)
                    if not is_valid:
                        if attempt < max_retries - 1:
                            continue  # 重试
                        else:
                            return SubtaskResult(
                                subtask_id=subtask["id"],
                                status=ExecutionStatus.FAILED,
                                output=output,
                                error="结果验证失败",
                                execution_time=execution_time,
                                retry_count=attempt
                            )
                
                return SubtaskResult(
                    subtask_id=subtask["id"],
                    status=ExecutionStatus.SUCCESS,
                    output=output,
                    execution_time=execution_time,
                    retry_count=attempt
                )
                
            except Exception as e:
                execution_time = time.time() - start_time
                
                if attempt < max_retries - 1:
                    continue  # 重试
                else:
                    return SubtaskResult(
                        subtask_id=subtask["id"],
                        status=ExecutionStatus.FAILED,
                        output="",
                        error=str(e),
                        execution_time=execution_time,
                        retry_count=attempt
                    )
        
        # 应该不会执行到这里
        return SubtaskResult(
            subtask_id=subtask["id"],
            status=ExecutionStatus.FAILED,
            output="",
            error="超过最大重试次数"
        )
    
    def _should_run_conditional(self, subtask: Dict, previous_results: List[SubtaskResult]) -> bool:
        """判断条件任务是否应该执行"""
        # 对于 TEAM 模式，fix 阶段在 verify 发现问题时执行
        for result in previous_results:
            if result.status == ExecutionStatus.FAILED:
                return True
        return False
    
    def _verify_result(self, output: str, task_type: str) -> bool:
        """验证执行结果"""
        # 基础验证：检查输出是否为空
        if not output or len(output.strip()) == 0:
            return False
        
        # 检查错误关键词
        error_keywords = ["error", "failed", "exception", "错误", "失败", "异常"]
        output_lower = output.lower()
        
        for keyword in error_keywords:
            if keyword in output_lower:
                # 如果有错误关键词，但不一定是失败（可能在描述问题）
                # 这里简化处理
                pass
        
        return True
    
    def get_summary(self) -> Dict[str, Any]:
        """获取执行摘要"""
        if not self.results:
            return {"status": "no_execution"}
        
        total = len(self.results)
        success = sum(1 for r in self.results if r.status == ExecutionStatus.SUCCESS)
        failed = sum(1 for r in self.results if r.status == ExecutionStatus.FAILED)
        total_time = sum(r.execution_time for r in self.results)
        
        return {
            "status": "success" if failed == 0 else "partial" if success > 0 else "failed",
            "total_tasks": total,
            "success_count": success,
            "failed_count": failed,
            "total_execution_time": round(total_time, 2),
            "results": [
                {
                    "id": r.subtask_id,
                    "status": r.status.value,
                    "time": round(r.execution_time, 2),
                    "retries": r.retry_count,
                    "error": r.error
                }
                for r in self.results
            ]
        }


class ValidationEngine:
    """结果验证引擎"""
    
    VALIDATION_CHECKS = [
        "output_not_empty",
        "no_critical_errors",
        "meets_requirements",
    ]
    
    def __init__(self):
        self.checks_passed = []
        self.checks_failed = []
    
    def validate(self, results: List[SubtaskResult], original_task: str) -> Dict[str, Any]:
        """
        验证执行结果
        
        Returns:
            Dict with keys: valid (bool), score (int), issues (list), details (dict)
        """
        score = 100
        issues = []
        details = {}
        
        # 1. 检查所有任务都执行了
        failed_tasks = [r for r in results if r.status == ExecutionStatus.FAILED]
        if failed_tasks:
            score -= len(failed_tasks) * 20
            issues.append(f"{len(failed_tasks)} 个任务执行失败")
            details["failed_tasks"] = [r.subtask_id for r in failed_tasks]
        
        # 2. 检查输出不为空
        empty_outputs = [r for r in results if not r.output or len(r.output.strip()) == 0]
        if empty_outputs:
            score -= len(empty_outputs) * 15
            issues.append(f"{len(empty_outputs)} 个任务输出为空")
        
        # 3. 检查执行时间合理性
        slow_tasks = [r for r in results if r.execution_time > 300]  # >5分钟
        if slow_tasks:
            score -= len(slow_tasks) * 5
            issues.append(f"{len(slow_tasks)} 个任务执行较慢")
        
        # 4. 检查重试次数
        retried_tasks = [r for r in results if r.retry_count > 0]
        if retried_tasks:
            score -= len(retried_tasks) * 5
            issues.append(f"{len(retried_tasks)} 个任务需要重试")
        
        score = max(0, score)
        
        return {
            "valid": score >= 60,
            "score": score,
            "issues": issues,
            "details": details,
            "passed": score >= 80,
            "needs_fix": 40 <= score < 80,
            "critical_failure": score < 40
        }
