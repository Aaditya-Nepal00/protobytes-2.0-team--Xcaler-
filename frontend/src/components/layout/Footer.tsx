import { Link } from 'react-router-dom'

export default function Footer() {
    return (
        <footer style={{
            borderTop: '1px solid rgba(255,255,255,0.08)',
            padding: '40px 16px',
            marginTop: 60,
        }}>
            <div style={{
                maxWidth: 1280, margin: '0 auto',
                display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: 32,
            }}>
                <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 12 }}>
                        <span style={{ fontSize: 24 }}>🔎</span>
                        <span style={{ fontWeight: 800, fontSize: '1.1rem' }} className="gradient-text">Sachet</span>
                    </div>
                    <p style={{ color: '#64748b', fontSize: '0.85rem', lineHeight: 1.6 }}>
                        Empowering citizens with transparency and accountability tools for better governance in Nepal.
                    </p>
                </div>
                <div>
                    <h4 style={{ fontWeight: 700, fontSize: '0.85rem', marginBottom: 12, color: '#94a3b8' }}>PLATFORM</h4>
                    {[
                        { to: '/projects', label: 'Government Projects' },
                        { to: '/budget', label: 'Budget Tracker' },
                        { to: '/tenders', label: 'Tender Watch' },
                        { to: '/corruption', label: 'Report Corruption' },
                    ].map(l => (
                        <Link key={l.to} to={l.to} style={{
                            display: 'block', color: '#64748b', textDecoration: 'none',
                            fontSize: '0.85rem', padding: '4px 0', transition: 'color 0.2s',
                        }}>{l.label}</Link>
                    ))}
                </div>
                <div>
                    <h4 style={{ fontWeight: 700, fontSize: '0.85rem', marginBottom: 12, color: '#94a3b8' }}>RESOURCES</h4>
                    {[
                        { to: '/laws', label: 'Know Your Laws' },
                        { to: '/forum', label: 'Community Forum' },
                    ].map(l => (
                        <Link key={l.to} to={l.to} style={{
                            display: 'block', color: '#64748b', textDecoration: 'none',
                            fontSize: '0.85rem', padding: '4px 0',
                        }}>{l.label}</Link>
                    ))}
                </div>
            </div>
            <div style={{
                maxWidth: 1280, margin: '24px auto 0', paddingTop: 24,
                borderTop: '1px solid rgba(255,255,255,0.05)',
                textAlign: 'center', color: '#475569', fontSize: '0.8rem',
            }}>
                © 2026 Project Sachet · Made for Nepal 🇳🇵 · Hackathon 2026
            </div>
        </footer>
    )
}
