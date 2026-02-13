import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import projectsService from '../services/projects.service'
import corruptionService from '../services/corruption.service'

export default function Home() {
    const [stats, setStats] = useState({
        projects: 12,
        reports: 45,
        citizens: 1250,
        transparency: 94
    })

    useEffect(() => {
        // Fetch live stats
        Promise.all([
            projectsService.getStats().catch(() => ({ total_projects: 12 })),
            corruptionService.getStats().catch(() => ({ total_reports: 45 }))
        ]).then(([pStats, cStats]: any) => {
            setStats(prev => ({
                ...prev,
                projects: pStats.total_projects || 12,
                reports: cStats.total_reports || 45
            }))
        })
    }, [])

    return (
        <div className="home-page">
            {/* Hero Section */}
            <section className="section hero-section" style={{ background: 'var(--bg-card)', borderBottom: '1px solid var(--border-color)', padding: '80px 0' }}>
                <div className="page-container" style={{ textAlign: 'center' }}>
                    <div className="animate-fade-in-up">
                        <span className="badge badge-primary" style={{ marginBottom: 16 }}>Official Transparency Portal of Nepal</span>
                        <h1 className="hero-title">
                            Empowering Citizens through <span className="text-gradient">Transparency</span>
                        </h1>
                        <p className="hero-subtitle">
                            Sachet is Nepal's dedicated platform for monitoring government projects,
                            tracking public spending, and reporting corruption with security.
                        </p>
                        <div className="hero-actions mobile-stack">
                            <Link to="/reports" className="btn btn-primary btn-lg">
                                Report an Issue
                            </Link>
                            <Link to="/projects" className="btn btn-outline btn-lg">
                                Explore Projects
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Stats Dashboard */}
            <section className="section" style={{ marginTop: -50 }}>
                <div className="page-container">
                    <div className="card-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 24 }}>
                        {[
                            { label: 'Active Projects', value: stats.projects, icon: '🏗️', color: 'var(--info)' },
                            { label: 'Corruption Reports', value: stats.reports, icon: '🔍', color: 'var(--danger)' },
                            { label: 'Verified Citizens', value: stats.citizens + '+', icon: '👥', color: 'var(--primary)' },
                            { label: 'Transparency Score', value: stats.transparency + '%', icon: '📈', color: 'var(--success)' },
                        ].map((stat, i) => (
                            <div key={i} className="card animate-fade-in-up" style={{ padding: 32, textAlign: 'center', borderBottom: `4px solid ${stat.color}` }}>
                                <div style={{ fontSize: '2.5rem', marginBottom: 12 }}>{stat.icon}</div>
                                <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--primary)', marginBottom: 4 }}>{stat.value}</div>
                                <div style={{ fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', fontSize: '0.8rem', letterSpacing: 1 }}>{stat.label}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section >

            {/* Core Features */}
            < section className="section" >
                <div className="page-container">
                    <div style={{ textAlign: 'center', marginBottom: 60 }}>
                        <h2 style={{ fontSize: '2.25rem', marginBottom: 16 }}>Everything you need for civic oversight</h2>
                        <p style={{ color: 'var(--text-muted)', maxWidth: 600, margin: '0 auto' }}>
                            Real-time data feeds and simplified legal tools to keep you informed and empowered.
                        </p>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: 32 }}>
                        <div className="card">
                            <h3 style={{ marginBottom: 12 }}>💰 Budget Tracking</h3>
                            <p style={{ color: 'var(--text-muted)', marginBottom: 20 }}>Detailed breakdown of annual budgets, sector allocations, and historical spending data for all ministries.</p>
                            <Link to="/budget" className="btn btn-outline" style={{ border: 'none', paddingLeft: 0 }}>View Budget Analysis →</Link>
                        </div>
                        <div className="card">
                            <h3 style={{ marginBottom: 12 }}>⚖️ Simplified Laws</h3>
                            <p style={{ color: 'var(--text-muted)', marginBottom: 20 }}>Government acts and policies translated into simple terms. Know your rights without the legal jargon.</p>
                            <Link to="/laws" className="btn btn-outline" style={{ border: 'none', paddingLeft: 0 }}>Browse Knowledge Hub →</Link>
                        </div >
                        <div className="card">
                            <h3 style={{ marginBottom: 12 }}>💬 Community Forum</h3>
                            <p style={{ color: 'var(--text-muted)', marginBottom: 20 }}>Participate in organized discussions on local issues, policy changes, and national development projects.</p>
                            <Link to="/forum" className="btn btn-outline" style={{ border: 'none', paddingLeft: 0 }}>Join Discussion →</Link>
                        </div >
                    </div >
                </div >
            </section >

            {/* CTA Section */}
            < section className="section" style={{ background: 'var(--primary)', color: 'white', textAlign: 'center' }
            }>
                <div className="page-container" style={{ padding: '80px 20px' }}>
                    <h2 style={{ color: 'white', fontSize: '2.5rem', marginBottom: 24 }}>Be the change Nepal needs.</h2>
                    <p style={{ color: 'rgba(255,255,255,0.8)', fontSize: '1.25rem', maxWidth: 700, margin: '0 auto 40px' }}>
                        Your participation ensures that our government remains accountable and every rupee is spent for the people.
                    </p>
                    <Link to="/register" className="btn btn-accent btn-lg" style={{ padding: '16px 40px', fontSize: '1.2rem' }}>
                        Create Your Account
                    </Link>
                </div>
            </section >

            <style>{`
        .btn-lg { height: 56px; border-radius: 28px; }
      `}</style>
        </div >
    )
}
