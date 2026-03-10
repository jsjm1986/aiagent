import { ConsciousnessStream } from './components/Consciousness/ConsciousnessStream'
import { ProjectsBoard } from './components/Projects/ProjectsBoard'
import { DrivesDashboard } from './components/Drives/DrivesDashboard'
import { CreationsGallery } from './components/Creations/CreationsGallery'
import './index.css'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="px-6 py-4">
          <h1 className="text-2xl font-bold text-gray-900">自主智能体系统</h1>
        </div>
      </header>
      <div className="grid grid-cols-4 gap-4 p-4 h-[calc(100vh-80px)]">
        <div className="overflow-y-auto bg-white rounded-lg shadow">
          <ConsciousnessStream />
        </div>
        <div className="overflow-y-auto bg-white rounded-lg shadow">
          <ProjectsBoard />
        </div>
        <div className="overflow-y-auto bg-white rounded-lg shadow">
          <CreationsGallery />
        </div>
        <div className="overflow-y-auto bg-white rounded-lg shadow">
          <DrivesDashboard />
        </div>
      </div>
    </div>
  )
}

export default App
