import { useEffect, useState } from 'react'
import lawsService from '../services/laws.service'

export default function Laws() {
    const [laws, setLaws] = useState<any[]>([])
    const [loading, setLoading] = useState(true)
    const [search, setSearch] = useState('')
    const [selectedLaw, setSelectedLaw] = useState<any>(null)

    useEffect(() => {
        setLoading(true)
        lawsService.getLaws({ search: search || undefined })
            .then(res => setLaws(res.laws))
            .catch(() => { })
            .finally(() => setLoading(false))
    }, [search])

    return (
        <div className="page-container">
            <div style={{ marginBottom: 40 }}>
                <h1 className="page-title">Legal Knowledge Hub</h1>
                <p className="page-subtitle">Access simplified versions of Nepali laws, acts, and your fundamental rights.</p>

                <div style={{ position: 'relative', maxWidth: 600 }}>
                    <input
                        type="text"
                        className="input"
                        placeholder="Search for laws (e.g. RTI, Anti-Corruption, Land)..."
                        style={{ paddingLeft: 48, height: 50 }}
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                    />
                    <span style={{ position: 'absolute', left: 16, top: '50%', transform: 'translateY(-50%)', fontSize: '1.2rem' }}>🔍</span>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: selectedLaw ? '1fr 500px' : '1fr', gap: 32 }}>
                <div style={{ display: 'grid', gridTemplateColumns: selectedLaw ? '1fr' : 'repeat(auto-fit, minmax(300px, 1fr))', gap: 20 }}>
                    {loading ? (
                        <div className="loader"><div className="spinner" /></div>
                    ) : laws.map((l: any) => (
                        <div key={l.id} className={`card ${selectedLaw?.id === l.id ? 'active' : ''}`}
                            style={{ cursor: 'pointer', borderLeft: selectedLaw?.id === l.id ? '5px solid var(--primary)' : '1px solid var(--border-color)' }}
                            onClick={() => setSelectedLaw(l)}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12 }}>
                                <span className="badge badge-primary">{l.category}</span>
                                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>BS {l.year_enacted}</span>
                            </div>
                            <h3 style={{ fontSize: '1.15rem', marginBottom: 8 }}>{l.title}</h3>
                            <p style={{ fontSize: '0.9rem', color: 'var(--text-ne)', marginBottom: 12 }}>{l.title_nepali}</p>
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                                {l.simplified}
                            </p>
                        </div>
                    ))}
                </div>

                {selectedLaw && (
                    <div className="card animate-fade-in-up" style={{ position: 'sticky', top: 100, height: 'fit-content', maxHeight: '80vh', overflowY: 'auto' }}>
                        <button style={{ float: 'right', background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem' }} onClick={() => setSelectedLaw(null)}>✕</button>
                        <span className="badge badge-primary" style={{ marginBottom: 16 }}>Detailed View</span>
                        <h2 style={{ fontSize: '1.75rem', marginBottom: 8 }}>{selectedLaw.title}</h2>
                        <p style={{ fontSize: '1.25rem', color: 'var(--primary)', marginBottom: 32, fontStyle: 'italic' }}>{selectedLaw.title_nepali}</p>

                        <div style={{ background: 'var(--bg-body)', padding: 24, borderRadius: 8, marginBottom: 32, borderLeft: '4px solid var(--info)' }}>
                            <h4 style={{ color: 'var(--info)', marginBottom: 8, fontSize: '0.9rem', textTransform: 'uppercase' }}>Plain Language Summary</h4>
                            <p style={{ fontSize: '1.1rem', lineHeight: 1.6, color: 'var(--primary)' }}>{selectedLaw.simplified}</p>
                            <p style={{ marginTop: 12, fontStyle: 'italic', color: 'var(--text-muted)' }}>{selectedLaw.simplified_nepali}</p>
                        </div>

                        <div style={{ marginBottom: 32 }}>
                            <h4 style={{ marginBottom: 12, color: 'var(--primary)' }}>Official Text Extracts</h4>
                            <div style={{ fontSize: '0.95rem', color: 'var(--text-main)', background: 'var(--bg-body)', padding: 20, borderRadius: 8, border: '1px solid var(--border-color)' }}>
                                {selectedLaw.content}
                            </div>
                        </div>

                        <button className="btn btn-primary" style={{ width: '100%' }}>Download Official PDF</button>
                    </div>
                )}
            </div>

            <style>{`
        .active { box-shadow: var(--shadow-lg); transform: translateX(5px); }
      `}</style>
        </div>
    )
}
