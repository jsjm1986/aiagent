import { useEffect, useState } from 'react'

interface Creation {
  id: string
  title: string
  type: string
  content: string
  created_at: string
}

export function CreationsGallery() {
  const [creations, setCreations] = useState<Creation[]>([])
  const [selected, setSelected] = useState<Creation | null>(null)

  useEffect(() => {
    fetch('/api/creations', {
      headers: { 'Accept': 'application/json; charset=utf-8' }
    })
      .then(res => res.json())
      .then(setCreations)

    const interval = setInterval(() => {
      fetch('/api/creations', {
        headers: { 'Accept': 'application/json; charset=utf-8' }
      })
        .then(res => res.json())
        .then(setCreations)
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">🎨 创作画廊</h2>
      <div className="space-y-2">
        {creations.length === 0 && (
          <div className="text-gray-400 text-center py-8 text-sm">暂无创作</div>
        )}
        {creations.slice(0, 20).map((creation) => (
          <div
            key={creation.id}
            className="p-3 bg-gray-50 rounded border border-gray-200 cursor-pointer hover:bg-gray-100 transition"
            onClick={() => setSelected(creation)}
          >
            <div className="flex justify-between items-start mb-1">
              <span className="font-semibold text-sm truncate">{creation.title}</span>
              <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs rounded ml-2">{creation.type}</span>
            </div>
            <p className="text-xs text-gray-500">{new Date(creation.created_at).toLocaleString('zh-CN')}</p>
          </div>
        ))}
      </div>

      {selected && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={() => setSelected(null)}>
          <div className="bg-white rounded-lg p-4 max-w-2xl w-full max-h-[80vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-lg font-bold">{selected.title}</h3>
              <button onClick={() => setSelected(null)} className="text-gray-500 hover:text-gray-700">✕</button>
            </div>
            <div className="mb-2 text-xs text-gray-500">
              类型: {selected.type} | 创建时间: {new Date(selected.created_at).toLocaleString('zh-CN')}
            </div>
            <pre className="bg-gray-50 p-3 rounded text-xs overflow-x-auto whitespace-pre-wrap">{selected.content}</pre>
          </div>
        </div>
      )}
    </div>
  )
}
