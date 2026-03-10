import { useEffect, useState } from 'react'

interface Drive {
  name: string
  score: number
  active: boolean
}

export function DrivesDashboard() {
  const [drives, setDrives] = useState<Record<string, Drive>>({})

  useEffect(() => {
    fetch('/api/drives/status', {
      headers: { 'Accept': 'application/json; charset=utf-8' }
    })
      .then(res => res.json())
      .then(setDrives)

    const interval = setInterval(() => {
      fetch('/api/drives/status', {
        headers: { 'Accept': 'application/json; charset=utf-8' }
      })
        .then(res => res.json())
        .then(setDrives)
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">⚡ 核心驱动力</h2>
      <div className="space-y-3">
        {Object.entries(drives).map(([key, drive]) => (
          <div
            key={key}
            className={`p-3 rounded border-2 ${
              drive.active ? 'border-green-500 bg-green-50' : 'border-gray-300 bg-gray-50'
            }`}
          >
            <h3 className="font-semibold text-sm mb-2">{drive.name}</h3>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full ${
                  drive.active ? 'bg-green-500' : 'bg-gray-400'
                }`}
                style={{ width: `${drive.score * 100}%` }}
              />
            </div>
            <p className="text-xs mt-1 text-gray-600">
              {(drive.score * 100).toFixed(0)}% {drive.active ? '✓ 活跃' : ''}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}
