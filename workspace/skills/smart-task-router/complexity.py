"""
复杂度评估模块 - 自动判断任务复杂度
"""

import re
from enum import Enum
from dataclasses import dataclass

class ComplexityLevel(Enum):
    LOW = "low"       # 简单任务，轻量模型
    MEDIUM = "medium" # 中等任务，标准模型
    HIGH = "high"     # 复杂任务，强力模型

@dataclass
class ComplexityScore:
    level: ComplexityLevel
    score: int  # 0-100
    reasons: list

class ComplexityAnalyzer:
    """任务复杂度分析器"""
    
    # 复杂度指标权重
    WEIGHTS = {
        "code_volume": 25,      # 代码量指标
        "concept_count": 20,    # 概念数量
        "dependency": 15,       # 依赖复杂度
        "reasoning": 20,        # 推理深度
        "uncertainty": 20,      # 不确定性
    }
    
    # 复杂度信号
    HIGH_COMPLEXITY_SIGNALS = [
        r"(重构|重构|refactor)",
        r"(架构|architecture|设计|design)",
        r"(系统|system|框架|framework)",
        r"(优化|optimize|性能|performance)",
        r"(安全|security|漏洞|vulnerability)",
        r"(多|multiple|批量|batch)",
        r"(全|all|整个|entire)",
        r"(复杂|complex|困难|difficult)",
        r"(分析|analyze|调研|research)",
        r"(实现|implement|开发|develop).*?(系统|模块|功能)",
        r"(迁移|migration|升级|upgrade)",
        r"(集成|integrate|整合)",
        r"(分布式|distributed|微服务|microservice)",
    ]
    
    MEDIUM_COMPLEXITY_SIGNALS = [
        r"(修复|fix|解决|resolve)",
        r"(添加|add|创建|create)",
        r"(修改|modify|更新|update)",
        r"(测试|test|验证|verify)",
        r"(文档|doc|注释|comment)",
        r"(配置|config|设置|setup)",
        r"(查询|query|搜索|search)",
        r"(生成|generate|构建|build)",
    ]
    
    LOW_COMPLEXITY_SIGNALS = [
        r"(查看|view|读取|read)",
        r"(检查|check|确认|confirm)",
        r"(列出|list|显示|show)",
        r"(转换|convert|格式化|format)",
        r"(简单|simple|快速|quick)",
    ]
    
    def analyze(self, task: str) -> ComplexityScore:
        """分析任务复杂度"""
        reasons = []
        total_score = 0
        
        # 1. 检查高复杂度信号
        high_matches = self._count_matches(task, self.HIGH_COMPLEXITY_SIGNALS)
        if high_matches > 0:
            total_score += min(high_matches * 25, 50)
            reasons.append(f"检测到{high_matches}个高复杂度信号")
        
        # 2. 检查中等复杂度信号
        medium_matches = self._count_matches(task, self.MEDIUM_COMPLEXITY_SIGNALS)
        if medium_matches > 0:
            total_score += min(medium_matches * 10, 20)
            reasons.append(f"检测到{medium_matches}个中复杂度信号")
        
        # 3. 检查低复杂度信号
        low_matches = self._count_matches(task, self.LOW_COMPLEXITY_SIGNALS)
        if low_matches > 0:
            total_score -= min(low_matches * 5, 15)
            reasons.append(f"检测到{low_matches}个低复杂度信号")
        
        # 4. 任务长度指标
        char_count = len(task)
        if char_count > 200:
            total_score += 15
            reasons.append("任务描述较长，可能涉及多个方面")
        elif char_count > 100:
            total_score += 5
            reasons.append("任务描述中等长度")
        else:
            total_score -= 5
            reasons.append("任务描述简洁")
        
        # 5. 代码/文件引用数量
        code_refs = len(re.findall(r"[\w\-/]+\.\w+|`[^`]+`|```", task))
        if code_refs > 5:
            total_score += 15
            reasons.append(f"引用较多代码/文件({code_refs}处)")
        elif code_refs > 2:
            total_score += 5
            reasons.append(f"引用一些代码/文件({code_refs}处)")
        
        # 6. 分句数量（任务分解度）
        sentences = len(re.findall(r"[。！；;]|\n", task))
        if sentences > 3:
            total_score += 10
            reasons.append(f"任务包含多个子任务({sentences}个分句)")
        
        # 边界处理
        total_score = max(0, min(100, total_score))
        
        # 确定复杂度等级
        if total_score >= 60:
            level = ComplexityLevel.HIGH
        elif total_score >= 30:
            level = ComplexityLevel.MEDIUM
        else:
            level = ComplexityLevel.LOW
        
        return ComplexityScore(level=level, score=total_score, reasons=reasons)
    
    def _count_matches(self, text: str, patterns: list) -> int:
        """计算匹配的模式数量"""
        count = 0
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                count += 1
        return count
    
    def get_model_for_complexity(self, level: ComplexityLevel) -> str:
        """根据复杂度获取推荐模型"""
        model_map = {
            ComplexityLevel.LOW: "kimi-coding/k2p5",
            ComplexityLevel.MEDIUM: "kimi-coding/k2p5",
            ComplexityLevel.HIGH: "kimi-coding/k2p5",
        }
        return model_map.get(level, "kimi-coding/k2p5")


# 单例实例
_analyzer = None

def get_analyzer() -> ComplexityAnalyzer:
    """获取复杂度分析器单例"""
    global _analyzer
    if _analyzer is None:
        _analyzer = ComplexityAnalyzer()
    return _analyzer


def analyze_complexity(task: str) -> ComplexityScore:
    """便捷函数：分析任务复杂度"""
    return get_analyzer().analyze(task)
