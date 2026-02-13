import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import forumService from '../services/forum.service'
import { useAuthStore } from '../store/authStore'

export default function Forum() {
    const [threads, setThreads] = useState<any[]>([])
    const [loading, setLoading] = useState(true)
    const [category, setCategory] = useState('')
    const [showCreate, setShowCreate] = useState(false)
    const { isAuthenticated } = useAuthStore()

    const [newThread, setNewThread] = useState({ title: '', content: '', category: 'governance' })

    useEffect(() => {
        setLoading(true)
        forumService.getThreads({ category: category || undefined })
            .then(res => setThreads(res.threads))
            .catch(() => { })
            .finally(() => setLoading(false))
    }, [category])

    const handleCreate = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            await forumService.createThread(newThread)
            setShowCreate(false)
            setNewThread({ title: '', content: '', category: 'governance' })
            // Refresh
            const res = await forumService.getThreads({ category: category || undefined })
            setThreads(res.threads)
        } catch (err) {
            alert('Failed to post thread. Please ensure you are logged in.')
        }
    }

    return (
        <div className="page-container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', marginBottom: 40, flexWrap: 'wrap', gap: 20 }}>
                <div>
                    <h1 className="page-title">Community Voice</h1>
                    <p className="page-subtitle" style={{ marginBottom: 0 }}>Engage with fellow citizens on national issues and governance.</p>
                </div>
                <div>
                    <button className="btn btn-primary" onClick={() => setShowCreate(!showCreate)}>
                        {showCreate ? '✕ Close Form' : '+ Share an Issue'}
                    </button>
                </div>
            </div>

            {showCreate && (
                <div className="card animate-fade-in-up" style={{ marginBottom: 40, background: 'var(--bg-body)' }}>
                    <h3 style={{ marginBottom: 20 }}>Post a New Discussion/Issue</h3>
                    <form onSubmit={handleCreate} style={{ display: 'grid', gap: 16 }}>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Title</label>
                            <input type="text" className="input" placeholder="Summarize your issue or question..."
                                value={newThread.title} onChange={e => setNewThread({ ...newThread, title: e.target.value })} required />
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Category</label>
                            <select className="input" value={newThread.category} onChange={e => setNewThread({ ...newThread, category: e.target.value })}>
                                <option value="governance">Governance</option>
                                <option value="corruption">Corruption</option>
                                <option value="development">Development</option>
                                <option value="budget">Budget</option>
                                <option value="general">General</option>
                            </select>
                        </div>
                        <div>
                            <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Details</label>
                            <textarea className="input" style={{ minHeight: 120, resize: 'vertical' }} placeholder="Explain in detail..."
                                value={newThread.content} onChange={e => setNewThread({ ...newThread, content: e.target.value })} required />
                        </div>
                        {!isAuthenticated && <p style={{ color: 'var(--danger)', fontSize: '0.85rem' }}>⚠️ You must be logged in to post.</p>}
                        <button type="submit" className="btn btn-primary" disabled={!isAuthenticated}>Create Thread</button>
                    </form>
                </div>
            )}

            {/* Categories & Layout Wrapper */}
            <div className="forum-layout">
                <div style={{ display: 'grid', gap: 12 }} className="forum-feed">
                    {loading ? (
                        <div className="loader"><div className="spinner" /></div>
                    ) : threads.length === 0 ? (
                        <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
                            <h3 style={{ color: 'var(--text-muted)' }}>No discussions found in this category.</h3>
                            <p>Be the first to start a conversation!</p>
                        </div>
                    ) : (
                        threads.map((t: any) => (
                            <div key={t.id} className="reddit-card">
                                <div className="vote-sidebar">
                                    <button className="vote-arrow" style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem', color: 'var(--text-muted)' }}>▲</button>
                                    <div className="vote-count">{t.upvotes - t.downvotes}</div>
                                    <button className="vote-arrow" style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1.2rem', color: 'var(--text-muted)' }}>▼</button>
                                </div>
                                <div className="reddit-content">
                                    <div className="thread-meta">
                                        <span className="badge badge-primary" style={{ fontSize: '0.65rem', padding: '2px 8px' }}>{t.category}</span>
                                        <span>•</span>
                                        <span>Posted by <strong>u/{t.author?.name || 'anonymous'}</strong></span>
                                        <span>•</span>
                                        <span>{new Date(t.created_at).toLocaleDateString()}</span>
                                    </div>
                                    <Link to={`/forum/${t.id}`} style={{ textDecoration: 'none' }}>
                                        <h3 className="thread-title" style={{ margin: '4px 0 8px 0', fontSize: '1.25rem', fontWeight: 700 }}>{t.title}</h3>
                                    </Link>
                                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginBottom: 12, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                                        {t.content}
                                    </p>
                                    <div className="thread-actions">
                                        <Link to={`/forum/${t.id}`} className="action-item" style={{ textDecoration: 'none', color: 'inherit' }}>
                                            💬 {t.comment_count} Comments
                                        </Link>
                                        <div className="action-item" onClick={(e) => { e.preventDefault(); /* handleVote('upvote') */ }}>⬆️ Upvote</div>
                                        <div className="action-item" onClick={(e) => { e.preventDefault(); /* handleVote('downvote') */ }}>⬇️ Downvote</div>
                                        <div className="action-item">🔗 Share</div>
                                    </div>
                                </div>
                            </div>
                        ))
                    )}
                </div>

                {/* Sidebar */}
                <div className="hide-mobile">
                    <div className="card" style={{ position: 'sticky', top: 100 }}>
                        <h3 style={{ fontSize: '1.1rem', marginBottom: 16 }}>Popular Categories</h3>
                        <div style={{ display: 'grid', gap: 8 }}>
                            {['', 'governance', 'corruption', 'development', 'budget', 'general'].map(c => (
                                <button
                                    key={c}
                                    onClick={() => setCategory(c)}
                                    style={{
                                        textAlign: 'left',
                                        padding: '10px 16px',
                                        borderRadius: 8,
                                        border: '1px solid var(--border-color)',
                                        background: category === c ? 'var(--primary)' : 'transparent',
                                        color: category === c ? 'white' : 'var(--text-main)',
                                        fontWeight: 600,
                                        cursor: 'pointer',
                                        transition: 'all 0.2s'
                                    }}
                                >
                                    {c ? (c === 'governance' ? '🏛️ ' : c === 'corruption' ? '⚖️ ' : c === 'development' ? '🏗️ ' : c === 'budget' ? '💰 ' : '💬 ') + c.charAt(0).toUpperCase() + c.slice(1) : '🏠 All Topics'}
                                </button>
                            ))}
                        </div>
                        <div style={{ marginTop: 24, padding: 16, background: 'var(--bg-body)', borderRadius: 8, fontSize: '0.85rem' }}>
                            <div style={{ fontWeight: 800, marginBottom: 8, color: 'var(--primary)' }}>COMMUNITY RULES</div>
                            <ol style={{ paddingLeft: 16, color: 'var(--text-muted)' }}>
                                <li>Be respectful and constructive.</li>
                                <li>Share verified information only.</li>
                                <li>No spam or self-promotion.</li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
