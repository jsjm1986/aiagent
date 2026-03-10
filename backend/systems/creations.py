"""创造成果画廊"""
from datetime import datetime
import json
import os

class CreationGallery:
    def __init__(self, data_dir: str = "./data/creations"):
        self.data_dir = data_dir
        self.index_file = os.path.join(data_dir, "index.json")
        os.makedirs(data_dir, exist_ok=True)
        self.creations = self._load_index()

    def _load_index(self) -> dict:
        if os.path.exists(self.index_file):
            with open(self.index_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_index(self):
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.creations, f, ensure_ascii=False, indent=2)

    def save_creation(self, title: str, content: str, creation_type: str = "code"):
        """保存创造"""
        creation_id = datetime.now().strftime("%Y%m%d%H%M%S")
        creation = {
            'id': creation_id,
            'title': title,
            'type': creation_type,
            'created_at': datetime.now().isoformat()
        }

        # 保存内容到文件
        file_path = os.path.join(self.data_dir, f"{creation_id}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        self.creations[creation_id] = creation
        self._save_index()
        return creation_id

    def get_all(self) -> list:
        """获取所有创造"""
        result = []
        for creation_id, creation in self.creations.items():
            file_path = os.path.join(self.data_dir, f"{creation_id}.txt")
            content = ""
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            result.append({**creation, 'content': content})
        return result
