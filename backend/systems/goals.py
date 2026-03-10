"""目标管理器 - 三层目标树"""
from datetime import datetime
import json
import os

class Goal:
    def __init__(self, title: str, level: str, parent_id: str = None):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self.title = title
        self.level = level  # strategic, tactical, operational
        self.parent_id = parent_id
        self.status = "active"
        self.priority = 5
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'level': self.level,
            'parent_id': self.parent_id,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat()
        }

class GoalManager:
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.goals_file = os.path.join(data_dir, "goals.json")
        self.goals = self._load_goals()

    def _load_goals(self) -> dict:
        if os.path.exists(self.goals_file):
            with open(self.goals_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_goals(self):
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.goals_file, 'w', encoding='utf-8') as f:
            json.dump(self.goals, f, ensure_ascii=False, indent=2)

    def create_goal(self, title: str, level: str, parent_id: str = None) -> Goal:
        goal = Goal(title, level, parent_id)
        self.goals[goal.id] = goal.to_dict()
        self._save_goals()
        return goal

    def get_tree(self) -> list:
        """获取目标树"""
        strategic = [g for g in self.goals.values() if g['level'] == 'strategic']
        return strategic

    def update_goal_progress(self, action: dict, result: dict):
        """更新目标进度"""
        pass
