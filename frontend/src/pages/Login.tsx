import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import authService from '../services/auth.service'

export default function Login() {
    const [credentials, setCredentials] = useState({ email: '', password: '' })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const { setToken, setUser } = useAuthStore()
    const navigate = useNavigate()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setLoading(true)
        setError('')
        try {
            const res = await authService.login(credentials.email, credentials.password)
            setToken(res.access_token)
            setUser(res.user)
            navigate('/forum')
        } catch (err: any) {
            setError(err.response?.data?.message || 'Login failed. Please check your credentials.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
            <div className="card animate-fade-in-up" style={{ width: '100%', maxWidth: 450, padding: 40 }}>
                <div style={{ textAlign: 'center', marginBottom: 32 }}>
                    <img src="/assets/logo.jpg" alt="Logo" style={{ height: 60, marginBottom: 16, borderRadius: 8 }} />
                    <h2 style={{ fontSize: '1.75rem' }}>Individual Sign In</h2>
                    <p style={{ color: 'var(--text-muted)' }}>Secure access to Sachet Nepal</p>
                </div>

                {error && <div style={{ background: 'rgba(239, 68, 68, 0.1)', color: 'var(--danger)', padding: 12, borderRadius: 8, marginBottom: 20, fontSize: '0.85rem', textAlign: 'center' }}>{error}</div>}

                <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 20 }}>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Email Address</label>
                        <input
                            type="email"
                            className="input"
                            placeholder="name@organization.np"
                            value={credentials.email}
                            onChange={e => setCredentials({ ...credentials, email: e.target.value })}
                            required
                        />
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Password</label>
                        <input
                            type="password"
                            className="input"
                            placeholder="••••••••"
                            value={credentials.password}
                            onChange={e => setCredentials({ ...credentials, password: e.target.value })}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary" style={{ height: 48, marginTop: 10 }} disabled={loading}>
                        {loading ? 'Authenticating...' : 'Sign In'}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: 32, fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                    New to the platform? <Link to="/register" style={{ color: 'var(--primary)', fontWeight: 700 }}>Citizen Registration</Link>
                </div>

                <div style={{ marginTop: 24, padding: '16px', background: 'var(--bg-body)', borderRadius: 8, fontSize: '0.8rem' }}>
                    <strong>Demo Citizens:</strong><br />
                    demo@sachet.np / Password123!
                </div>
            </div>
        </div>
    )
}
