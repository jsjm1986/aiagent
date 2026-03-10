"""长期记忆系统"""
from datetime import datetime, timedelta
import json
import os

class LongTermMemory:
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.memory_file = os.path.join(data_dir, "memory.json")
        self.memory = self._load_memory()

    def _load_memory(self) -> dict:
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'failed_actions': [],
            'successful_patterns': [],
            'mistakes': []
        }

    def _save_memory(self):
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.memory_file, 'w', encoding='utf-8') as f:
            json.dump(self.memory, f, ensure_ascii=False, indent=2)

    def store_failed_action(self, action: dict, error: str):
        """存储失败的行动"""
        self.memory['failed_actions'].append({
            'action': action,
            'error': error,
            'timestamp': datetime.now().isoformat()
        })
        self._save_memory()

    def store_mistake(self, mistake: dict):
        """存储错误教训"""
        self.memory['mistakes'].append({
            **mistake,
            'timestamp': datetime.now().isoformat()
        })
        self._save_memory()

    def get_failed_actions(self, days: int = 7) -> list:
        """获取最近失败的行动"""
        cutoff = datetime.now() - timedelta(days=days)
        return [
            a for a in self.memory['failed_actions']
            if datetime.fromisoformat(a['timestamp']) > cutoff
        ]
