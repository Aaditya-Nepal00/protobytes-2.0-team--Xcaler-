import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import tendersService from '../services/tenders.service'

export default function Tenders() {
    const [data, setData] = useState<any>({ tenders: [], total: 0 })
    const [loading, setLoading] = useState(true)
    const [search, setSearch] = useState('')

    useEffect(() => {
        setLoading(true)
        tendersService.getAll({ q: search || undefined })
            .then(setData)
            .catch(() => { })
            .finally(() => setLoading(false))
    }, [search])

    const formatAmount = (n: number) => {
        if (!n) return 'N/A'
        if (n >= 1e7) return `रु ${(n / 1e7).toFixed(1)} Cr`
        if (n >= 1e5) return `रु ${(n / 1e5).toFixed(1)} Lakh`
        return `रु ${n.toLocaleString()}`
    }

    return (
        <div className="page-container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', marginBottom: 40, flexWrap: 'wrap', gap: 20 }} className="mobile-stack">
                <div>
                    <h1 className="page-title">Public Procurement</h1>
                    <p className="page-subtitle" style={{ marginBottom: 0 }}>Discover active tenders and track government contract awards.</p>
                </div>
                <div style={{ position: 'relative', width: '100%', maxWidth: 400 }} className="mobile-stack">
                    <input
                        type="text"
                        className="input"
                        placeholder="Search tenders, organizations..."
                        style={{ paddingLeft: 44 }}
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                    />
                    <span style={{ position: 'absolute', left: 14, top: '50%', transform: 'translateY(-50%)' }} className="hide-mobile">🔍</span>
                </div>
            </div>

            {loading ? (
                <div className="loader"><div className="spinner" /></div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(min(100%, 320px), 1fr))', gap: 24 }}>
                    {data.tenders.map((t: any) => (
                        <div key={t.id} className="card" style={{ display: 'flex', flexDirection: 'column' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 16 }}>
                                <span className={`badge ${t.status === 'active' ? 'badge-success' : 'badge-primary'}`}>{t.status}</span>
                                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Procuring Entity: <strong>{t.organization}</strong></span>
                            </div>
                            <h3 style={{ fontSize: '1.2rem', marginBottom: 12, flex: 1 }}>{t.title}</h3>

                            <div style={{ background: '#f8fafc', padding: 16, borderRadius: 8, marginBottom: 20 }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
                                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>ESTIMATED BUDGET</span>
                                    <span style={{ fontWeight: 800, color: 'var(--primary)' }}>{formatAmount(t.budget)}</span>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 600 }}>SUBMISSION DEADLINE</span>
                                    <span style={{ fontWeight: 600, color: 'var(--danger)', fontSize: '0.85rem' }}>{new Date(t.deadline).toLocaleDateString()}</span>
                                </div>
                            </div>

                            <div style={{ display: 'flex', gap: 12 }}>
                                <Link to={`/tenders/${t.id}`} className="btn btn-primary" style={{ flex: 1, textAlign: 'center' }}>View Notice</Link>
                                <button className="btn btn-outline" style={{ flex: 1 }}>Bidding Docs</button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    )
}
