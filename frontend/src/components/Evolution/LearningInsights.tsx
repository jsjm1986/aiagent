import { useEffect, useState } from 'react'

interface Insight {
  type: string
  message: string
  priority: string
}

export function LearningInsights() {
  const [insights, setInsights] = useState<Insight[]>([])

  useEffect(() => {
    fetch('/api/evolution/insights')
      .then(res => res.json())
      .then(setInsights)

    const interval = setInterval(() => {
      fetch('/api/evolution/insights')
        .then(res => res.json())
        .then(setInsights)
    }, 15000)

    return () => clearInterval(interval)
  }, [])

  const priorityColors = {
    high: 'bg-red-100 border-red-400 text-red-800',
    medium: 'bg-yellow-100 border-yellow-400 text-yellow-800',
    low: 'bg-blue-100 border-blue-400 text-blue-800',
    info: 'bg-green-100 border-green-400 text-green-800'
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">学习洞察</h2>
      <div className="space-y-3">
        {insights.map((insight, i) => (
          <div
            key={i}
            className={`p-4 rounded-lg border-2 ${priorityColors[insight.priority as keyof typeof priorityColors]}`}
          >
            <div className="flex items-start gap-2">
              <span className="text-xl">💡</span>
              <div>
                <span className="text-xs font-semibold uppercase">{insight.type}</span>
                <p className="mt-1">{insight.message}</p>
              </div>
            </div>
          </div>
        ))}
        {insights.length === 0 && (
          <p className="text-gray-500 text-center py-8">暂无学习洞察</p>
        )}
      </div>
    </div>
  )
}
