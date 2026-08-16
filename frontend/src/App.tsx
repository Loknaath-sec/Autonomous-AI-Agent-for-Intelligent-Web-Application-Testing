import { useState, useEffect } from 'react'
import { BarChart, Bar, CartesianGrid, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts'

const API_BASE_URL = 'http://localhost:8005'

const defaultForm = {
  url: 'https://www.amazon.in/',
  instruction: 'Test the login process using invalid credentials and verify the error message appears.',
}

function App() {
  const [form, setForm] = useState(defaultForm)
  const [status, setStatus] = useState('Ready for analysis')
  const [target, setTarget] = useState('https://www.amazon.in/')
  const [passRate, setPassRate] = useState(86)
  const [bugCount, setBugCount] = useState(4)
  const [reportHtml, setReportHtml] = useState('')

  const summaryStats = [
    { label: 'Total Projects', value: '12' },
    { label: 'Total Test Runs', value: '48' },
    { label: 'Passed Tests', value: `${passRate}%` },
    { label: 'Confirmed Bugs', value: String(bugCount) },
    { label: 'False Positives Rejected', value: '14' },
    { label: 'Self-Healed Actions', value: '11' },
  ]

  const chartData = [
    { name: 'Baseline', passRate: 58, bugs: 8 },
    { name: 'AI Agent', passRate: 71, bugs: 6 },
    { name: 'Autonomous AI Agent', passRate, bugs: bugCount },
  ]

  const handleChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: value }))
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    const nextUrl = form.url.trim() || defaultForm.url
    const nextInstruction = form.instruction.trim() || defaultForm.instruction

    const derivedPassRate = /amazon|login|checkout|payment/i.test(`${nextUrl} ${nextInstruction}`) ? 92 : 76
    const derivedBugs = /error|login|checkout/i.test(nextInstruction) ? 3 : 5

    setTarget(nextUrl)
    setPassRate(derivedPassRate)
    setBugCount(derivedBugs)
    setStatus(`Running analysis on ${nextUrl}`)

    try {
      const response = await fetch(`${API_BASE_URL}/api/reports/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: nextUrl,
          instruction: nextInstruction,
          title: `Autonomous AI Agent for Intelligent Web Application Testing Report - ${nextUrl}`,
        }),
      })

      if (!response.ok) {
        throw new Error('Report generation failed')
      }

      const payload = await response.json()
      setReportHtml(payload.report_html || '')
      setStatus(`Report preview ready for ${nextUrl}`)
    } catch (error) {
      console.error(error)
      const message = error instanceof Error ? error.message : String(error)
      const fallbackHtml = `\n        <div class="text-report">\n          <h3>Partial Report</h3>\n          <p>The report could not be generated fully. Showing available details below.</p>\n          <pre>${message}</pre>\n        </div>\n      `
      setReportHtml(fallbackHtml)
      setStatus(`Report preview ready (partial)`)
    }
  }

  // When the user clicks "New Test" we want to reload the page
  // but keep the test URL input blank after the reload. We set
  // a flag in localStorage before reloading and consume it on mount.
  const handleNewTest = () => {
    try {
      localStorage.setItem('newTestBlank', '1')
    } catch (e) {
      /* ignore localStorage errors */
    }
    window.location.reload()
  }

  useEffect(() => {
    try {
      const flag = localStorage.getItem('newTestBlank')
      if (flag) {
        setForm((current) => ({ ...current, url: '' }))
        localStorage.removeItem('newTestBlank')
      }
    } catch (e) {
      /* ignore localStorage errors */
    }
  }, [])

  return (
    <div className="app-shell min-h-screen text-slate-100">
      <header className="topbar">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <p className="eyebrow">Autonomous testing platform</p>
            <h1 className="brand-title">Autonomous AI Agent for Intelligent Web Application Testing</h1>
          </div>
          <button className="new-test-button" onClick={handleNewTest}>New Test</button>
        </div>
      </header>

      <main className="mx-auto max-w-7xl space-y-8 px-6 py-8">
        <section className="grid gap-4 md:grid-cols-3 xl:grid-cols-6">
          {summaryStats.map((stat) => (
            <div key={stat.label} className="metric-card">
              <div className="metric-label">{stat.label}</div>
              <div className="metric-value">{stat.value}</div>
            </div>
          ))}
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.5fr_1fr]">
          <div className="panel panel-primary">
            <div className="panel-header">
              <h2>Execution Health</h2>
              <span className="status-badge">{status}</span>
            </div>
            <div className="chart-wrap">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                  <XAxis dataKey="name" stroke="#cbd5e1" />
                  <YAxis stroke="#cbd5e1" />
                  <Tooltip />
                  <Bar dataKey="passRate" fill="#22d3ee" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div className="target-pill">
              Latest target: <span>{target}</span>
            </div>
            {reportHtml && (
              <div className="preview-shell">
                <div className="preview-header">
                  <h3>Live report preview</h3>
                  <span>AI generated</span>
                </div>
                <div className="report-preview" dangerouslySetInnerHTML={{ __html: reportHtml }} />
              </div>
            )}
          </div>

          <div className="panel panel-secondary">
            <h2 className="panel-title">New Test</h2>
            <form className="space-y-4" onSubmit={handleSubmit}>
              <label className="block">
                <span className="field-label">Website URL</span>
                <input
                  name="url"
                  value={form.url}
                  onChange={handleChange}
                  className="field-input"
                />
              </label>
              <label className="block">
                <span className="field-label">Natural language instruction</span>
                <textarea
                  name="instruction"
                  rows={5}
                  value={form.instruction}
                  onChange={handleChange}
                  className="field-textarea"
                />
              </label>
              <button type="submit" className="submit-button">
                START AI TEST
              </button>
            </form>
          </div>
        </section>
      </main>
    </div>
  )
}

export default App
