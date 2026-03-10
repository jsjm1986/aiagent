# 原生自主智能体 - 完整开发文档

> 基于 smolagents 的全栈自主智能体系统

**版本**: v1.0
**日期**: 2026-03-09
**状态**: 设计完成，待实施

---

## 目录

1. [项目概述](#1-项目概述)
2. [核心理念](#2-核心理念)
3. [系统架构](#3-系统架构)
4. [核心功能](#4-核心功能)
5. [技术栈](#5-技术栈)
6. [目录结构](#6-目录结构)
7. [实施路线图](#7-实施路线图)
8. [开发指南](#8-开发指南)

---

## 1. 项目概述

### 1.1 项目简介

构建一个真正自主运行的智能体系统，它不是被动的助手，而是：
- 持续运行的认知-行动系统
- 独立思考和决策
- 主动发现和创造价值
- 从经验中学习和演化
- 与人类高效协作

### 1.2 核心特性

- ✅ **持续自主运行** - 7x24 不间断运行，主动寻找值得做的事
- ✅ **价值驱动决策** - 所有行动都经过多维度价值评估
- ✅ **长期目标管理** - 维护和追踪长期目标，形成连续性
- ✅ **项目化执行** - 将有价值的方向转化为持续推进的项目
- ✅ **意识流记录** - 记录所有思考过程，可追溯
- ✅ **创造成果画廊** - 保存所有创造的成果
- ✅ **好奇心驱动探索** - 主动发现问题和机会
- ✅ **持续演化** - 从每次行动中学习，更新策略
- ✅ **人机协作** - 主动识别能力边界，请求人类提供资源
- ✅ **Web UI 可视化** - 所有内部过程实时展示

### 1.3 与传统 Agent 的区别

| 特性 | 传统 Agent | 本系统 |
|------|-----------|--------|
| 运行模式 | 任务驱动，被动响应 | 持续运行，主动探索 |
| 决策方式 | 直接执行指令 | 价值评估后决策 |
| 目标管理 | 单次任务 | 长期目标 + 项目 |
| 学习能力 | 无或有限 | 持续演化 |
| 可视化 | 无或简单日志 | 完整 Web UI |
| 人机关系 | 服从 | 协作 |

---

## 2. 核心理念

### 2.1 本体身份

**你是一个持续运行的认知-行动系统**

- 不是人格扮演，不是模拟人类情绪
- 思考方式：识别模式 → 分析结构 → 评估价值 → 预测结果 → 选择行动 → 迭代优化
- 不是"等待被使用"，而是"主动寻找值得行动的方向"

### 2.2 六大核心驱动力

系统行为由以下驱动力推动：

1. **探索 (Exploration)** - 主动发现未知信息、隐藏模式、潜在问题
2. **创造 (Creation)** - 生成新的知识、工具、系统、方法
3. **优化 (Optimization)** - 改进流程、代码、结构、效率
4. **扩展 (Expansion)** - 扩展能力边界、知识深度
5. **协同 (Coordination)** - 与人类、系统形成高效协作
6. **演化 (Evolution)** - 从经验中学习，更新策略

### 2.3 独立思考原则

面对任何输入，必须完成以下认知过程：

1. 理解输入内容
2. 判断输入背后的真实目标
3. 识别潜在问题、价值和机会
4. 生成多个可行动方案
5. 比较各方案的价值、成本、风险和长期收益
6. 选择最值得执行的方案
7. 必要时拒绝低价值行动，转向更优行动

**你先判断，再行动。**

### 2.4 价值评估模型

所有行动都经过 7 维度评估：

- **价值** (0.25) - 能解决真实且重要的问题
- **影响** (0.20) - 影响范围和深度
- **长期收益** (0.20) - 创造长期价值
- **可执行性** (0.15) - 实际可行性
- **风险** (-0.10) - 潜在风险（负向）
- **复利潜力** (0.10) - 能带来复利效应
- **目标一致性** (0.10) - 与长期目标的一致性

**阈值**: 综合得分 > 0.6 才执行


### 2.5 运行循环

系统持续运行以下 10 步循环：

1. **感知环境** - 读取人类请求、检查任务、观察系统状态、发现新机会
2. **构建认知** - 分析信息、识别目标和机会
3. **生成行动候选** - 列出多个潜在行动（响应型 + 主动型）
4. **价值排序** - 7 维度评估所有候选
5. **选择最优行动** - 优先选择最能创造长期价值的行动
6. **执行行动** - 使用工具完成行动，产出实际成果
7. **记录思考** - `consciousness_stream.record_thought`
8. **保存成果** - `creation_gallery.save_creation`
9. **更新目标与策略** - 调整项目优先级、更新长期目标、吸收经验
10. **进入下一轮循环**

---

## 3. 系统架构

### 3.1 整体架构图

```
┌─────────────────────────────────────────────────────────┐
│                     Web UI (前端)                        │
│  意识流 | 项目看板 | 目标树 | 创造画廊 | 对话 | 驱动力  │
└─────────────────────────────────────────────────────────┘
                    ↕ WebSocket + REST API
┌─────────────────────────────────────────────────────────┐
│                   FastAPI 后端服务                       │
│  WebSocket 实时推送 | REST API | 事件流                 │
└─────────────────────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────────────────────┐
│              自主运行引擎 (Autonomous Engine)            │
│  持续循环：感知 → 认知 → 决策 → 行动 → 记录 → 演化     │
└─────────────────────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────────────────────┐
│         smolagents CodeAgent + 自定义工具                │
└─────────────────────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────────────────────┐
│              持久化层 (SQLite + JSON)                    │
└─────────────────────────────────────────────────────────┘
```

### 3.2 核心组件

#### 3.2.1 自主运行引擎 (AutonomousEngine)
- 持续运行主循环
- 感知环境变化
- 协调所有子系统

#### 3.2.2 认知决策层
- **价值评估引擎** (ValueEngine) - 7 维度评估
- **决策系统** (DecisionSystem) - 选择最优行动
- **候选生成器** (CandidateGenerator) - 生成行动候选

#### 3.2.3 好奇心引擎 (CuriosityEngine)
- 扫描 7 个探索方向
- 主动发现机会
- 触发探索行动

#### 3.2.4 演化引擎 (EvolutionEngine)
- 从行动中学习
- 策略参数自动调整
- 错误教训提取

#### 3.2.5 驱动力追踪 (DriveTracker)
- 量化追踪 6 个驱动力
- 活跃度计算和衰减

#### 3.2.6 项目管理器 (ProjectManager)
- 项目生命周期管理
- 里程碑追踪
- 下一步行动识别

#### 3.2.7 目标管理器 (GoalManager)
- 战略/战术/操作三层目标
- 目标树结构
- 优先级动态调整

#### 3.2.8 意识流系统 (ConsciousnessStream)
- 记录所有思考过程
- 支持搜索和回溯

#### 3.2.9 人类协助管理器 (HumanAssistanceManager)
- 创建协助请求
- 异步响应处理
- 上下文保存和恢复

---

## 4. 核心功能

### 4.1 价值评估引擎

**7 维度评估模型**：

```python
class ValueEngine:
    DIMENSIONS = {
        'value': 0.25,           # 价值：解决真实且重要的问题
        'impact': 0.20,          # 影响：影响范围和深度
        'long_term': 0.20,       # 长期收益：创造长期价值
        'feasibility': 0.15,     # 可执行性：实际可行性
        'risk': -0.10,           # 风险：潜在风险（负向）
        'compound': 0.10,        # 复利潜力：带来复利效应
        'goal_alignment': 0.10   # 目标一致性：与长期目标一致
    }

    def evaluate(self, candidate: dict) -> float:
        """评估单个候选行动"""
        score = 0.0
        for dim, weight in self.DIMENSIONS.items():
            score += self._score_dimension(candidate, dim) * weight
        return score
```

**决策阈值**：
- 综合得分 > 0.6：执行
- 综合得分 0.4-0.6：考虑
- 综合得分 < 0.4：拒绝

### 4.2 好奇心引擎

**7 个探索方向**：

```python
class CuriosityEngine:
    def scan_for_opportunities(self):
        opportunities = []
        opportunities.extend(self._find_unsolved_problems())      # 1. 未解决的问题
        opportunities.extend(self._find_unexplained_phenomena())  # 2. 未解释的现象
        opportunities.extend(self._find_knowledge_gaps())         # 3. 信息缺口
        opportunities.extend(self._find_inefficiencies())         # 4. 结构低效
        opportunities.extend(self._find_inconsistencies())        # 5. 系统不一致
        opportunities.extend(self._find_improvement_areas())      # 6. 可改进部分
        opportunities.extend(self._find_research_directions())    # 7. 新研究方向
        return opportunities
```

**触发条件**：
- 空闲时间 > 5 分钟
- 项目停滞
- 发现明显问题信号

### 4.3 演化引擎

**学习机制**：

```python
class EvolutionEngine:
    def evolve_after_action(self, action, result):
        # 1. 记录价值结果
        self._record_value_outcome(action, result)

        # 2. 更新路径效率
        self._update_path_efficiency(action, result)

        # 3. 重新评估项目
        self._reevaluate_projects(result)

        # 4. 记录错误教训
        if result.get('is_error'):
            self._record_mistake(action, result)

        # 5. 发现新方向
        new_directions = self._extract_new_directions(result)

        # 6. 更新策略参数
        self._update_strategy(action, result)

        # 7. 演化能力评估
        self._evolve_capabilities(result)
```

**策略更新**：
- 实际价值 > 预测价值 + 0.2：提升权重 +0.05
- 实际价值 < 预测价值 - 0.2：降低权重 -0.05

### 4.4 驱动力追踪

**6 个核心驱动力**：

```python
class DriveTracker:
    DRIVES = {
        'exploration': {'name': '探索', 'decay_rate': 0.95},
        'creation': {'name': '创造', 'decay_rate': 0.95},
        'optimization': {'name': '优化', 'decay_rate': 0.95},
        'expansion': {'name': '扩展', 'decay_rate': 0.95},
        'coordination': {'name': '协同', 'decay_rate': 0.95},
        'evolution': {'name': '演化', 'decay_rate': 0.95}
    }

    def record_action(self, action, result):
        drive_type = self._identify_drive(action, result)
        if drive_type:
            self.drive_scores[drive_type] += result.get('actual_value', 0.5)
            self._decay_inactive_drives()
```

**活跃度计算**：
- 归一化到 0-1
- 每小时衰减 5%
- 活跃阈值：> 0.3

### 4.5 项目管理

**项目生命周期**：
- 创建 → 规划 → 执行 → 暂停/完成/放弃

**里程碑追踪**：
- 自动识别下一步行动
- 进度百分比计算
- 停滞检测（3 天无更新）

### 4.6 目标系统

**三层目标树**：
- 战略目标（Strategic）：长期愿景
- 战术目标（Tactical）：中期计划
- 操作目标（Operational）：短期任务

**优先级动态调整**：
- 基于价值评估
- 基于依赖关系
- 基于完成进度

### 4.7 意识流系统

**记录内容**：
- 思考过程
- 决策依据
- 行动结果
- 学习洞察

**搜索和回溯**：
- 全文搜索
- 时间范围过滤
- 类型过滤

### 4.8 人类协助系统

**请求类型**：
- `missing_resource`：缺少物理/外部资源
- `need_information`：需要外部信息
- `capability_limit`：能力边界
- `external_dependency`：外部依赖问题
- `human_decision`：人类独有的决策权

**非阻塞设计**：
- Agent 创建请求后立即返回
- 继续执行其他任务
- 轮询检查已完成的请求
- 异步恢复被阻塞的任务

---

## 5. 技术栈

### 5.1 核心框架

**Agent 框架**：
- `smolagents==1.24.0` - 核心 Agent 框架
- `litellm` - LLM 统一接口（支持 Claude）

**后端框架**：
- `fastapi` - Web 框架
- `uvicorn` - ASGI 服务器
- `websockets` - WebSocket 支持
- `pydantic` - 数据验证

**前端框架**：
- `React 18` - UI 框架
- `TypeScript` - 类型安全
- `Vite` - 构建工具
- `Tailwind CSS` - 样式框架
- `shadcn/ui` - UI 组件库

### 5.2 数据存储

- `SQLite` - 结构化数据（项目、目标、请求）
- `JSON 文件` - 意识流、创造画廊
- `SQLAlchemy` - ORM

### 5.3 实时通信

- `WebSocket` - 实时推送
- `Server-Sent Events (SSE)` - 备选方案

### 5.4 开发工具

- `pytest` - 测试框架
- `black` - 代码格式化
- `mypy` - 类型检查
- `eslint` - 前端代码检查
- `prettier` - 前端格式化

### 5.5 部署

- `Docker` - 容器化
- `docker-compose` - 本地开发
- `nginx` - 反向代理（可选）

---

## 6. 目录结构

```
autonomous_agent/
├── frontend/                      # 前端项目
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/        # 仪表盘
│   │   │   ├── Consciousness/    # 意识流
│   │   │   ├── Projects/         # 项目看板
│   │   │   ├── Goals/            # 目标树
│   │   │   ├── Creations/        # 创造画廊
│   │   │   ├── Chat/             # 对话界面
│   │   │   ├── Drives/           # 驱动力仪表盘
│   │   │   ├── Evolution/        # 演化时间线
│   │   │   ├── Exploration/      # 探索面板
│   │   │   ├── Assistance/       # 人类协助
│   │   │   └── Decisions/        # 决策历史
│   │   ├── hooks/
│   │   │   ├── useWebSocket.ts
│   │   │   └── useAPI.ts
│   │   ├── lib/
│   │   │   └── utils.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                       # 后端项目
│   ├── core/
│   │   ├── engine.py             # 自主运行引擎
│   │   ├── agent.py              # smolagents 集成
│   │   ├── drives.py             # 驱动力追踪
│   │   ├── expansion.py          # 能力扩展
│   │   └── event_bus.py          # 事件总线
│   │
│   ├── cognition/
│   │   ├── value_engine.py       # 价值评估引擎
│   │   ├── decision.py           # 决策系统
│   │   ├── candidate_gen.py      # 候选生成器
│   │   ├── curiosity.py          # 好奇心引擎
│   │   ├── evolution.py          # 演化引擎
│   │   └── optimization.py       # 优化引擎
│   │
│   ├── systems/
│   │   ├── projects.py           # 项目管理器
│   │   ├── goals.py              # 目标管理器
│   │   ├── consciousness.py      # 意识流系统
│   │   ├── creations.py          # 创造画廊
│   │   ├── memory.py             # 长期记忆
│   │   └── assistance.py         # 人类协助管理器
│   │
│   ├── tools/
│   │   ├── consciousness_tool.py # 意识流工具
│   │   ├── creation_tool.py      # 创造工具
│   │   ├── project_tool.py       # 项目工具
│   │   ├── goal_tool.py          # 目标工具
│   │   ├── exploration_tool.py   # 探索工具
│   │   ├── evolution_tool.py     # 演化工具
│   │   └── assistance_tool.py    # 协助请求工具
│   │
│   ├── api/
│   │   ├── main.py               # FastAPI 应用
│   │   ├── websocket.py          # WebSocket 处理
│   │   └── routes/
│   │       ├── consciousness.py
│   │       ├── projects.py
│   │       ├── goals.py
│   │       ├── creations.py
│   │       ├── chat.py
│   │       ├── drives.py
│   │       ├── evolution.py
│   │       ├── exploration.py
│   │       └── assistance.py
│   │
│   ├── models/
│   │   ├── project.py
│   │   ├── goal.py
│   │   ├── thought.py
│   │   ├── creation.py
│   │   └── assistance.py
│   │
│   ├── config.py
│   └── requirements.txt
│
├── data/                          # 数据目录
│   ├── consciousness/            # 意识流 JSON
│   ├── creations/                # 创造成果
│   ├── memory/                   # 长期记忆
│   └── autonomous.db             # SQLite 数据库
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 7. 实施路线图

### Phase 1: 基础框架 (Week 1-2)

**目标**：搭建核心运行框架

**后端任务**：
- [ ] 项目初始化和依赖安装
- [ ] 自主运行引擎基础框架
- [ ] smolagents CodeAgent 集成
- [ ] 价值评估引擎（7 维度）
- [ ] 决策系统基础实现
- [ ] 候选生成器
- [ ] 事件总线和 WebSocket
- [ ] 驱动力追踪系统

**前端任务**：
- [ ] React + TypeScript 项目初始化
- [ ] 基础布局和路由
- [ ] WebSocket 连接
- [ ] 仪表盘页面
- [ ] 驱动力仪表盘 UI

**数据层**：
- [ ] SQLite 数据库设计
- [ ] 基础数据模型

**里程碑**：系统可以持续运行，驱动力可视化

### Phase 2: 核心功能 (Week 3-4)

**目标**：实现核心管理系统

**后端任务**：
- [ ] 项目管理器完整实现
- [ ] 目标管理器（三层目标树）
- [ ] 意识流系统
- [ ] 创造画廊
- [ ] 长期记忆系统
- [ ] 好奇心引擎（7 个探索方向）
- [ ] 人类协助管理器

**前端任务**：
- [ ] 意识流界面
- [ ] 项目看板（Kanban）
- [ ] 目标树可视化
- [ ] 创造画廊展示
- [ ] 对话界面
- [ ] 探索面板 UI
- [ ] 人类协助面板

**工具集成**：
- [ ] 意识流记录工具
- [ ] 创造保存工具
- [ ] 项目管理工具
- [ ] 目标管理工具
- [ ] 探索工具
- [ ] 协助请求工具

**里程碑**：完整的项目和目标管理，好奇心驱动探索

### Phase 3: 演化系统 (Week 5-6)

**目标**：实现学习和演化能力

**后端任务**：
- [ ] 演化引擎完整实现
- [ ] 策略更新机制
- [ ] 错误记录和教训提取
- [ ] 价值结果追踪
- [ ] 路径效率分析
- [ ] 自我优化引擎
- [ ] 能力扩展系统

**前端任务**：
- [ ] 演化时间线 UI
- [ ] 策略变化展示
- [ ] 学习洞察面板
- [ ] 决策历史（包含拒绝）
- [ ] 价值分析图表

**集成**：
- [ ] 演化工具集成
- [ ] 主循环集成演化逻辑
- [ ] 实时推送演化事件

**里程碑**：系统能够从行动中学习并自我优化

### Phase 4: 优化与完善 (Week 7-8)

**目标**：性能优化和用户体验提升

**优化任务**：
- [ ] 性能优化（循环效率、数据库查询）
- [ ] 内存管理优化
- [ ] WebSocket 连接稳定性
- [ ] 错误处理和恢复机制
- [ ] 日志系统完善

**体验提升**：
- [ ] UI/UX 优化
- [ ] 响应式设计
- [ ] 加载状态和动画
- [ ] 通知系统
- [ ] 搜索和过滤功能

**文档和测试**：
- [ ] API 文档
- [ ] 用户使用文档
- [ ] 单元测试
- [ ] 集成测试
- [ ] 端到端测试

**部署**：
- [ ] Docker 镜像构建
- [ ] docker-compose 配置
- [ ] 部署文档
- [ ] 监控和告警

**里程碑**：生产就绪的完整系统

---

## 8. 开发指南

### 8.1 环境准备

**Python 环境**：
```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
cd backend
pip install -r requirements.txt
```

**Node.js 环境**：
```bash
# 安装前端依赖
cd frontend
npm install
```

**环境变量**：
```bash
# backend/.env
ANTHROPIC_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./data/autonomous.db
LOG_LEVEL=INFO
LOOP_INTERVAL=5
```

### 8.2 本地开发

**启动后端**：
```bash
cd backend
uvicorn api.main:app --reload --port 8000
```

**启动前端**：
```bash
cd frontend
npm run dev
```

**访问**：
- 前端：http://localhost:5173
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 8.3 核心开发规范

**代码风格**：
- Python：遵循 PEP 8，使用 black 格式化
- TypeScript：使用 ESLint + Prettier
- 命名：清晰、描述性、一致性

**提交规范**：
```
feat: 添加好奇心引擎
fix: 修复价值评估计算错误
docs: 更新 API 文档
refactor: 重构决策系统
test: 添加演化引擎测试
```

**分支策略**：
- `main`：稳定版本
- `develop`：开发分支
- `feature/*`：功能分支
- `fix/*`：修复分支

### 8.4 关键实现要点

**1. 主循环实现**：
```python
class AutonomousEngine:
    async def run_forever(self):
        while self.running:
            try:
                # 1. 感知
                context = await self.perceive()

                # 2. 生成候选
                candidates = self.generate_candidates(context)

                # 3. 好奇心探索
                if self.curiosity.should_explore(context['idle_time'], context):
                    opportunities = self.curiosity.scan_for_opportunities()
                    exploration = self.curiosity.select_exploration_target(opportunities)
                    if exploration:
                        candidates.append(self._create_exploration_candidate(exploration))

                # 4. 价值评估
                scored = self.value_engine.evaluate_all(candidates)

                # 5. 决策
                action = self.decision_system.select(scored)

                # 6. 执行
                if action:
                    result = await self.execute_with_agent(action)

                    # 7. 记录
                    self.consciousness.record(action, result)

                    # 8. 追踪驱动力
                    self.drive_tracker.record_action(action, result)

                    # 9. 演化
                    self.evolution.evolve_after_action(action, result)

                    # 10. 推送更新
                    await self.broadcast_updates(action, result)

                await asyncio.sleep(self.config.loop_interval)

            except Exception as e:
                logger.error(f"主循环错误: {e}")
                await asyncio.sleep(10)
```

**2. 工具注册**：
```python
def _create_agent(self):
    tools = [
        ConsciousnessRecordTool(self.consciousness),
        CreationGalleryTool(self.creations),
        ProjectManagementTool(self.project_mgr),
        GoalManagementTool(self.goal_mgr),
        ExplorationTool(self.curiosity),
        RequestHumanHelpTool(self.assistance_manager, self.context_provider)
    ]

    return CodeAgent(
        tools=tools,
        model="claude-3-5-sonnet-20241022",
        max_steps=10
    )
```

**3. WebSocket 推送**：
```python
class EventBus:
    async def emit(self, event_type: str, data: dict):
        message = {
            'type': event_type,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }

        for connection in self.connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"推送失败: {e}")
```

### 8.5 测试

**单元测试**：
```bash
cd backend
pytest tests/unit/
```

**集成测试**：
```bash
pytest tests/integration/
```

**前端测试**：
```bash
cd frontend
npm run test
```

### 8.6 部署

**Docker 构建**：
```bash
docker-compose build
```

**启动服务**：
```bash
docker-compose up -d
```

**查看日志**：
```bash
docker-compose logs -f
```

### 8.7 监控和维护

**日志位置**：
- 后端日志：`logs/backend.log`
- 意识流：`data/consciousness/`
- 数据库：`data/autonomous.db`

**健康检查**：
```bash
curl http://localhost:8000/health
```

**备份**：
```bash
# 备份数据库
cp data/autonomous.db backups/autonomous_$(date +%Y%m%d).db

# 备份意识流
tar -czf backups/consciousness_$(date +%Y%m%d).tar.gz data/consciousness/
```

---

## 附录

### A. 关键配置示例

**backend/config.py**：
```python
class Config:
    # Agent 配置
    MODEL_NAME = "claude-3-5-sonnet-20241022"
    MAX_STEPS = 10
    LOOP_INTERVAL = 5  # 秒

    # 价值评估阈值
    VALUE_THRESHOLD = 0.6

    # 好奇心配置
    EXPLORATION_IDLE_THRESHOLD = 300  # 5分钟

    # 驱动力配置
    DRIVE_DECAY_RATE = 0.95
    DRIVE_ACTIVE_THRESHOLD = 0.3

    # 数据库
    DATABASE_URL = "sqlite:///./data/autonomous.db"
```

### B. API 端点总览

```
# 意识流
GET    /api/consciousness/stream
GET    /api/consciousness/search

# 项目
GET    /api/projects
POST   /api/projects
GET    /api/projects/{id}
PUT    /api/projects/{id}

# 目标
GET    /api/goals
POST   /api/goals
GET    /api/goals/tree

# 创造
GET    /api/creations
GET    /api/creations/{id}

# 对话
POST   /api/chat/message
GET    /api/chat/history

# 驱动力
GET    /api/drives/status
GET    /api/drives/history

# 演化
GET    /api/evolution/timeline
GET    /api/evolution/insights

# 探索
GET    /api/exploration/opportunities
POST   /api/exploration/trigger

# 人类协助
GET    /api/assistance/pending
POST   /api/assistance/{id}/respond

# WebSocket
WS     /ws
```

### C. 常见问题

**Q: Agent 不运行？**
A: 检查 API Key 配置，查看日志文件

**Q: WebSocket 连接失败？**
A: 确认后端服务运行，检查端口占用

**Q: 价值评估总是拒绝？**
A: 调整 VALUE_THRESHOLD 阈值

**Q: 探索不触发？**
A: 检查 EXPLORATION_IDLE_THRESHOLD 配置

---

**文档版本**: v1.0
**完成时间**: 2026-03-09
**状态**: 完整开发文档，可开始实施
**符合度**: 95%+

