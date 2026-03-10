"""
智能任务路由核心模块
"""

import re
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Dict, Any
from complexity import analyze_complexity, ComplexityLevel

class ExecutionMode(Enum):
    """执行模式"""
    AUTO = "auto"       # 自动模式：根据复杂度自动选择
    DIRECT = "direct"   # 直接执行：单代理直接处理
    PARALLEL = "parallel"  # 并行模式：多代理并行
    TEAM = "team"       # 团队模式：规划→执行→验证→修复
    DEEP = "deep"       # 深度模式：分析→执行→验证

@dataclass
class RoutingResult:
    """路由结果"""
    mode: ExecutionMode
    complexity: ComplexityLevel
    model: str
    subtasks: list
    config: Dict[str, Any]
    reasoning: str

class TaskRouter:
    """任务路由器"""
    
    # 关键词映射
    MODE_KEYWORDS = {
        r"^(自动|auto):\s*": ExecutionMode.AUTO,
        r"^(直接|direct):\s*": ExecutionMode.DIRECT,
        r"^(并行|并行|parallel|ulw):\s*": ExecutionMode.PARALLEL,
        r"^(团队|团队|team|ralph):\s*": ExecutionMode.TEAM,
        r"^(深度|深度|deep|analyze):\s*": ExecutionMode.DEEP,
    }
    
    def __init__(self):
        self.complexity_analyzer = None
    
    def route(self, task: str) -> RoutingResult:
        """
        路由任务到合适的执行模式
        
        Args:
            task: 用户输入的任务描述
            
        Returns:
            RoutingResult: 包含执行模式、模型、子任务等信息
        """
        # 1. 检测关键词前缀
        mode, clean_task = self._detect_mode(task)
        
        # 2. 分析复杂度
        complexity = analyze_complexity(clean_task)
        
        # 3. 如果是 AUTO 模式，根据复杂度确定执行策略
        if mode == ExecutionMode.AUTO:
            mode = self._auto_select_mode(complexity)
        
        # 4. 选择模型
        model = self._select_model(complexity.level, mode)
        
        # 5. 分解子任务
        subtasks = self._decompose_task(clean_task, mode)
        
        # 6. 生成配置
        config = self._generate_config(mode, complexity)
        
        # 7. 生成推理说明
        reasoning = self._generate_reasoning(mode, complexity, model, subtasks)
        
        return RoutingResult(
            mode=mode,
            complexity=complexity.level,
            model=model,
            subtasks=subtasks,
            config=config,
            reasoning=reasoning
        )
    
    def _detect_mode(self, task: str) -> tuple[ExecutionMode, str]:
        """检测并提取执行模式关键词"""
        for pattern, mode in self.MODE_KEYWORDS.items():
            match = re.match(pattern, task, re.IGNORECASE)
            if match:
                # 移除关键词前缀，返回清理后的任务
                clean_task = task[match.end():].strip()
                return mode, clean_task
        
        # 默认使用 AUTO 模式
        return ExecutionMode.AUTO, task.strip()
    
    def _auto_select_mode(self, complexity) -> ExecutionMode:
        """根据复杂度自动选择执行模式"""
        score = complexity.score
        
        if score >= 70:
            return ExecutionMode.TEAM
        elif score >= 50:
            return ExecutionMode.DEEP
        elif score >= 30:
            return ExecutionMode.PARALLEL
        else:
            return ExecutionMode.DIRECT
    
    def _select_model(self, complexity: ComplexityLevel, mode: ExecutionMode) -> str:
        """选择合适的模型"""
        # 基础模型映射
        base_models = {
            ComplexityLevel.LOW: "kimi-coding/k2p5",
            ComplexityLevel.MEDIUM: "kimi-coding/k2p5",
            ComplexityLevel.HIGH: "kimi-coding/k2p5",
        }
        
        # 根据模式调整
        if mode == ExecutionMode.TEAM:
            # Team 模式使用强力模型
            return "kimi-coding/k2p5"
        elif mode == ExecutionMode.DEEP:
            # Deep 模式使用强力模型
            return "kimi-coding/k2p5"
        
        return base_models.get(complexity, "kimi-coding/k2p5")
    
    def _decompose_task(self, task: str, mode: ExecutionMode) -> list:
        """根据执行模式分解任务"""
        subtasks = []
        
        if mode == ExecutionMode.DIRECT:
            # 直接模式：不分解
            subtasks = [{"id": 1, "type": "execute", "task": task}]
            
        elif mode == ExecutionMode.PARALLEL:
            # 并行模式：尝试分解为多个并行子任务
            subtasks = self._extract_parallel_subtasks(task)
            if len(subtasks) < 2:
                # 如果不能有效分解，使用多个角度分析
                subtasks = [
                    {"id": 1, "type": "analyze", "task": f"从功能角度分析: {task}"},
                    {"id": 2, "type": "analyze", "task": f"从代码质量角度分析: {task}"},
                    {"id": 3, "type": "implement", "task": f"执行主要修改: {task}"},
                ]
                
        elif mode == ExecutionMode.TEAM:
            # 团队模式：完整阶段分解
            subtasks = [
                {"id": 1, "type": "plan", "task": f"规划阶段：分析需求并制定执行计划: {task}"},
                {"id": 2, "type": "execute", "task": f"执行阶段：按计划实施: {task}"},
                {"id": 3, "type": "verify", "task": f"验证阶段：检查执行结果: {task}"},
                {"id": 4, "type": "fix", "task": f"修复阶段（如需要）：修复发现的问题", "conditional": True},
            ]
            
        elif mode == ExecutionMode.DEEP:
            # 深度模式：分析+执行+验证
            subtasks = [
                {"id": 1, "type": "analysis", "task": f"深度分析：全面理解问题: {task}"},
                {"id": 2, "type": "execute", "task": f"执行：基于分析结果实施: {task}"},
                {"id": 3, "type": "verify", "task": f"验证：检查结果质量"},
            ]
        
        return subtasks
    
    def _extract_parallel_subtasks(self, task: str) -> list:
        """从任务中提取可并行的子任务"""
        subtasks = []
        
        # 尝试识别文件/模块列表
        file_patterns = [
            r"([\w\-/]+\.\w+)",  # 文件路径
            r"`([^`]+)`",         # 代码引用
        ]
        
        # 查找显式的文件引用
        files = []
        for pattern in file_patterns:
            matches = re.findall(pattern, task)
            files.extend(matches)
        
        # 如果有多个文件，按文件分解
        if len(files) >= 2:
            for i, f in enumerate(files[:5], 1):  # 最多5个
                subtasks.append({
                    "id": i,
                    "type": "process",
                    "task": f"处理文件/模块: {f}",
                    "target": f
                })
        
        return subtasks
    
    def _generate_config(self, mode: ExecutionMode, complexity) -> Dict[str, Any]:
        """生成执行配置"""
        configs = {
            ExecutionMode.DIRECT: {
                "max_retries": 1,
                "verify_result": False,
                "parallel": False,
                "timeout": 300,
            },
            ExecutionMode.PARALLEL: {
                "max_retries": 2,
                "verify_result": True,
                "parallel": True,
                "max_workers": 3,
                "timeout": 600,
            },
            ExecutionMode.TEAM: {
                "max_retries": 3,
                "verify_result": True,
                "parallel": False,
                "staged": True,
                "timeout": 1800,
            },
            ExecutionMode.DEEP: {
                "max_retries": 2,
                "verify_result": True,
                "parallel": False,
                "deep_analysis": True,
                "timeout": 1200,
            },
        }
        
        config = configs.get(mode, configs[ExecutionMode.DIRECT]).copy()
        config["complexity_score"] = complexity.score
        config["complexity_reasons"] = complexity.reasons
        
        return config
    
    def _generate_reasoning(self, mode: ExecutionMode, complexity, model: str, subtasks: list) -> str:
        """生成路由决策说明"""
        mode_names = {
            ExecutionMode.DIRECT: "直接执行模式",
            ExecutionMode.PARALLEL: "并行执行模式",
            ExecutionMode.TEAM: "团队协作模式",
            ExecutionMode.DEEP: "深度分析模式",
        }
        
        level_names = {
            ComplexityLevel.LOW: "低复杂度",
            ComplexityLevel.MEDIUM: "中等复杂度",
            ComplexityLevel.HIGH: "高复杂度",
        }
        
        reasoning = f"""路由决策：
- 执行模式: {mode_names.get(mode, mode.value)}
- 任务复杂度: {level_names.get(complexity.level, complexity.level.value)} (评分: {complexity.score}/100)
- 使用模型: {model}
- 子任务数: {len(subtasks)}

复杂度评估依据:
"""
        for reason in complexity.reasons:
            reasoning += f"  • {reason}\n"
        
        reasoning += f"\n执行计划:\n"
        for subtask in subtasks:
            conditional = " (条件执行)" if subtask.get("conditional") else ""
            reasoning += f"  {subtask['id']}. [{subtask['type'].upper()}] {subtask['task']}{conditional}\n"
        
        return reasoning


# 便捷函数
_router = None

def get_router() -> TaskRouter:
    """获取路由器单例"""
    global _router
    if _router is None:
        _router = TaskRouter()
    return _router

def route_task(task: str) -> RoutingResult:
    """便捷函数：路由任务"""
    return get_router().route(task)
