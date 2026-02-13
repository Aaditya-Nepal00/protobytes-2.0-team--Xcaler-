import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import tendersService from '../services/tenders.service'

export default function TenderDetail() {
    const { tenderId } = useParams()
    const [tender, setTender] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (tenderId) {
            tendersService.getById(tenderId)
                .then(setTender)
                .catch(() => { })
                .finally(() => setLoading(false))
        }
    }, [tenderId])

    const formatAmount = (n: number) => {
        if (!n) return 'N/A'
        if (n >= 1e7) return `रु ${(n / 1e7).toFixed(2)} Crore`
        if (n >= 1e5) return `रु ${(n / 1e5).toFixed(1)} Lakh`
        return `रु ${n.toLocaleString()}`
    }

    if (loading) return <div className="page-container"><div className="loader"><div className="spinner" /></div></div>
    if (!tender) return <div className="page-container"><h1>Tender not found</h1></div>

    return (
        <div className="page-container">
            <Link to="/tenders" className="btn btn-outline" style={{ marginBottom: 32, display: 'inline-flex', alignItems: 'center', gap: 8, padding: '8px 16px' }}>
                ← Back to Tenders
            </Link>

            <div className="card animate-fade-in-up" style={{ padding: 40 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 32, flexWrap: 'wrap', gap: 20 }}>
                    <div style={{ flex: 1, minWidth: '60%' }}>
                        <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
                            <span className="badge badge-primary">{tender.category || 'General'}</span>
                            <span className={`badge ${tender.status === 'active' || tender.status === 'open' ? 'badge-success' : 'badge-primary'}`}>
                                {tender.status.toUpperCase()}
                            </span>
                        </div>
                        <h1 style={{ fontSize: '2.2rem', marginBottom: 16, color: 'var(--primary)', lineHeight: 1.2 }}>{tender.title}</h1>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 12, color: 'var(--text-muted)', fontWeight: 600 }}>
                            🏢 Procuring Entity: <span style={{ color: 'var(--text-main)' }}>{tender.organization}</span>
                        </div>
                    </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: 32, marginBottom: 40 }}>
                    <div className="card" style={{ background: 'var(--bg-body)', padding: 24, border: '1px solid var(--border-color)' }}>
                        <h4 style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 16 }}>Financial Overview</h4>
                        <div style={{ marginBottom: 20 }}>
                            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 4 }}>Estimated Budget</div>
                            <div style={{ fontSize: '1.5rem', fontWeight: 900, color: 'var(--primary)' }}>{formatAmount(tender.budget)}</div>
                        </div>
                        {tender.awarded_amount && (
                            <div style={{ padding: '16px 0', borderTop: '1px solid var(--border-color)' }}>
                                <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 4 }}>Awarded Amount</div>
                                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--success)' }}>{formatAmount(tender.awarded_amount)}</div>
                            </div>
                        )}
                    </div>

                    <div className="card" style={{ background: 'rgba(239, 68, 68, 0.05)', padding: 24, border: '1px solid rgba(239, 68, 68, 0.2)' }}>
                        <h4 style={{ fontSize: '0.75rem', color: 'var(--danger)', textTransform: 'uppercase', marginBottom: 16, fontWeight: 800 }}>Critical Dates</h4>
                        <div style={{ marginBottom: 16 }}>
                            <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: 4 }}>Submission Deadline</div>
                            <div style={{ fontSize: '1.2rem', fontWeight: 800, color: 'var(--danger)' }}>{new Date(tender.deadline).toLocaleString()}</div>
                        </div>
                        <div style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                            Published on: {new Date(tender.published_date).toLocaleDateString()}
                        </div>
                    </div>
                </div>

                <div style={{ marginBottom: 48 }}>
                    <h3 style={{ marginBottom: 20, borderBottom: '2px solid var(--primary)', display: 'inline-block', paddingBottom: 6 }}>Scope of Work & Description</h3>
                    <div style={{ fontSize: '1.1rem', lineHeight: 1.8, color: 'var(--text-main)', whiteSpace: 'pre-wrap' }}>
                        {tender.description}
                    </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 24 }}>
                    <div className="card" style={{ padding: 24 }}>
                        <h4 style={{ marginBottom: 12 }}>Eligibility Criteria</h4>
                        <ul style={{ paddingLeft: 20 }}>
                            <li>Registered Nepali firm for over 5 years</li>
                            <li>Annual Turnover &gt; रु 10 Crore</li>
                            <li>Technical certification equivalent to ISO</li>
                        </ul>
                    </div>
                    {tender.awarded_to && (
                        <div className="card" style={{ padding: 24, background: 'var(--bg-body)' }}>
                            <h4 style={{ marginBottom: 12 }}>Award Information</h4>
                            <div style={{ color: 'var(--text-muted)', marginBottom: 12 }}>This contract has been awarded following a competitive bidding process.</div>
                            <div style={{ fontWeight: 800, fontSize: '1.1rem', color: 'var(--primary)' }}>🏆 {tender.awarded_to}</div>
                        </div>
                    )}
                </div>

                <div style={{ marginTop: 40, textAlign: 'center' }}>
                    <button className="btn btn-primary" style={{ padding: '16px 40px', fontSize: '1rem', fontWeight: 700 }}>Download Full Tender Document (PDF)</button>
                </div>
            </div>
        </div>
    )
}
