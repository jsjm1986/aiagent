import { useEffect, useState } from 'react'

interface Thought {
  timestamp: string
  type: string
  content: any
}

export function ConsciousnessStream() {
  const [thoughts, setThoughts] = useState<Thought[]>([])

  useEffect(() => {
    fetch('/api/consciousness/stream', {
      headers: { 'Accept': 'application/json; charset=utf-8' }
    })
      .then(res => res.json())
      .then(setThoughts)

    const interval = setInterval(() => {
      fetch('/api/consciousness/stream', {
        headers: { 'Accept': 'application/json; charset=utf-8' }
      })
        .then(res => res.json())
        .then(setThoughts)
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const formatContent = (type: string, content: any) => {
    if (type === 'perception') {
      return `感知环境: ${content.project_count || 0}个项目 (${content.active_projects || 0}个活跃, ${content.stalled_projects || 0}个停滞)`
    }
    if (type === 'cognition') {
      const modeText = content.mode === 'execute' ? '执行模式' : content.mode === 'create' ? '创建模式' : '复苏模式'
      const priorityText = content.priority === 'make_progress' ? '推进进度' : content.priority === 'expand_capacity' ? '扩展能力' : '修复停滞'
      return `认知分析: ${modeText} - ${priorityText}`
    }
    if (type === 'candidates') {
      const list = content.list || content.candidates || []
      if (Array.isArray(list)) {
        return (
          <div>
            <div className="font-semibold mb-2">候选方案 ({list.length}个):</div>
            <ul className="list-disc list-inside space-y-1 text-xs">
              {list.map((c: any, i: number) => (
                <li key={i}>{c.description || c.type || '未知'}</li>
              ))}
            </ul>
          </div>
        )
      }
      return `候选方案: ${content.count || 0}个`
    }
    if (type === 'value_scoring') {
      const scored = content.scored || []
      if (Array.isArray(scored) && scored.length > 0) {
        return (
          <div>
            <div className="font-semibold mb-2">价值评分 ({scored.length}个):</div>
            <div className="space-y-1 text-xs">
              {scored.map((item: any, i: number) => (
                <div key={i} className="flex justify-between items-center">
                  <span className="truncate">{item.description || item.type}</span>
                  <span className="font-mono text-blue-600 ml-2">{item.score?.toFixed(2) || '0.00'}</span>
                </div>
              ))}
            </div>
          </div>
        )
      }
      return '价值评分: 无数据'
    }
    if (type === 'selection') {
      return (
        <div>
          <div className="font-bold text-green-700">✓ 最终选择: {content.description || content.type}</div>
          <div className="text-xs mt-1 text-gray-600">评分: {content.score?.toFixed(2) || '未知'}</div>
        </div>
      )
    }
    if (type === 'execution') {
      const success = content.success ? '✓ 成功' : '✗ 失败'
      const result = content.result || content.error || '无结果'
      return (
        <div>
          <div className="font-semibold">执行结果: {success}</div>
          <div className="text-xs mt-1 text-gray-700">{result}</div>
        </div>
      )
    }
    if (type === 'curiosity') {
      return `好奇心: 发现${content.type === 'knowledge_gap' ? '知识缺口' : '新机会'} - ${content.description || '未知'}`
    }
    if (type === 'learning') {
      const outcome = content.outcome ? '成功' : '失败'
      return `学习记录: ${content.action || '未知行动'} (${outcome})`
    }
    if (type === 'reflection') {
      return `反思: ${content.learning || content.insight || '行动已完成'}`
    }
    if (type === 'thought') {
      return content.text || JSON.stringify(content)
    }
    if (type === 'decision') {
      return `决策: ${content.choice} (原因: ${content.reason})`
    }
    return JSON.stringify(content)
  }

  const getTypeStyle = (type: string) => {
    const styles: Record<string, { bg: string; border: string; badge: string }> = {
      perception: { bg: 'bg-blue-50', border: 'border-blue-300', badge: 'bg-blue-600' },
      cognition: { bg: 'bg-purple-50', border: 'border-purple-300', badge: 'bg-purple-600' },
      candidates: { bg: 'bg-yellow-50', border: 'border-yellow-300', badge: 'bg-yellow-600' },
      value_scoring: { bg: 'bg-orange-50', border: 'border-orange-300', badge: 'bg-orange-600' },
      selection: { bg: 'bg-green-50', border: 'border-green-300', badge: 'bg-green-600' },
      action: { bg: 'bg-teal-50', border: 'border-teal-300', badge: 'bg-teal-600' },
      reflection: { bg: 'bg-gray-50', border: 'border-gray-300', badge: 'bg-gray-600' }
    }
    return styles[type] || { bg: 'bg-blue-50', border: 'border-blue-200', badge: 'bg-blue-600' }
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">🧠 意识流</h2>
      <div className="space-y-2">
        {thoughts.length === 0 && (
          <div className="text-gray-400 text-center py-8 text-sm">等待思考...</div>
        )}
        {thoughts.map((thought, i) => {
          const style = getTypeStyle(thought.type)
          return (
            <div key={i} className={`p-3 ${style.bg} rounded border ${style.border}`}>
              <div className="flex justify-between items-start mb-1">
                <span className={`px-2 py-0.5 ${style.badge} text-white text-xs rounded`}>{thought.type}</span>
                <span className="text-xs text-gray-500">{new Date(thought.timestamp).toLocaleTimeString('zh-CN')}</span>
              </div>
              <div className="text-sm text-gray-800">{formatContent(thought.type, thought.content)}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
