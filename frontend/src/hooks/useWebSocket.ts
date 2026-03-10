import { useEffect, useState } from 'react'

export function useWebSocket() {
  const [ws, setWs] = useState<WebSocket | null>(null)
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws')

    socket.onopen = () => {
      setConnected(true)
      console.log('WebSocket connected')
    }

    socket.onclose = () => {
      setConnected(false)
      console.log('WebSocket disconnected')
    }

    setWs(socket)

    return () => {
      socket.close()
    }
  }, [])

  const subscribe = (eventType: string, callback: (data: any) => void) => {
    if (!ws) return

    const handler = (event: MessageEvent) => {
      const message = JSON.parse(event.data)
      if (message.type === eventType) {
        callback(message.data)
      }
    }

    ws.addEventListener('message', handler)
    return () => ws.removeEventListener('message', handler)
  }

  return { connected, subscribe }
}
