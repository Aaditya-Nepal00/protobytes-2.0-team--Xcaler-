import { useEffect, useState } from 'react'
import corruptionService from '../services/corruption.service'

export default function CorruptionReport() {
    const [reports, setReports] = useState<any[]>([])
    const [loading, setLoading] = useState(true)
    const [showForm, setShowForm] = useState(false)

    const [newReport, setNewReport] = useState({
        title: '',
        description: '',
        severity: 'medium',
        location: '',
    })

    useEffect(() => {
        corruptionService.getReports()
            .then(res => setReports(res.reports))
            .catch(() => { })
            .finally(() => setLoading(false))
    }, [])

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            const res = await corruptionService.submitReport(newReport)
            alert(`Report submitted successfully! Your tracking ID is: ${res.tracking_id}`)
            setShowForm(false)
            setNewReport({ title: '', description: '', severity: 'medium', location: '' })
            // Refresh
            const updated = await corruptionService.getReports()
            setReports(updated.reports)
        } catch (err) {
            alert('Submission failed.')
        }
    }

    return (
        <div className="page-container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', marginBottom: 40, flexWrap: 'wrap', gap: 20 }}>
                <div>
                    <h1 className="page-title">Citizen Accountability</h1>
                    <p className="page-subtitle" style={{ marginBottom: 0 }}>Report irregularities and monitor the status of corruption investigations.</p>
                </div>
                <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
                    {showForm ? '✕ Close Form' : '🚀 File a Report'}
                </button>
            </div>

            {showForm && (
                <div className="card animate-fade-in-up" style={{ marginBottom: 40, background: 'var(--bg-body)', border: '2px solid var(--primary)' }}>
                    <h3 style={{ marginBottom: 20 }}>Secure Anonymous Submission</h3>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: 24 }}>
                        Your identity is protected by end-to-end encryption. Please provide as much detail as possible.
                    </p>
                    <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 20 }}>
                        <div style={{ gridColumn: 'span 2' }}>
                            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Title of Malpractice</label>
                            <input type="text" className="input" placeholder="e.g. Bribe requested at Ward Office 4"
                                value={newReport.title} onChange={e => setNewReport({ ...newReport, title: e.target.value })} required />
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Severity Level</label>
                            <select className="input" value={newReport.severity} onChange={e => setNewReport({ ...newReport, severity: e.target.value })}>
                                <option value="low">Low (Minor policy violation)</option>
                                <option value="medium">Medium (Procedural issues)</option>
                                <option value="high">High (Direct Bribery)</option>
                                <option value="critical">Critical (Systemic Fraud)</option>
                            </select>
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Location/District</label>
                            <input type="text" className="input" placeholder="e.g. Kathmandu, Koteshwor"
                                value={newReport.location} onChange={e => setNewReport({ ...newReport, location: e.target.value })} required />
                        </div>
                        <div style={{ gridColumn: 'span 2' }}>
                            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Detailed Description & Evidence</label>
                            <textarea className="input" style={{ minHeight: 120 }} placeholder="Describe what happened, when, and who was involved..."
                                value={newReport.description} onChange={e => setNewReport({ ...newReport, description: e.target.value })} required />
                        </div>
                        <div style={{ gridColumn: 'span 2' }}>
                            <button type="submit" className="btn btn-primary" style={{ width: '100%', padding: '14px' }}>Submit Secure Report</button>
                        </div>
                    </form>
                </div>
            )}

            {loading ? (
                <div className="loader"><div className="spinner" /></div>
            ) : (
                <div className="reports-list" style={{ display: 'grid', gap: 24 }}>
                    {reports.map((r: any) => (
                        <div key={r.id} className="card report-card mobile-stack">
                            <div className="report-main">
                                <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
                                    <span className={`badge ${r.severity === 'critical' ? 'badge-danger' : r.severity === 'high' ? 'badge-warning' : 'badge-info'}`}>
                                        {r.severity}
                                    </span>
                                    <span className="badge badge-primary" style={{ background: 'var(--bg-body)' }}>#{r.tracking_id}</span>
                                </div>
                                <h3 className="report-title">{r.title}</h3>
                                <p className="report-desc">{r.description}</p>
                            </div>
                            <div className="status-sidebar">
                                <div className="status-label">Investigation Status</div>
                                <div className="status-value">
                                    {r.status.replace(/_/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase())}
                                </div>
                                <div className="status-progress-bg">
                                    <div className="status-progress-bar" style={{ width: r.status === 'pending' ? '20%' : r.status === 'resolved' ? '100%' : '60%' }} />
                                </div>
                                <span className="status-updated">Updated: {new Date(r.created_at).toLocaleDateString()}</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
