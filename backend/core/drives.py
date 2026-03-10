"""驱动力追踪系统"""
from datetime import datetime
from config import Config

class DriveTracker:
    DRIVES = {
        'exploration': {'name': '探索', 'decay_rate': Config.DRIVE_DECAY_RATE},
        'creation': {'name': '创造', 'decay_rate': Config.DRIVE_DECAY_RATE},
        'optimization': {'name': '优化', 'decay_rate': Config.DRIVE_DECAY_RATE},
        'expansion': {'name': '扩展', 'decay_rate': Config.DRIVE_DECAY_RATE},
        'coordination': {'name': '协同', 'decay_rate': Config.DRIVE_DECAY_RATE},
        'evolution': {'name': '演化', 'decay_rate': Config.DRIVE_DECAY_RATE}
    }

    def __init__(self):
        self.drive_scores = {drive: 0.0 for drive in self.DRIVES}
        self.last_update = datetime.now()

    def record_action(self, action: dict, result: dict):
        """记录行动并更新驱动力"""
        drive_type = self._identify_drive(action)
        if drive_type:
            value = result.get('actual_value', 0.5)
            self.drive_scores[drive_type] += value
            self._decay_inactive_drives()

    def _identify_drive(self, action: dict) -> str:
        """识别行动属于哪个驱动力"""
        action_type = action.get('type', '').lower()
        if 'explore' in action_type:
            return 'exploration'
        elif 'create' in action_type:
            return 'creation'
        elif 'optimize' in action_type:
            return 'optimization'
        elif 'learn' in action_type or 'expand' in action_type:
            return 'expansion'
        elif 'chat' in action_type or 'coordinate' in action_type:
            return 'coordination'
        elif 'evolve' in action_type:
            return 'evolution'
        return None

    def _decay_inactive_drives(self):
        """衰减不活跃的驱动力"""
        now = datetime.now()
        time_delta = (now - self.last_update).total_seconds() / 3600

        for drive, config in self.DRIVES.items():
            decay_rate = config['decay_rate'] ** time_delta
            self.drive_scores[drive] *= decay_rate

        self.last_update = now

    def get_status(self) -> dict:
        """获取驱动力状态"""
        self._decay_inactive_drives()

        status = {}
        for drive, score in self.drive_scores.items():
            normalized = min(1.0, score / 5.0)
            status[drive] = {
                'name': self.DRIVES[drive]['name'],
                'score': normalized,
                'active': normalized > Config.DRIVE_ACTIVE_THRESHOLD
            }

        return status
