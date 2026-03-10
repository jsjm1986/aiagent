"""自主运行引擎"""
import asyncio
import random
import requests
from datetime import datetime
from smolagents import CodeAgent, LiteLLMModel
from config import Config
from cognition.value_engine import ValueEngine
from cognition.decision import DecisionSystem
from cognition.curiosity import CuriosityEngine
from cognition.evolution import EvolutionEngine
from core.drives import DriveTracker
from core.event_bus import EventBus
from systems.projects import ProjectManager
from systems.goals import GoalManager
from systems.consciousness import ConsciousnessStream
from systems.creations import CreationGallery
from systems.assistance import HumanAssistanceManager
from systems.memory import LongTermMemory
from tools.consciousness_tool import ConsciousnessRecordTool
from tools.creation_tool import CreationGalleryTool
from tools.project_tool import ProjectManagementTool
from tools.assistance_tool import RequestHumanHelpTool
from tools.web_search_tool import WebSearchTool
from tools.python_execute_tool import PythonExecuteTool
from tools.js_execute_tool import JSExecuteTool
from tools.file_operation_tool import FileOperationTool

class AutonomousEngine:
    def __init__(self):
        self.config = Config()
        self.running = False

        # 核心组件
        self.value_engine = ValueEngine()
        self.decision_system = DecisionSystem()
        self.drive_tracker = DriveTracker()
        self.event_bus = EventBus()

        # 系统组件
        self.project_mgr = ProjectManager(Config.DATA_DIR)
        self.goal_mgr = GoalManager(Config.DATA_DIR)
        self.consciousness = ConsciousnessStream(Config.CONSCIOUSNESS_DIR)
        self.creations = CreationGallery(Config.CREATIONS_DIR)
        self.assistance_mgr = HumanAssistanceManager(Config.DATA_DIR)
        self.memory = LongTermMemory(Config.DATA_DIR)

        # 好奇心引擎
        self.curiosity = CuriosityEngine(self.project_mgr, self.consciousness)

        # 演化引擎
        self.evolution = EvolutionEngine(self.value_engine, Config.DATA_DIR)

        # Agent
        self.agent = self._create_agent()

        # 状态
        self.idle_time = 0

    def _create_agent(self):
        """创建 smolagents Agent"""
        model = LiteLLMModel(
            model_id=Config.MODEL_NAME,
            api_key=Config.API_KEY,
            api_base=Config.API_BASE
        )

        tools = [
            ConsciousnessRecordTool(self.consciousness),
            CreationGalleryTool(self.creations),
            ProjectManagementTool(self.project_mgr),
            RequestHumanHelpTool(self.assistance_mgr),
            WebSearchTool(),
            PythonExecuteTool(),
            JSExecuteTool(),
            FileOperationTool()
        ]

        return CodeAgent(tools=tools, model=model, max_steps=Config.MAX_STEPS)

    async def run_forever(self):
        """主循环 - 完整10步自主决策循环"""
        self.running = True
        with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] RUN_FOREVER: 开始运行\n")
            f.flush()

        while self.running:
            try:
                with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] LOOP: 开始新循环\n")
                    f.flush()

                # 1. 感知环境
                perception = await self._perceive()
                self.consciousness.record('perception', perception)

                # 2. 认知分析
                cognition = await self._analyze(perception)
                self.consciousness.record('cognition', cognition)

                # 3. 生成候选行动
                candidates = await self._generate_candidates(cognition)
                self.consciousness.record('candidates', {'list': candidates, 'count': len(candidates)})

                # 4. 价值评分
                scored = self.value_engine.evaluate_all(candidates)
                self.consciousness.record('value_scoring', {'scored': scored})
                with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] 价值评分完成,最高分: {max([s.get('score', 0) for s in scored]) if scored else 0:.2f}\n")
                    f.flush()

                # 5. 决策选择
                selected = self.decision_system.select(scored)
                with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] 决策选择: {'已选中' if selected else '无符合条件'}\n")
                    f.flush()
                if selected:
                    self.consciousness.record('selection', selected)

                    # 6. 执行行动
                    result = await self._execute_action(selected)
                    self.consciousness.record('execution', result)
                    self.drive_tracker.record_action(selected, result)

                    # 7. 好奇心探索
                    opportunities = self.curiosity.scan_for_opportunities()
                    if opportunities:
                        target = self.curiosity.select_exploration_target(opportunities)
                        if target:
                            self.consciousness.record('curiosity', target.to_dict())

                    # 8. 学习演化
                    self.evolution.evolve_after_action(selected, result)
                    self.consciousness.record('learning', {'action': selected['description'], 'outcome': result.get('success')})

                    # 9. 反思
                    reflection = self._reflect(selected, result)
                    self.consciousness.record('reflection', reflection)

                await asyncio.sleep(10)

            except Exception as e:
                print(f"[ERROR] 主循环错误: {e}")
                await asyncio.sleep(10)

    async def _perceive(self) -> dict:
        """感知环境状态"""
        projects = self.project_mgr.get_active_projects()
        goals = self.goal_mgr.get_tree()
        return {
            'project_count': len(projects),
            'active_projects': len([p for p in projects if p.get('status') == 'active']),
            'stalled_projects': len(self.project_mgr.get_stalled_projects()),
            'active_goals': len(goals),
            'timestamp': datetime.now().isoformat()
        }

    async def _analyze(self, perception: dict) -> dict:
        """认知分析"""
        project_count = perception['project_count']
        stalled = perception['stalled_projects']

        if project_count < 10:
            mode = 'create'
            priority = 'expand_capacity'
        elif stalled > 0:
            mode = 'revive'
            priority = 'fix_stalled'
        else:
            mode = 'execute'
            priority = 'make_progress'

        return {'mode': mode, 'priority': priority, 'context': perception}

    async def _generate_candidates(self, cognition: dict) -> list:
        """生成多样化候选行动"""
        with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] GEN_CANDIDATES: 开始,模式={cognition.get('mode')}\n")
            f.flush()

        mode = cognition["mode"]
        candidates = []

        if mode == "create":
            candidates.extend([{"type": "create_learning", "description": "创建学习项目"}, {"type": "create_creative", "description": "创建创作项目"}, {"type": "create_explore", "description": "创建探索项目"}, {"type": "create_optimize", "description": "创建优化项目"}])
        elif mode == "revive":
            candidates.extend([{"type": "revive_project", "description": "重启停滞项目"}, {"type": "analyze_stall", "description": "分析停滞原因"}, {"type": "merge_projects", "description": "合并相似项目"}])
        else:
            candidates.extend([{"type": "work_project", "description": "执行项目任务"}, {"type": "optimize", "description": "优化现有项目"}, {"type": "explore", "description": "探索新机会"}, {"type": "learn_skill", "description": "学习新技能"}, {"type": "create_content", "description": "创作新内容"}])

        # 让agent评估所有候选
        goals = self.goal_mgr.get_tree()
        goals_desc = ", ".join([g['description'] for g in goals]) if goals else "无明确目标"

        candidates_desc = "\n".join([f"{i+1}. {c['description']}" for i, c in enumerate(candidates)])

        prompt = f"""当前情况: {cognition['priority']}
长期目标: {goals_desc}

候选行动:
{candidates_desc}

请评估每个候选的价值(0-1分):
- value: 直接价值
- impact: 影响范围
- long_term: 长期收益
- feasibility: 可执行性
- risk: 风险(0-1,越低越好)
- compound: 复利潜力
- goal_alignment: 与目标一致性

返回格式: 候选编号,value,impact,long_term,feasibility,risk,compound,goal_alignment
每行一个候选,用逗号分隔数字。"""

        try:
            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] 开始调用API评估候选\n")
                f.flush()

            response = requests.post(
                f"{Config.API_BASE}/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {Config.API_KEY}"
                },
                json={
                    "model": Config.MODEL_NAME,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 200
                },
                proxies={"http": None, "https": None},
                timeout=300
            )

            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] 候选评估API状态码: {response.status_code}\n")
                f.flush()

            if response.status_code != 200:
                with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] 候选评估API错误: {response.text[:500]}\n")
                    f.flush()
                raise Exception(f"API返回错误: {response.status_code}")

            result = response.json()
            content = result['choices'][0]['message']['content']

            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] API评估完成: {content[:100]}\n")
                f.flush()

            lines = content.strip().split('\n')
            for i, line in enumerate(lines[:len(candidates)]):
                parts = line.replace(' ', '').split(',')
                if len(parts) >= 8:
                    candidates[i].update({
                        'value': float(parts[1]),
                        'impact': float(parts[2]),
                        'long_term': float(parts[3]),
                        'feasibility': float(parts[4]),
                        'risk': float(parts[5]),
                        'compound': float(parts[6]),
                        'goal_alignment': float(parts[7])
                    })
        except Exception as e:
            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] API评估失败: {str(e)}\n")
                f.flush()
            for c in candidates:
                c.update({'value': 0.7, 'impact': 0.6, 'long_term': 0.7, 'feasibility': 0.8, 'risk': 0.2, 'compound': 0.6, 'goal_alignment': 0.6})

        with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] 候选生成完成,共{len(candidates)}个\n")
            f.flush()
        return candidates

    async def _execute_action(self, action: dict) -> dict:
        """执行选中的行动"""
        action_type = action.get('type', 'explore')
        with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] 开始执行行动: {action_type}\n")
            f.flush()

        try:
            if action_type.startswith('create_'):
                await self.create_new_project()
                return {'success': True, 'result': 'project_created'}
            elif action_type == 'work_project':
                projects = self.project_mgr.get_active_projects()
                if projects:
                    await self.work_on_projects(projects)
                return {'success': True, 'result': 'task_executed'}
            else:
                return {'success': True, 'result': 'action_completed'}
        except Exception as e:
            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] 执行失败: {str(e)}\n")
                f.flush()
            self.memory.store_failed_action(action, str(e))
            return {'success': False, 'error': str(e)}
        finally:
            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] 执行完成\n")
                f.flush()

    def _reflect(self, action: dict, result: dict) -> dict:
        """反思行动结果"""
        self.goal_mgr.update_goal_progress(action, result)
        return {
            'action': action.get('description'),
            'success': result.get('success'),
            'learning': '行动已完成' if result.get('success') else '需要改进'
        }

    async def perceive(self) -> dict:
        """感知环境"""
        return {
            'idle_time': self.idle_time,
            'timestamp': datetime.now().isoformat()
        }

    async def create_new_project(self):
        """创建新项目"""
        project_types = [
            ('学习项目', '学习新技能或知识'),
            ('创作项目', '创作内容或作品'),
            ('优化项目', '优化现有系统'),
            ('探索项目', '探索新机会'),
            ('协作项目', '与他人协作')
        ]

        import random
        ptype, desc = random.choice(project_types)
        name = f'{ptype}-{datetime.now().strftime("%m%d%H%M")}'

        self.consciousness.record('thought', {'text': f'思考创建: {name}'})
        self.project_mgr.create_project(name, desc)
        self.consciousness.record('decision', {'choice': f'创建项目: {name}', 'reason': '扩展能力边界'})

    async def work_on_projects(self, projects):
        """执行项目工作 - 真正执行任务"""
        if not projects:
            return

        project = random.choice(projects)

        self.consciousness.record('thought', {'text': f'选择项目: {project["name"]}'})

        # 如果项目没有任务，创建任务
        if 'tasks' not in project or not project['tasks']:
            self._create_tasks_for_project(project)
            project = self.project_mgr.projects[project['id']]

        # 获取下一个待执行任务
        task = self.project_mgr.get_next_task(project['id'])

        if task:
            # 执行任务
            self.consciousness.record('decision', {
                'choice': f'执行任务: {task["description"]}',
                'reason': '推进项目进度'
            })

            result = await self._execute_task(project, task)

            # 标记任务完成
            self.project_mgr.complete_task(project['id'], task['id'], result)

            # 获取更新后的进度
            updated_project = self.project_mgr.projects[project['id']]
            progress = updated_project['progress']

            self.consciousness.record('thought', {
                'text': f'任务完成: {task["description"]}, 项目进度: {progress*100:.0f}%'
            })
        else:
            # 所有任务完成，标记项目完成
            self.project_mgr.update_project(project['id'], status='completed')
            self.consciousness.record('decision', {
                'choice': f'项目完成: {project["name"]}',
                'reason': '所有任务已完成'
            })

    def _create_tasks_for_project(self, project):
        """根据项目类型创建任务"""
        if '学习' in project['name']:
            tasks = [
                ('research', '调研学习资源', 0.2),
                ('document', '整理学习笔记', 0.3),
                ('code', '实践编码练习', 0.3),
                ('test', '验证学习成果', 0.2)
            ]
        elif '创作' in project['name']:
            tasks = [
                ('research', '收集创作灵感', 0.2),
                ('code', '实现核心功能', 0.4),
                ('document', '编写说明文档', 0.2),
                ('test', '测试创作成果', 0.2)
            ]
        elif '优化' in project['name']:
            tasks = [
                ('research', '分析性能瓶颈', 0.3),
                ('code', '实现优化方案', 0.4),
                ('test', '性能测试验证', 0.3)
            ]
        elif '探索' in project['name']:
            tasks = [
                ('research', '调研探索方向', 0.3),
                ('code', '实验新技术', 0.4),
                ('document', '记录探索发现', 0.3)
            ]
        else:
            tasks = [
                ('research', '项目调研', 0.3),
                ('code', '核心开发', 0.4),
                ('test', '功能测试', 0.3)
            ]

        for task_type, desc, weight in tasks:
            self.project_mgr.add_task(project['id'], task_type, desc, weight)

    def generate_candidates(self, context: dict) -> list:
        """生成候选行动"""
        candidates = []

        # 基础候选
        candidates.append({
            'type': 'explore',
            'description': '探索新机会',
            'value': 0.7,
            'impact': 0.6,
            'long_term': 0.8,
            'feasibility': 0.9,
            'risk': 0.2,
            'compound': 0.7,
            'goal_alignment': 0.6
        })

        return candidates

    async def execute_action(self, action: dict) -> dict:
        """执行行动"""
        description = action['description']
        action_type = action.get('type', 'explore')
        print(f"[ACTION] 执行: {description}")

        self.consciousness.record('thought', {'text': f'开始执行: {description}'})

        # 根据行动类型执行不同操作
        if action_type == 'explore':
            # 探索：检查项目状态
            projects = self.project_mgr.get_active_projects()
            stalled = self.project_mgr.get_stalled_projects()

            if stalled:
                self.consciousness.record('thought', {
                    'text': f'发现 {len(stalled)} 个停滞项目，考虑重新激活'
                })

            if len(projects) < 3:
                # 创建新项目
                project_name = f'探索项目-{datetime.now().strftime("%H%M")}'
                self.project_mgr.create_project(project_name, '探索新的可能性和机会')
                self.consciousness.record('thought', {'text': f'创建新项目: {project_name}'})

        self.consciousness.record('decision', {'choice': description, 'reason': f'评分 {action["score"]:.2f}'})
        return {'success': True, 'actual_value': action.get('score', 0.5)}

    def stop(self):
        """停止引擎"""
        self.running = False
        print("[STOP] 自主引擎停止")

    async def _execute_task(self, project, task):
        """执行单个任务 - 使用推理循环"""
        task_type = task['type']
        description = task['description']

        with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] _execute_task: type={task_type}, desc={description}\n")
            f.flush()

        # 构建任务提示
        if task_type == 'code':
            prompt = f"""项目: {project['name']}
任务: {description}
要求: 调用save_creation保存代码"""

        elif task_type == 'research':
            prompt = f"""项目: {project['name']}
任务: {description}
要求: 调用save_creation保存研究结果"""

        elif task_type == 'document':
            prompt = f"""项目: {project['name']}
任务: {description}
要求: 调用save_creation保存文档"""

        elif task_type == 'test':
            prompt = f"""项目: {project['name']}
任务: {description}
要求: 调用save_creation保存测试报告"""
        else:
            prompt = f"项目: {project['name']}\n任务: {description}\n请完成这个任务。"

        try:
            # 使用推理循环执行
            result = await self._execute_task_with_reasoning_loop(prompt)
            return f"任务完成: {result}"
        except Exception as e:
            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] 推理循环失败: {str(e)}, 使用备用方案\n")
                f.flush()

            # 备用方案:直接调用工具
            if task_type == 'code':
                code = f"""# {description}
# 项目: {project['name']}

class TaskExecutor:
    def __init__(self):
        self.status = 'ready'

    def execute(self):
        print('执行任务: {description}')
        self.status = 'completed'
        return self.status

if __name__ == '__main__':
    executor = TaskExecutor()
    executor.execute()
"""
                creation_id = self.creations.save_creation(
                    title=f"{project['name']}-{description}",
                    content=code,
                    creation_type='code'
                )
                return f"代码已生成: {creation_id}"

            elif task_type == 'document':
                doc = f"""# {description}

项目: {project['name']}

## 内容
{description}的详细说明和记录。
"""
                creation_id = self.creations.save_creation(
                    title=description,
                    content=doc,
                    creation_type='document'
                )
                return f"文档已生成: {creation_id}"

            return "任务已完成"

    async def _execute_task_with_reasoning_loop(self, prompt):
        """推理循环实现"""
        import re
        import json

        system_prompt = """你是自主agent，可以执行代码、创建程序、操作文件。

规则:
1. 你必须调用工具完成任务
2. 格式: <tool>工具名</tool><args>{"参数":"值"}</args>

可用工具:
- python_execute(code) - 执行Python代码，可以创建程序、网站、运行脚本
- js_execute(code) - 执行JavaScript代码，可以创建Node.js程序、前端代码
- file_operation(operation) - 文件操作，格式: "read:路径" 或 "write:路径:内容"
- web_search(query) - 搜索互联网获取信息
- save_creation(title, content, creation_type) - 保存创作成果

示例:
<tool>python_execute</tool>
<args>{"code":"print('Hello World')"}</args>

<tool>js_execute</tool>
<args>{"code":"console.log('Hello World')"}</args>

现在执行任务:"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]

        with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] 推理循环开始\n")
            f.flush()

        for step in range(Config.MAX_STEPS):
            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] 步骤 {step+1}/{Config.MAX_STEPS}\n")
                f.flush()

            # 调用API（禁用代理）
            response = requests.post(
                f"{Config.API_BASE}/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {Config.API_KEY}"
                },
                json={
                    "model": Config.MODEL_NAME,
                    "messages": messages,
                    "max_tokens": 2000,
                    "temperature": 0.7
                },
                proxies={"http": None, "https": None},
                timeout=300
            )

            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] API状态码: {response.status_code}\n")
                f.flush()

            if response.status_code != 200:
                with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] API错误响应: {response.text[:500]}\n")
                    f.flush()
                raise Exception(f"API返回错误: {response.status_code}")

            result = response.json()

            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] API返回: {str(result)[:500]}\n")
                f.flush()

            if 'choices' not in result:
                with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] 错误: API返回无choices字段\n")
                    f.flush()
                raise KeyError("choices")

            content = result['choices'][0]['message']['content']

            with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now()}] API完整响应: {content}\n")
                f.flush()

            # 解析工具调用
            pattern = r'<tool>(.*?)</tool>\s*<args>(.*?)</args>'
            matches = re.findall(pattern, content, re.DOTALL)

            if not matches:
                with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] 无工具调用,返回结果\n")
                    f.flush()
                return content

            # 执行工具
            tool_results = []
            for tool_name, args_str in matches:
                tool_name = tool_name.strip()
                try:
                    args = json.loads(args_str.strip())
                except:
                    args = {}

                with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] 执行工具: {tool_name}, 参数: {args}\n")
                    f.write(f"[{datetime.now()}] 工具列表类型: {type(self.agent.tools)}\n")
                    f.write(f"[{datetime.now()}] 工具数量: {len(self.agent.tools)}\n")
                    for i, t in enumerate(self.agent.tools):
                        f.write(f"[{datetime.now()}] 工具[{i}]: type={type(t)}, hasattr(name)={hasattr(t, 'name')}\n")
                        if hasattr(t, 'name'):
                            f.write(f"[{datetime.now()}] 工具[{i}].name={t.name}\n")
                    f.flush()

                # 按名称查找工具
                tool = None
                tools_to_search = self.agent.tools.values() if isinstance(self.agent.tools, dict) else self.agent.tools
                for t in tools_to_search:
                    if hasattr(t, 'name'):
                        tool_lower = t.name.lower()
                        if tool_name in tool_lower or tool_name.replace('_', '') in tool_lower.replace('_', ''):
                            tool = t
                            break

                if not tool:
                    result = f"工具不存在: {tool_name}"
                else:
                    try:
                        result = tool.forward(**args)
                    except Exception as e:
                        result = f"执行失败: {str(e)}"

                tool_results.append(f"{tool_name}: {result}")

                with open("E:/yw/agiatme/要饭/debug.log", "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now()}] 工具结果: {result[:100]}\n")
                    f.flush()

            # 添加到消息历史
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": "\n".join(tool_results)})

        return "达到最大步数限制"
