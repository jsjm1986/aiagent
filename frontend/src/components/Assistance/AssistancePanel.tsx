import { useEffect, useState } from 'react'

interface AssistanceRequest {
  id: string
  type: string
  title: string
  description: string
  status: string
  created_at: string
}

export function AssistancePanel() {
  const [requests, setRequests] = useState<AssistanceRequest[]>([])

  useEffect(() => {
    fetch('/api/assistance/pending')
      .then(res => res.json())
      .then(setRequests)

    const interval = setInterval(() => {
      fetch('/api/assistance/pending')
        .then(res => res.json())
        .then(setRequests)
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">人类协助请求</h2>
      <div className="space-y-3">
        {requests.map(req => (
          <div key={req.id} className="p-4 bg-yellow-50 border-2 border-yellow-300 rounded-lg">
            <div className="flex justify-between items-start">
              <div>
                <span className="text-xs bg-yellow-200 px-2 py-1 rounded">{req.type}</span>
                <h3 className="font-bold mt-2">{req.title}</h3>
                <p className="text-sm text-gray-700 mt-1">{req.description}</p>
              </div>
              <span className="text-xs text-gray-500">{new Date(req.created_at).toLocaleString()}</span>
            </div>
          </div>
        ))}
        {requests.length === 0 && (
          <p className="text-gray-500 text-center py-8">暂无协助请求</p>
        )}
      </div>
    </div>
  )
}
