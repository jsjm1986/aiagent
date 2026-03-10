"""决策系统"""
from config import Config

class DecisionSystem:
    def __init__(self):
        self.threshold = Config.VALUE_THRESHOLD

    def select(self, scored_candidates: list) -> dict:
        """选择最优行动，拒绝后尝试替代方案"""
        if not scored_candidates:
            return None

        for candidate in scored_candidates:
            if candidate['score'] >= self.threshold:
                return candidate

        return None
