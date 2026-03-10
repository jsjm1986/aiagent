"""意识流系统"""
from datetime import datetime
import json
import os

class ConsciousnessStream:
    def __init__(self, data_dir: str = "./data/consciousness"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def record(self, thought_type: str, content: dict):
        """记录思考"""
        thought = {
            'timestamp': datetime.now().isoformat(),
            'type': thought_type,
            'content': content
        }

        # 按日期存储
        date = datetime.now().strftime("%Y%m%d")
        file_path = os.path.join(self.data_dir, f"{date}.jsonl")

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(thought, ensure_ascii=False) + '\n')

    def get_recent(self, limit: int = 50) -> list:
        """获取最近的思考"""
        thoughts = []
        date = datetime.now().strftime("%Y%m%d")
        file_path = os.path.join(self.data_dir, f"{date}.jsonl")

        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    thoughts.append(json.loads(line))

        return thoughts
