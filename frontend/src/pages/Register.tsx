import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'
import authService from '../services/auth.service'

export default function Register() {
    const [formData, setFormData] = useState({ name: '', email: '', password: '', confirm_password: '' })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()
    const { setToken, setUser } = useAuthStore()

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (formData.password !== formData.confirm_password) return setError('Passwords do not match')
        setLoading(true)
        setError('')
        try {
            const res = await authService.register(formData.email, formData.name, formData.password)
            setToken(res.access_token)
            setUser(res.user)
            navigate('/forum')
        } catch (err: any) {
            setError(err.response?.data?.message || 'Registration failed.')
        } finally {
            setLoading(false)
        }
    }

    const handleQuickDemo = async () => {
        setLoading(true)
        setError('')
        const demoEmail = `citizen_${Math.floor(Math.random() * 10000)}@demo.sachet.np`
        try {
            const res = await authService.register(demoEmail, "Demo Citizen", "Password123!")
            setToken(res.access_token)
            setUser(res.user)
            navigate('/forum')
        } catch (err) {
            setError('Quick registration failed. Try manual.')
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="page-container" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '80vh' }}>
            <div className="card animate-fade-in-up" style={{ width: '100%', maxWidth: 450, padding: 40 }}>
                <div style={{ textAlign: 'center', marginBottom: 32 }}>
                    <h2 style={{ fontSize: '1.75rem' }}>Join Sachet Nepal</h2>
                    <p style={{ color: 'var(--text-muted)' }}>Your platform for civic accountability</p>
                </div>

                {error && <div style={{ background: 'rgba(239, 68, 68, 0.1)', color: 'var(--danger)', padding: 12, borderRadius: 8, marginBottom: 20, fontSize: '0.85rem' }}>{error}</div>}

                <div style={{ marginBottom: 24 }}>
                    <button
                        onClick={handleQuickDemo}
                        className="btn btn-accent"
                        style={{ width: '100%', height: 48, fontWeight: 700 }}
                        disabled={loading}
                    >
                        ⚡ Create Quick Demo Account
                    </button>
                    <div style={{ textAlign: 'center', margin: '16px 0', color: 'var(--text-muted)', fontSize: '0.8rem' }}>— OR REGISTER MANUALLY —</div>
                </div>

                <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 16 }}>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Full Name</label>
                        <input className="input" placeholder="Aaditya Nepal" value={formData.name} onChange={e => setFormData({ ...formData, name: e.target.value })} required />
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Email Address</label>
                        <input className="input" type="email" placeholder="name@domain.com" value={formData.email} onChange={e => setFormData({ ...formData, email: e.target.value })} required />
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Password</label>
                        <input className="input" type="password" placeholder="••••••••" value={formData.password} onChange={e => setFormData({ ...formData, password: e.target.value })} required />
                    </div>
                    <div>
                        <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, marginBottom: 6 }}>Confirm Password</label>
                        <input className="input" type="password" value={formData.confirm_password} onChange={e => setFormData({ ...formData, confirm_password: e.target.value })} required />
                    </div>
                    <button type="submit" className="btn btn-primary" style={{ height: 48, marginTop: 10 }} disabled={loading}>
                        {loading ? 'Creating Account...' : 'Register'}
                    </button>
                </form>

                <div style={{ textAlign: 'center', marginTop: 32, fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                    Already have an account? <Link to="/login" style={{ color: 'var(--primary)', fontWeight: 700 }}>Sign In</Link>
                </div>
            </div>
        </div>
    )
}
