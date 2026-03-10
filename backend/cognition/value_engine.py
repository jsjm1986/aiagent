"""价值评估引擎 - 7维度评估"""

class ValueEngine:
    DIMENSIONS = {
        'value': 0.25,
        'impact': 0.20,
        'long_term': 0.20,
        'feasibility': 0.15,
        'risk': -0.10,
        'compound': 0.10,
        'goal_alignment': 0.10
    }

    def evaluate(self, candidate: dict) -> float:
        """评估单个候选行动"""
        score = 0.0
        for dim, weight in self.DIMENSIONS.items():
            dim_score = candidate.get(dim, 0.5)
            score += dim_score * weight
        return score

    def evaluate_all(self, candidates: list) -> list:
        """评估所有候选并排序"""
        scored = []
        for candidate in candidates:
            score = self.evaluate(candidate)
            scored.append({**candidate, 'score': score})
        return sorted(scored, key=lambda x: x['score'], reverse=True)
