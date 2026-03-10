import { useEffect, useState } from 'react'

interface Task {
  id: string
  type: string
  description: string
  status: string
  weight: number
  created_at: string
  completed_at: string | null
  result: string | null
}

interface Project {
  id: string
  name: string
  description: string
  status: string
  progress: number
  tasks?: Task[]
}

export function ProjectsBoard() {
  const [projects, setProjects] = useState<Project[]>([])
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)

  useEffect(() => {
    fetch('/api/projects', {
      headers: { 'Accept': 'application/json; charset=utf-8' }
    })
      .then(res => res.json())
      .then(setProjects)

    const interval = setInterval(() => {
      fetch('/api/projects', {
        headers: { 'Accept': 'application/json; charset=utf-8' }
      })
        .then(res => res.json())
        .then(setProjects)
    }, 5000)

    return () => clearInterval(interval)
  }, [])

  const loadProjectDetail = async (projectId: string) => {
    const res = await fetch(`/api/projects/${projectId}`, {
      headers: { 'Accept': 'application/json; charset=utf-8' }
    })
    const data = await res.json()
    setSelectedProject(data)
  }

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4">📋 项目看板</h2>
      <div className="space-y-3">
        {projects.map(project => (
          <div
            key={project.id}
            className="p-3 bg-gray-50 rounded border border-gray-200 cursor-pointer hover:bg-gray-100 transition"
            onClick={() => loadProjectDetail(project.id)}
          >
            <h3 className="font-semibold text-sm">{project.name}</h3>
            <p className="text-xs text-gray-600 mt-1">{project.description}</p>
            <div className="mt-2">
              <div className="w-full bg-gray-200 rounded-full h-1.5">
                <div
                  className="bg-blue-500 h-1.5 rounded-full"
                  style={{ width: `${project.progress * 100}%` }}
                />
              </div>
              <p className="text-xs text-gray-500 mt-1">{(project.progress * 100).toFixed(0)}%</p>
            </div>
          </div>
        ))}
      </div>

      {selectedProject && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" onClick={() => setSelectedProject(null)}>
          <div className="bg-white rounded-lg p-4 max-w-lg w-full max-h-[70vh] overflow-y-auto" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-3">
              <h3 className="text-lg font-bold">{selectedProject.name}</h3>
              <button onClick={() => setSelectedProject(null)} className="text-gray-500 hover:text-gray-700">✕</button>
            </div>
            <p className="text-sm text-gray-600 mb-3">{selectedProject.description}</p>
            <div className="mb-3">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${selectedProject.progress * 100}%` }} />
              </div>
              <p className="text-xs text-gray-500 mt-1">进度: {(selectedProject.progress * 100).toFixed(0)}%</p>
            </div>
            <h4 className="font-semibold mb-2 text-sm">任务列表</h4>
            <div className="space-y-2">
              {selectedProject.tasks?.map(task => (
                <div key={task.id} className={`p-2 rounded border text-xs ${task.status === 'completed' ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'}`}>
                  <div className="flex justify-between items-start mb-1">
                    <div>
                      <span className="px-1.5 py-0.5 bg-blue-100 text-blue-700 rounded mr-1">{task.type}</span>
                      <span className={`px-1.5 py-0.5 rounded ${task.status === 'completed' ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'}`}>{task.status}</span>
                    </div>
                    <span className="text-gray-500">权重: {(task.weight * 100).toFixed(0)}%</span>
                  </div>
                  <p className="mt-1">{task.description}</p>
                  {task.result && <p className="mt-1 text-gray-600">结果: {task.result}</p>}
                </div>
              ))}
              {(!selectedProject.tasks || selectedProject.tasks.length === 0) && (
                <p className="text-gray-400 text-center py-4 text-sm">暂无任务</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
