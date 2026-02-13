import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false)
    const { isAuthenticated, user, logout } = useAuthStore()
    const location = useLocation()
    const [scrolled, setScrolled] = useState(false)
    const [theme, setTheme] = useState(localStorage.getItem('theme') || 'light')

    useEffect(() => {
        const handleScroll = () => setScrolled(window.scrollY > 10)
        window.addEventListener('scroll', handleScroll)
        return () => window.removeEventListener('scroll', handleScroll)
    }, [])

    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme)
        localStorage.setItem('theme', theme)
    }, [theme])

    const toggleTheme = () => {
        setTheme(prev => prev === 'light' ? 'dark' : 'light')
    }

    const navLinks = [
        { name: 'Projects', path: '/projects' },
        { name: 'Budget', path: '/budget' },
        { name: 'Reports', path: '/reports' },
        { name: 'Tenders', path: '/tenders' },
        { name: 'Forum', path: '/forum' },
        { name: 'Laws', path: '/laws' },
    ]

    return (
        <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
            <div className="page-container" style={{ padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', minHeight: 'auto' }}>
                <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 14, textDecoration: 'none' }}>
                    <img src="/assets/logo.jpg" alt="Sachet Logo" style={{ height: 48, borderRadius: 6, border: '1px solid var(--border-color)' }} />
                    <div>
                        <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--primary)', lineHeight: 1, letterSpacing: '-0.5px' }}>SACHET</div>
                        <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--text-muted)', letterSpacing: 2, marginTop: 2 }}>NEPAL</div>
                    </div>
                </Link>

                {/* Desktop Nav */}
                <div style={{ display: 'flex', gap: 6, alignItems: 'center' }} className="desktop-menu">
                    {navLinks.map(link => (
                        <Link key={link.path} to={link.path} className={`nav-link ${location.pathname === link.path ? 'active' : ''}`}>
                            {link.name}
                        </Link>
                    ))}

                    <div style={{ width: 1, height: 24, background: 'var(--border-color)', margin: '0 12px' }} />

                    <button
                        onClick={toggleTheme}
                        className="btn btn-outline"
                        style={{ width: 40, height: 40, padding: 0, borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
                        title={`Switch to ${theme === 'light' ? 'Dark' : 'Light'} Mode`}
                    >
                        {theme === 'light' ? '🌙' : '☀️'}
                    </button>

                    <div style={{ width: 1, height: 24, background: 'var(--border-color)', margin: '0 12px' }} />

                    {isAuthenticated ? (
                        <div style={{ display: 'flex', gap: 16, alignItems: 'center' }}>
                            <div style={{ textAlign: 'right' }}>
                                <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--primary)' }}>{user?.name}</div>
                                <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{user?.role?.toUpperCase()}</div>
                            </div>
                            <button className="btn btn-outline" style={{ padding: '6px 14px', fontSize: '0.8rem', height: 36 }} onClick={logout}>Sign Out</button>
                        </div>
                    ) : (
                        <div style={{ display: 'flex', gap: 12 }}>
                            <Link to="/login" className="nav-link" style={{ alignSelf: 'center' }}>Log In</Link>
                            <Link to="/register" className="btn btn-primary" style={{ padding: '8px 20px', fontSize: '0.9rem' }}>Join Now</Link>
                        </div>
                    )}
                </div>

                {/* Mobile Toggle */}
                <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
                    <button
                        onClick={toggleTheme}
                        className="mobile-show btn btn-outline"
                        style={{ width: 36, height: 36, padding: 0, borderRadius: '50%', display: 'none' }}
                    >
                        {theme === 'light' ? '🌙' : '☀️'}
                    </button>
                    <button className="mobile-toggle" onClick={() => setIsOpen(!isOpen)} style={{ display: 'none', background: 'none', border: 'none', fontSize: '1.8rem', cursor: 'pointer', color: 'var(--primary)' }}>
                        {isOpen ? '✕' : '☰'}
                    </button>
                </div>
            </div>

            {isOpen && (
                <div style={{
                    padding: '24px 20px',
                    background: 'var(--bg-card)',
                    borderBottom: '1px solid var(--border-color)',
                    display: 'grid',
                    gap: 16,
                    position: 'absolute',
                    top: '100%',
                    left: 0,
                    right: 0,
                    zIndex: 1001,
                    boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)'
                }} className="mobile-menu-overlay animate-fade-in-up">
                    {navLinks.map(link => (
                        <Link key={link.path} to={link.path} className={`nav-link ${location.pathname === link.path ? 'active' : ''}`} onClick={() => setIsOpen(false)} style={{ fontSize: '1rem', padding: '12px 16px' }}>
                            {link.name}
                        </Link>
                    ))}
                    <hr style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '8px 0' }} />
                    {isAuthenticated ? (
                        <div style={{ display: 'grid', gap: 12 }}>
                            <div style={{ padding: '0 16px', fontSize: '0.9rem' }}>
                                <div style={{ fontWeight: 800 }}>{user?.name}</div>
                                <div style={{ color: 'var(--text-muted)' }}>{user?.role?.toUpperCase()}</div>
                            </div>
                            <button className="btn btn-primary" onClick={() => { logout(); setIsOpen(false); }}>Sign Out</button>
                        </div>
                    ) : (
                        <div style={{ display: 'grid', gap: 12 }}>
                            <Link to="/login" className="btn btn-outline" onClick={() => setIsOpen(false)}>Log In</Link>
                            <Link to="/register" className="btn btn-primary" onClick={() => setIsOpen(false)}>Join Sachet</Link>
                        </div>
                    )}
                </div>
            )}

            <style>{`
        @media (max-width: 1024px) {
          .desktop-menu { display: none !important; }
          .mobile-toggle { display: block !important; }
          .mobile-show { display: flex !important; }
        }
        .navbar.scrolled { box-shadow: var(--shadow); }
      `}</style>
        </nav>
    )
}
