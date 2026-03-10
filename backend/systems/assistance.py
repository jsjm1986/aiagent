"""人类协助管理器"""
from datetime import datetime
import json
import os

class HumanAssistanceManager:
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.requests_file = os.path.join(data_dir, "assistance_requests.json")
        self.requests = self._load_requests()
        self.pending_queue = []
        self.completed_queue = []

    def _load_requests(self) -> dict:
        if os.path.exists(self.requests_file):
            with open(self.requests_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_requests(self):
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.requests_file, 'w', encoding='utf-8') as f:
            json.dump(self.requests, f, ensure_ascii=False, indent=2)

    def create_request(self, request_type: str, title: str, description: str) -> str:
        """创建协助请求"""
        request_id = datetime.now().strftime("%Y%m%d%H%M%S")
        request = {
            'id': request_id,
            'type': request_type,
            'title': title,
            'description': description,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'response': None
        }
        self.requests[request_id] = request
        self.pending_queue.append(request_id)
        self._save_requests()
        return request_id

    def get_pending(self) -> list:
        """获取待处理请求"""
        return [self.requests[rid] for rid in self.pending_queue if rid in self.requests]

    def submit_response(self, request_id: str, response: dict):
        """提交响应"""
        if request_id in self.requests:
            self.requests[request_id]['status'] = 'completed'
            self.requests[request_id]['response'] = response
            if request_id in self.pending_queue:
                self.pending_queue.remove(request_id)
            self.completed_queue.append(request_id)
            self._save_requests()
