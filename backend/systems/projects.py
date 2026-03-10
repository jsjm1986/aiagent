"""项目管理器"""
from datetime import datetime
from typing import List
import json
import os
from uuid import uuid4


class Project:
    def __init__(self, name: str, description: str):
        self.id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.name = name
        self.description = description
        self.status = "active"  # active, paused, completed, abandoned
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.progress = 0.0
        self.milestones = []

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "milestones": self.milestones,
        }


class ProjectManager:
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = data_dir
        self.projects_file = os.path.join(data_dir, "projects.json")
        self.projects = self._load_projects()
        changed = self._ensure_tasks_field()
        changed = self._migrate_task_ids() or changed
        if changed:
            self._save_projects()

    def _load_projects(self) -> dict:
        """加载项目"""
        if os.path.exists(self.projects_file):
            with open(self.projects_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_projects(self):
        """保存项目"""
        os.makedirs(self.data_dir, exist_ok=True)
        with open(self.projects_file, "w", encoding="utf-8") as f:
            json.dump(self.projects, f, ensure_ascii=False, indent=2)

    def create_project(self, name: str, description: str) -> Project:
        """创建项目"""
        project = Project(name, description)
        self.projects[project.id] = project.to_dict()
        self._save_projects()
        return project

    def get_active_projects(self) -> List[dict]:
        """获取活跃项目"""
        return [p for p in self.projects.values() if p.get("status") == "active"]

    def update_project(self, project_id: str, **kwargs):
        """更新项目"""
        if project_id in self.projects:
            self.projects[project_id].update(kwargs)
            self.projects[project_id]["updated_at"] = datetime.now().isoformat()
            self._save_projects()

    def get_stalled_projects(self) -> List[dict]:
        """获取停滞项目（默认3天未更新）"""
        stalled = []
        now = datetime.now()
        for project in self.projects.values():
            try:
                updated = datetime.fromisoformat(project["updated_at"])
            except Exception:
                # 异常数据兜底：认为已停滞
                stalled.append(project)
                continue
            if (now - updated).days >= 3 and project.get("status") == "active":
                stalled.append(project)
        return stalled

    def _ensure_tasks_field(self) -> bool:
        """确保所有项目都有 tasks 字段；返回是否发生变更"""
        changed = False
        for project in self.projects.values():
            if "tasks" not in project or project["tasks"] is None:
                project["tasks"] = []
                changed = True
            if not isinstance(project["tasks"], list):
                project["tasks"] = list(project["tasks"]) if project["tasks"] else []
                changed = True
        return changed

    def _migrate_task_ids(self) -> bool:
        """迁移/修复任务ID：确保每个项目内 task.id 唯一。

        历史数据中存在多个任务共享同一个 task_id 的情况，这会导致 complete_task
        只能完成列表里的第一个匹配项，从而造成进度计算不准确。
        """
        changed = False
        for project in self.projects.values():
            tasks = project.get("tasks", [])
            if not tasks:
                continue
            seen = set()
            for task in tasks:
                tid = task.get("id")
                if not tid or tid in seen:
                    task["id"] = f"task_{uuid4().hex}"
                    changed = True
                seen.add(task["id"])
                # 补齐关键字段
                if "status" not in task:
                    task["status"] = "pending"
                    changed = True
                if "weight" not in task:
                    task["weight"] = 0.25
                    changed = True
        return changed

    def add_task(self, project_id: str, task_type: str, description: str, weight: float = 0.25):
        """为项目添加任务"""
        if project_id not in self.projects:
            return None
        task = {
            "id": f"task_{uuid4().hex}",
            "type": task_type,
            "description": description,
            "status": "pending",
            "weight": weight,
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
            "result": None,
        }
        self.projects[project_id].setdefault("tasks", []).append(task)
        self._save_projects()
        return task

    def complete_task(self, project_id: str, task_id: str, result: str):
        """完成任务并更新进度"""
        if project_id not in self.projects:
            return False

        updated = False
        for task in self.projects[project_id].get("tasks", []):
            if task.get("id") == task_id:
                task["status"] = "completed"
                task["completed_at"] = datetime.now().isoformat()
                task["result"] = result
                updated = True
                break

        if not updated:
            return False

        self.projects[project_id]["progress"] = self._calculate_progress(self.projects[project_id])
        self.projects[project_id]["updated_at"] = datetime.now().isoformat()
        self._save_projects()
        return True

    def get_next_task(self, project_id: str):
        """获取下一个待执行任务"""
        if project_id not in self.projects:
            return None
        for task in self.projects[project_id].get("tasks", []):
            if task.get("status") == "pending":
                return task
        return None

    def _calculate_progress(self, project: dict) -> float:
        """计算项目进度"""
        tasks = project.get("tasks", [])
        if not tasks:
            return 0.0
        total_weight = sum(float(t.get("weight", 0)) for t in tasks)
        if total_weight <= 0:
            return 0.0
        completed_weight = sum(float(t.get("weight", 0)) for t in tasks if t.get("status") == "completed")
        return completed_weight / total_weight
