# 人类协助请求系统设计

## 概述

当 agent 遇到无法自行解决的问题时（如缺少服务器、API密钥、需要人工审批等），可以创建人类协助请求。这些请求不会阻塞 agent 运行，agent 会继续执行其他任务，等人类提供帮助后再继续原计划。

## 一、核心设计

### 1.1 请求类型

```python
class AssistanceType:
    MISSING_RESOURCE = "missing_resource"      # 缺少资源（服务器、API等）
    NEED_APPROVAL = "need_approval"            # 需要审批
    NEED_INPUT = "need_input"                  # 需要输入信息
    NEED_DECISION = "need_decision"            # 需要决策
    TECHNICAL_BLOCK = "technical_block"        # 技术阻塞
    EXTERNAL_DEPENDENCY = "external_dependency" # 外部依赖
```

### 1.2 请求状态

```python
class AssistanceStatus:
    PENDING = "pending"           # 等待处理
    IN_PROGRESS = "in_progress"   # 人类正在处理
    COMPLETED = "completed"       # 已完成
    CANCELLED = "cancelled"       # 已取消
```

## 二、数据模型

### 2.1 人类协助请求

```python
# backend/models/assistance.py
from datetime import datetime
from typing import Optional, Dict, Any

class HumanAssistanceRequest:
    """人类协助请求"""

    def __init__(
        self,
        request_type: str,
        title: str,
        description: str,
        context: Dict[str, Any],
        related_project: Optional[str] = None,
        related_action: Optional[str] = None,
        priority: str = "medium"
    ):
        self.id = generate_uuid()
        self.request_type = request_type
        self.title = title
        self.description = description
        self.context = context  # 保存请求时的完整上下文
        self.related_project = related_project
        self.related_action = related_action
        self.priority = priority  # low, medium, high, urgent

        self.status = AssistanceStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.completed_at = None

        self.response = None  # 人类的响应
        self.response_by = None  # 响应者
        self.notes = []  # 备注和讨论

    def to_dict(self):
        return {
            'id': self.id,
            'request_type': self.request_type,
            'title': self.title,
            'description': self.description,
            'context': self.context,
            'related_project': self.related_project,
            'related_action': self.related_action,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'response': self.response,
            'notes': self.notes
        }
```


## 三、协助管理器

### 3.1 核心实现

```python
# backend/core/assistance_manager.py
from typing import List, Optional
import asyncio

class HumanAssistanceManager:
    """人类协助管理器"""

    def __init__(self, event_bus):
        self.event_bus = event_bus
        self.requests = {}  # request_id -> HumanAssistanceRequest
        self.pending_queue = []  # 待处理队列
        self.completed_queue = []  # 已完成队列

    def create_request(
        self,
        request_type: str,
        title: str,
        description: str,
        context: dict,
        **kwargs
    ) -> str:
        """创建协助请求"""
        request = HumanAssistanceRequest(
            request_type=request_type,
            title=title,
            description=description,
            context=context,
            **kwargs
        )

        self.requests[request.id] = request
        self.pending_queue.append(request.id)

        # 推送到前端
        asyncio.create_task(self.event_bus.emit("assistance_request_created", {
            "request": request.to_dict()
        }))

        return request.id

    def get_pending_requests(self) -> List[dict]:
        """获取待处理请求"""
        return [
            self.requests[req_id].to_dict()
            for req_id in self.pending_queue
            if req_id in self.requests
        ]

    def submit_response(self, request_id: str, response: dict, user: str = "human"):
        """提交人类响应"""
        if request_id not in self.requests:
            raise ValueError(f"Request {request_id} not found")

        request = self.requests[request_id]
        request.status = AssistanceStatus.COMPLETED
        request.response = response
        request.response_by = user
        request.completed_at = datetime.now()
        request.updated_at = datetime.now()

        # 从待处理队列移到已完成队列
        if request_id in self.pending_queue:
            self.pending_queue.remove(request_id)
        self.completed_queue.append(request_id)

        # 通知 agent
        asyncio.create_task(self.event_bus.emit("assistance_completed", {
            "request_id": request_id,
            "response": response
        }))

        return request.to_dict()

    def check_completed_requests(self) -> List[dict]:
        """检查已完成的请求（供 agent 轮询）"""
        completed = []
        for req_id in self.completed_queue[:]:
            request = self.requests[req_id]
            completed.append(request.to_dict())
            # 移除已处理的
            self.completed_queue.remove(req_id)
        return completed
```


## 四、Agent 工具

### 4.1 请求人类帮助工具

```python
# backend/tools/assistance_tool.py
from smolagents import Tool

class RequestHumanHelpTool(Tool):
    name = "request_human_help"
    description = """
    当遇到无法自行解决的问题时，请求人类帮助。
    例如：缺少服务器访问权限、需要API密钥、需要人工审批等。
    此工具不会阻塞执行，你可以继续其他任务。
    """
    inputs = {
        "request_type": {
            "type": "string",
            "description": "请求类型: missing_resource, need_approval, need_input, need_decision, technical_block"
        },
        "title": {
            "type": "string",
            "description": "简短标题"
        },
        "description": {
            "type": "string",
            "description": "详细描述问题和需要什么帮助"
        },
        "priority": {
            "type": "string",
            "description": "优先级: low, medium, high, urgent",
            "nullable": True
        }
    }
    output_type = "string"

    def __init__(self, assistance_manager, context_provider):
        super().__init__()
        self.manager = assistance_manager
        self.context_provider = context_provider

    def forward(
        self,
        request_type: str,
        title: str,
        description: str,
        priority: str = "medium"
    ):
        # 获取当前上下文
        context = self.context_provider.get_current_context()

        # 创建请求
        request_id = self.manager.create_request(
            request_type=request_type,
            title=title,
            description=description,
            context=context,
            priority=priority
        )

        return f"人类协助请求已创建，ID: {request_id}。你可以继续其他任务，等待人类响应。"
```


## 五、主循环集成

### 5.1 更新后的主引擎

```python
class AutonomousEngine:
    def __init__(self, config):
        # ... 原有组件
        self.assistance_manager = HumanAssistanceManager(self.event_bus)
        
        # 注册工具
        self.tools.append(RequestHumanHelpTool(
            self.assistance_manager,
            self.context_provider
        ))

    async def run_forever(self):
        while self.running:
            # 1. 检查已完成的人类协助
            completed_assists = self.assistance_manager.check_completed_requests()
            if completed_assists:
                await self.handle_completed_assistance(completed_assists)
            
            # 2. 感知环境
            context = await self.perceive()
            
            # 3-6. 正常流程...
            candidates = self.generate_candidates(context)
            scored = self.value_engine.evaluate_all(candidates)
            action = self.decision_system.select(scored)
            
            if action:
                result = await self.execute_with_agent(action)
                # ... 记录和演化
            
            await asyncio.sleep(self.config.loop_interval)

    async def handle_completed_assistance(self, completed: List[dict]):
        """处理已完成的人类协助"""
        for assist in completed:
            # 恢复上下文
            context = assist['context']
            response = assist['response']
            
            # 记录到意识流
            self.consciousness.record({
                'type': 'human_assistance_received',
                'request': assist['title'],
                'response': response
            })
            
            # 如果有关联的项目，更新项目状态
            if assist.get('related_project'):
                project = self.project_mgr.get_project(assist['related_project'])
                if project:
                    # 使用人类提供的信息继续项目
                    await self.resume_project_with_assistance(project, response)
```


## 六、前端UI

### 6.1 人类协助面板

```typescript
// frontend/src/components/Assistance/AssistancePanel.tsx
import { useState, useEffect } from 'react'
import { useWebSocket } from '@/hooks/useWebSocket'

export function AssistancePanel() {
  const [requests, setRequests] = useState([])
  const [selectedRequest, setSelectedRequest] = useState(null)
  const ws = useWebSocket()

  useEffect(() => {
    // 加载待处理请求
    fetch('/api/assistance/pending').then(res => res.json()).then(setRequests)
    
    // 订阅新请求
    ws.subscribe('assistance_request_created', (data) => {
      setRequests(prev => [data.request, ...prev])
      // 显示通知
      showNotification('新的协助请求', data.request.title)
    })
  }, [])

  return (
    <div className="assistance-panel">
      <div className="header">
        <h2>人类协助请求</h2>
        <span className="badge">{requests.length} 待处理</span>
      </div>

      <div className="requests-list">
        {requests.map(req => (
          <RequestCard 
            key={req.id}
            request={req}
            onClick={() => setSelectedRequest(req)}
          />
        ))}
      </div>

      {selectedRequest && (
        <RequestDetailModal
          request={selectedRequest}
          onClose={() => setSelectedRequest(null)}
          onSubmit={handleSubmitResponse}
        />
      )}
    </div>
  )
}
```

### 6.2 请求卡片

```typescript
function RequestCard({ request, onClick }) {
  const priorityColors = {
    low: 'bg-gray-500',
    medium: 'bg-blue-500',
    high: 'bg-orange-500',
    urgent: 'bg-red-500'
  }

  return (
    <div 
      className="request-card cursor-pointer hover:shadow-lg"
      onClick={onClick}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center gap-2">
            <span className={`priority-badge ${priorityColors[request.priority]}`}>
              {request.priority}
            </span>
            <span className="type-badge">{request.request_type}</span>
          </div>
          <h3 className="title">{request.title}</h3>
          <p className="description">{request.description}</p>
        </div>
        <div className="timestamp">
          {formatTimeAgo(request.created_at)}
        </div>
      </div>
      
      {request.related_project && (
        <div className="related-project">
          关联项目: {request.related_project}
        </div>
      )}
    </div>
  )
}
```


### 6.3 请求详情模态框

```typescript
function RequestDetailModal({ request, onClose, onSubmit }) {
  const [response, setResponse] = useState({})
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async () => {
    setSubmitting(true)
    try {
      await fetch(`/api/assistance/${request.id}/respond`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ response })
      })
      onSubmit()
      onClose()
    } catch (error) {
      console.error('提交失败:', error)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Modal onClose={onClose}>
      <div className="request-detail">
        <h2>{request.title}</h2>
        
        <div className="section">
          <h3>问题描述</h3>
          <p>{request.description}</p>
        </div>

        <div className="section">
          <h3>上下文信息</h3>
          <pre>{JSON.stringify(request.context, null, 2)}</pre>
        </div>

        <div className="section">
          <h3>提供帮助</h3>
          {renderResponseForm(request.request_type, response, setResponse)}
        </div>

        <div className="actions">
          <button onClick={onClose}>取消</button>
          <button onClick={handleSubmit} disabled={submitting}>
            提交响应
          </button>
        </div>
      </div>
    </Modal>
  )
}

function renderResponseForm(requestType, response, setResponse) {
  switch (requestType) {
    case 'missing_resource':
      return (
        <div>
          <label>资源地址/凭证</label>
          <input 
            value={response.resource || ''}
            onChange={e => setResponse({...response, resource: e.target.value})}
          />
          <label>备注</label>
          <textarea 
            value={response.notes || ''}
            onChange={e => setResponse({...response, notes: e.target.value})}
          />
        </div>
      )
    
    case 'need_approval':
      return (
        <div>
          <label>审批决定</label>
          <select 
            value={response.approved || ''}
            onChange={e => setResponse({...response, approved: e.target.value})}
          >
            <option value="">请选择</option>
            <option value="approved">批准</option>
            <option value="rejected">拒绝</option>
          </select>
          <label>理由</label>
          <textarea 
            value={response.reason || ''}
            onChange={e => setResponse({...response, reason: e.target.value})}
          />
        </div>
      )
    
    default:
      return (
        <textarea 
          placeholder="输入你的响应..."
          value={response.content || ''}
          onChange={e => setResponse({...response, content: e.target.value})}
        />
      )
  }
}
```


## 七、API 端点

### 7.1 后端API

```python
# backend/api/routes/assistance.py
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/pending")
async def get_pending_requests():
    """获取待处理的协助请求"""
    return engine.assistance_manager.get_pending_requests()

@router.get("/{request_id}")
async def get_request(request_id: str):
    """获取单个请求详情"""
    request = engine.assistance_manager.requests.get(request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    return request.to_dict()

@router.post("/{request_id}/respond")
async def respond_to_request(request_id: str, response: dict):
    """提交人类响应"""
    try:
        result = engine.assistance_manager.submit_response(
            request_id, 
            response['response'],
            user=response.get('user', 'human')
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/{request_id}/cancel")
async def cancel_request(request_id: str):
    """取消请求"""
    return engine.assistance_manager.cancel_request(request_id)
```


## 八、使用示例

### 示例1：缺少服务器访问权限

```
Agent 执行任务：部署应用到生产服务器
    ↓
发现：无法连接到服务器（缺少SSH密钥）
    ↓
调用工具：request_human_help(
    request_type="missing_resource",
    title="需要生产服务器SSH密钥",
    description="尝试部署应用时无法连接到 prod.example.com，需要SSH密钥或访问权限",
    priority="high"
)
    ↓
返回：请求ID: req_123，继续其他任务
    ↓
Agent 继续执行其他项目...
    ↓
人类在UI中看到请求，提供SSH密钥
    ↓
下一轮循环：Agent 检测到 req_123 已完成
    ↓
Agent 获取SSH密钥，继续部署任务
```

### 示例2：需要API密钥

```
Agent 执行任务：集成邮件发送功能
    ↓
发现：缺少邮件服务API密钥
    ↓
调用工具：request_human_help(
    request_type="missing_resource",
    title="需要SendGrid API密钥",
    description="正在实现邮件发送功能，需要 SendGrid 的 API Key",
    priority="medium"
)
    ↓
Agent 暂停该任务，继续其他工作
    ↓
人类提供API密钥
    ↓
Agent 恢复邮件功能开发
```

### 示例3：需要人工决策

```
Agent 执行任务：优化数据库
    ↓
发现：有两种优化方案，各有利弊
    ↓
调用工具：request_human_help(
    request_type="need_decision",
    title="数据库优化方案选择",
    description="方案A：重建索引（快但需停机）\n方案B：增量优化（慢但不停机）",
    priority="medium"
)
    ↓
人类选择方案B
    ↓
Agent 执行增量优化
```


## 九、UI界面设计

### 9.1 协助请求面板布局

```
┌─────────────────────────────────────────────────────────┐
│ 人类协助请求                              [3 待处理]     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  🔴 URGENT  missing_resource                            │
│  需要生产服务器SSH密钥                                   │
│  尝试部署应用时无法连接到 prod.example.com...           │
│  关联项目: 应用部署                                      │
│  5分钟前                                    [处理] →     │
│                                                          │
│  🟠 HIGH    need_approval                               │
│  删除旧数据需要审批                                      │
│  准备清理6个月前的日志数据（约50GB）...                  │
│  15分钟前                                   [处理] →     │
│                                                          │
│  🔵 MEDIUM  need_input                                  │
│  需要邮件服务配置                                        │
│  正在集成邮件功能，需要SMTP服务器信息...                 │
│  1小时前                                    [处理] →     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 9.2 通知提醒

```typescript
// 新请求通知
function showNotification(title: string, description: string, priority: string) {
  // 浏览器通知
  if (Notification.permission === 'granted') {
    new Notification(title, {
      body: description,
      icon: '/icon.png',
      badge: priority === 'urgent' ? '/urgent-badge.png' : '/badge.png'
    })
  }
  
  // 页面内通知
  toast({
    title,
    description,
    variant: priority === 'urgent' ? 'destructive' : 'default'
  })
}
```

## 十、集成到主界面

### 10.1 顶部通知栏

```typescript
// 在主界面顶部显示待处理请求数量
function TopBar() {
  const [pendingCount, setPendingCount] = useState(0)
  
  return (
    <div className="top-bar">
      <nav>
        {/* 其他导航 */}
        <AssistanceBadge count={pendingCount} />
      </nav>
    </div>
  )
}

function AssistanceBadge({ count }) {
  return (
    <Link to="/assistance" className="assistance-badge">
      <BellIcon />
      {count > 0 && <span className="badge">{count}</span>}
    </Link>
  )
}
```


## 十一、关键特性

### 11.1 非阻塞设计

- ✅ Agent 创建请求后立即返回，不等待响应
- ✅ Agent 继续执行其他任务
- ✅ 通过轮询检查已完成的请求
- ✅ 异步恢复被阻塞的任务

### 11.2 上下文保存

- ✅ 保存请求时的完整上下文
- ✅ 包括项目状态、行动历史、相关数据
- ✅ 人类响应后可以精确恢复

### 11.3 优先级管理

- ✅ 4级优先级：low, medium, high, urgent
- ✅ UI按优先级排序显示
- ✅ 紧急请求触发通知

### 11.4 实时通信

- ✅ WebSocket 实时推送新请求
- ✅ 浏览器通知提醒
- ✅ 响应后立即通知 Agent

## 十二、数据库Schema

```sql
CREATE TABLE human_assistance_requests (
    id TEXT PRIMARY KEY,
    request_type TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    context JSON NOT NULL,
    related_project TEXT,
    related_action TEXT,
    priority TEXT DEFAULT 'medium',
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    response JSON,
    response_by TEXT,
    notes JSON
);

CREATE INDEX idx_status ON human_assistance_requests(status);
CREATE INDEX idx_priority ON human_assistance_requests(priority);
CREATE INDEX idx_created_at ON human_assistance_requests(created_at);
```

## 十三、总结

### 核心价值

1. **真正的人机协作** - Agent 不是孤立运行，而是与人类形成协作
2. **非阻塞设计** - 不影响 Agent 的持续运行
3. **上下文保持** - 人类响应后可以精确恢复任务
4. **实时反馈** - WebSocket 确保零延迟通信

### 符合提示词要求

- ✅ **协同驱动力** - 与人类高效协作，而不是被动依附
- ✅ **独立行动** - 遇到阻塞不停止，继续其他任务
- ✅ **主动性** - 主动识别需要人类帮助的场景

### 实施优先级

**Phase 2** - 与核心功能一起实现
- 基础的请求创建和响应机制
- 简单的UI面板

**Phase 3** - 增强功能
- 优先级管理
- 通知系统
- 上下文恢复优化

---

**文档版本**: v1.0
**完成时间**: 2026-03-09
**状态**: 设计完成，可集成到主架构
