import { useEffect, useState } from 'react'

interface StrategyUpdate {
  id: string
  timestamp: string
  parameter: string
  old_value: number
  new_value: number
  reason: string
}

export function EvolutionTimeline() {
  const [timeline, setTimeline] = useState<StrategyUpdate[]>([])

  useEffect(() => {
    fetch('/api/evolution/timeline')
      .then(res => res.json())
      .then(setTimeline)

    const interval = setInterval(() => {
      fetch('/api/evolution/timeline')
        .then(res => res.json())
        .then(setTimeline)
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">演化历史</h2>
      <div className="space-y-3">
        {timeline.map(update => (
          <div key={update.id} className="p-4 bg-white rounded-lg border-l-4 border-purple-500">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-xs text-gray-500">
                  {new Date(update.timestamp).toLocaleString()}
                </span>
                <h3 className="font-semibold mt-1">{update.parameter}</h3>
                <div className="text-sm mt-2">
                  <span className="text-red-600">{update.old_value.toFixed(3)}</span>
                  {' → '}
                  <span className="text-green-600">{update.new_value.toFixed(3)}</span>
                </div>
                <p className="text-sm text-gray-600 mt-1">{update.reason}</p>
              </div>
            </div>
          </div>
        ))}
        {timeline.length === 0 && (
          <p className="text-gray-500 text-center py-8">暂无演化记录</p>
        )}
      </div>
    </div>
  )
}
