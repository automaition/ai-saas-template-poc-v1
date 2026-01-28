import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import api from '@/lib/api'
import { CheckCircle, Rocket, Zap } from 'lucide-react'

function App() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle')
  const [healthData, setHealthData] = useState<{
    status: string
    environment: string
    database: string
  } | null>(null)

  const checkHealth = async () => {
    setStatus('loading')
    try {
      const response = await api.get('/v1/health')
      setHealthData(response.data)
      setStatus('success')
    } catch {
      setStatus('error')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <Card className="w-full max-w-lg border-slate-700 bg-slate-800/50 backdrop-blur-sm shadow-2xl">
        <CardHeader className="text-center space-y-4">
          <div className="mx-auto w-16 h-16 rounded-full bg-gradient-to-br from-emerald-400 to-cyan-500 flex items-center justify-center">
            <Rocket className="w-8 h-8 text-white" />
          </div>
          <CardTitle className="text-3xl font-bold bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
            Agent PoC Template Ready
          </CardTitle>
          <CardDescription className="text-slate-400 text-base">
            Full-stack scaffold per SaaS PoC con FastAPI, React, e OpenRouter AI
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="p-3 rounded-lg bg-slate-700/50">
              <Zap className="w-6 h-6 mx-auto mb-2 text-yellow-400" />
              <p className="text-xs text-slate-400">FastAPI</p>
            </div>
            <div className="p-3 rounded-lg bg-slate-700/50">
              <Zap className="w-6 h-6 mx-auto mb-2 text-blue-400" />
              <p className="text-xs text-slate-400">React + TS</p>
            </div>
            <div className="p-3 rounded-lg bg-slate-700/50">
              <Zap className="w-6 h-6 mx-auto mb-2 text-purple-400" />
              <p className="text-xs text-slate-400">OpenRouter</p>
            </div>
          </div>

          <Button
            onClick={checkHealth}
            className="w-full bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-600 hover:to-cyan-600 text-white font-semibold h-12 text-base transition-all duration-300"
            disabled={status === 'loading'}
          >
            {status === 'loading' ? 'Checking...' : 'Check Backend Health'}
          </Button>

          {status === 'success' && healthData && (
            <div className="p-4 rounded-lg bg-emerald-900/30 border border-emerald-700 animate-in fade-in duration-300">
              <div className="flex items-center gap-2 mb-3">
                <CheckCircle className="w-5 h-5 text-emerald-400" />
                <span className="font-semibold text-emerald-400">Backend Connected!</span>
              </div>
              <div className="text-sm text-slate-300 space-y-1">
                <p>Status: <span className="text-emerald-400">{healthData.status}</span></p>
                <p>Environment: <span className="text-cyan-400">{healthData.environment}</span></p>
                <p>Database: <span className="text-cyan-400">{healthData.database}</span></p>
              </div>
            </div>
          )}

          {status === 'error' && (
            <div className="p-4 rounded-lg bg-red-900/30 border border-red-700 text-center animate-in fade-in duration-300">
              <p className="text-red-400">Backend non raggiungibile. Avvia con:</p>
              <code className="text-xs text-slate-400 mt-2 block">docker-compose up</code>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default App
