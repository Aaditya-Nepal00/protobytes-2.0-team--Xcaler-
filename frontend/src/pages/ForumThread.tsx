import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import forumService from '../services/forum.service'
import { useAuthStore } from '../store/authStore'

export default function ForumThread() {
    const { threadId } = useParams()
    const [thread, setThread] = useState<any>(null)
    const [loading, setLoading] = useState(true)
    const [commentContent, setCommentContent] = useState('')
    const { isAuthenticated, user } = useAuthStore()

    useEffect(() => {
        if (threadId) {
            forumService.getThread(threadId)
                .then(setThread)
                .catch(() => { })
                .finally(() => setLoading(false))
        }
    }, [threadId])

    const handlePostComment = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!threadId || !commentContent) return
        try {
            await forumService.createComment(threadId, { content: commentContent })
            setCommentContent('')
            // Refresh
            const updated = await forumService.getThread(threadId)
            setThread(updated)
        } catch (err) {
            alert('Failed to post comment.')
        }
    }

    const handleVote = async (type: 'upvote' | 'downvote') => {
        if (!threadId || !isAuthenticated) return
        try {
            await forumService.voteThread(threadId, type)
            const updated = await forumService.getThread(threadId)
            setThread(updated)
        } catch (err) { }
    }

    if (loading) return <div className="page-container"><div className="loader"><div className="spinner" /></div></div>
    if (!thread) return <div className="page-container"><h1>Thread not found</h1></div>

    return (
        <div className="page-container" style={{ maxWidth: 1000 }}>
            <Link to="/forum" style={{ display: 'inline-flex', alignItems: 'center', gap: 8, textDecoration: 'none', color: 'var(--text-muted)', marginBottom: 24, fontWeight: 700, fontSize: '0.9rem' }}>
                ← Back to Community
            </Link>

            <div className="reddit-card" style={{ marginBottom: 24, padding: '0 0 16px 0' }}>
                <div className="vote-sidebar" style={{ background: 'var(--bg-card)', borderRight: '1px solid var(--border-color)' }}>
                    <button onClick={() => handleVote('upvote')} style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', color: thread.user_vote === 'upvote' ? 'var(--accent)' : 'var(--text-muted)' }}>▲</button>
                    <div className="vote-count" style={{ fontSize: '1rem' }}>{thread.upvotes - thread.downvotes}</div>
                    <button onClick={() => handleVote('downvote')} style={{ background: 'none', border: 'none', fontSize: '1.5rem', cursor: 'pointer', color: thread.user_vote === 'downvote' ? 'var(--danger)' : 'var(--text-muted)' }}>▼</button>
                </div>
                <div className="reddit-content">
                    <div className="thread-meta">
                        <span className="badge badge-primary">{thread.category}</span>
                        <span>•</span>
                        <span>Posted by <strong>u/{thread.author?.name}</strong></span>
                        <span>•</span>
                        <span>{new Date(thread.created_at).toLocaleString()}</span>
                    </div>
                    <h1 className="thread-title-main">{thread.title}</h1>
                    <div className="thread-body">
                        {thread.content}
                    </div>
                    <div className="thread-actions" style={{ borderTop: '1px solid var(--border-color)', paddingTop: 16 }}>
                        <div className="action-item">💬 {thread.comment_count} Comments</div>
                        <div className="action-item" onClick={() => handleVote('upvote')} style={{ color: thread.user_vote === 'upvote' ? 'var(--accent)' : 'inherit' }}>⬆️ Upvote</div>
                        <div className="action-item" onClick={() => handleVote('downvote')} style={{ color: thread.user_vote === 'downvote' ? 'var(--danger)' : 'inherit' }}>⬇️ Downvote</div>
                        <div className="action-item">🔗 Share</div>
                    </div>
                </div>
            </div>

            {/* Comment Section */}
            <div className="card comment-section">
                <h3 className="section-title">Discussion ({thread.comment_count})</h3>
                {isAuthenticated ? (
                    <form onSubmit={handlePostComment} style={{ marginBottom: 40 }}>
                        <textarea
                            className="input"
                            style={{ minHeight: 120, marginBottom: 12, borderRadius: 8 }}
                            placeholder="What are your thoughts?"
                            value={commentContent}
                            onChange={e => setCommentContent(e.target.value)}
                            required
                        />
                        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <button type="submit" className="btn btn-primary" style={{ borderRadius: 8, padding: '10px 32px' }}>Comment</button>
                        </div>
                    </form>
                ) : (
                    <div style={{ textAlign: 'center', padding: 24, marginBottom: 40, border: '1px dashed var(--border-color)', borderRadius: 12 }}>
                        <p style={{ marginBottom: 16 }}>Log in or sign up to leave a comment</p>
                        <div style={{ display: 'flex', gap: 12, justifyContent: 'center' }}>
                            <Link to="/login" className="btn btn-outline" style={{ borderRadius: 8 }}>Log In</Link>
                            <Link to="/register" className="btn btn-primary" style={{ borderRadius: 8 }}>Sign Up</Link>
                        </div>
                    </div>
                )}

                <div style={{ display: 'grid', gap: 32 }}>
                    {thread.comments?.map((comment: any) => (
                        <div key={comment.id} style={{ display: 'flex', gap: 16 }}>
                            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                                <div style={{ width: 32, height: 32, borderRadius: '50%', background: 'var(--primary)', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '0.8rem' }}>
                                    {comment.author?.name?.charAt(0) || 'A'}
                                </div>
                                <div style={{ flex: 1, width: 2, background: 'var(--border-color)', margin: '8px 0' }} />
                            </div>
                            <div style={{ flex: 1 }}>
                                <div style={{ fontSize: '0.85rem', marginBottom: 8 }}>
                                    <strong>u/{comment.author?.name || 'anonymous'}</strong> • <span style={{ color: 'var(--text-muted)' }}>{new Date(comment.created_at).toLocaleDateString()}</span>
                                </div>
                                <div style={{ color: 'var(--text-main)', lineHeight: 1.5, marginBottom: 12 }}>{comment.content}</div>
                                <div style={{ display: 'flex', gap: 16, fontSize: '0.85rem', fontWeight: 700, alignItems: 'center' }}>
                                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, background: 'var(--bg-body)', padding: '4px 12px', borderRadius: 20 }}>
                                        <span style={{ cursor: 'pointer', color: 'var(--text-muted)' }} onClick={() => forumService.voteComment(comment.id, 'upvote')}>▲</span>
                                        <span style={{ minWidth: 20, textAlign: 'center' }}>{comment.upvotes - comment.downvotes}</span>
                                        <span style={{ cursor: 'pointer', color: 'var(--text-muted)' }} onClick={() => forumService.voteComment(comment.id, 'downvote')}>▼</span>
                                    </div>
                                    <span style={{ cursor: 'pointer', color: 'var(--text-muted)' }}>Reply</span>
                                    <span style={{ cursor: 'pointer', color: 'var(--text-muted)' }}>Share</span>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}
