"""好奇心引擎 - 7个探索方向"""
from datetime import datetime

class Opportunity:
    def __init__(self, opp_type: str, description: str, value: float):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.type = opp_type
        self.description = description
        self.value = value
        self.discovered_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'description': self.description,
            'value': self.value,
            'discovered_at': self.discovered_at.isoformat()
        }

class CuriosityEngine:
    def __init__(self, project_mgr, consciousness):
        self.project_mgr = project_mgr
        self.consciousness = consciousness

    def should_explore(self, idle_time: int) -> bool:
        """判断是否应该探索"""
        return idle_time > 300  # 5分钟

    def scan_for_opportunities(self) -> list:
        """扫描探索机会"""
        opportunities = []

        # 1. 未解决的问题 - 检查停滞项目
        stalled = self.project_mgr.get_stalled_projects()
        for project in stalled:
            opportunities.append(Opportunity(
                'unsolved_problem',
                f"项目停滞: {project['name']}",
                0.8
            ))

        # 2. 信息缺口 - 简化版
        opportunities.append(Opportunity(
            'knowledge_gap',
            '探索新的技术方向',
            0.6
        ))

        return opportunities

    def select_exploration_target(self, opportunities: list):
        """选择探索目标"""
        if not opportunities:
            return None
        return max(opportunities, key=lambda x: x.value)
