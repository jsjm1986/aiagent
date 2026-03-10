import { DrivesDashboard } from '../Drives/DrivesDashboard'
import { ConsciousnessStream } from '../Consciousness/ConsciousnessStream'
import { ProjectsBoard } from '../Projects/ProjectsBoard'
import { AssistancePanel } from '../Assistance/AssistancePanel'
import { EvolutionTimeline } from '../Evolution/EvolutionTimeline'
import { LearningInsights } from '../Evolution/LearningInsights'
import { useWebSocket } from '../../hooks/useWebSocket'

export function Dashboard() {
  const { connected } = useWebSocket()

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4">
          <h1 className="text-3xl font-bold text-gray-900">
            自主智能体系统
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            WebSocket: {connected ? '🟢 已连接' : '🔴 未连接'}
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 px-4 space-y-6">
        <DrivesDashboard />
        <div className="grid grid-cols-2 gap-6">
          <ConsciousnessStream />
          <AssistancePanel />
        </div>
        <div className="grid grid-cols-2 gap-6">
          <EvolutionTimeline />
          <LearningInsights />
        </div>
        <ProjectsBoard />
      </main>
    </div>
  )
}
