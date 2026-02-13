import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import projectsService from '../services/projects.service'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix Leaflet icon issue
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
    iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
    iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

export default function Projects() {
    const [data, setData] = useState<any>({ projects: [], total: 0 })
    const [loading, setLoading] = useState(true)
    const [statusFilter, setStatusFilter] = useState('')
    const [viewMode, setViewMode] = useState<'grid' | 'map'>('grid')

    useEffect(() => {
        setLoading(true)
        projectsService.getAll({ status: statusFilter || undefined })
            .then(setData)
            .catch(() => { })
            .finally(() => setLoading(false))
    }, [statusFilter])

    const statusBadge = (status: string) => {
        const mapBadge: Record<string, string> = {
            completed: 'badge-success', ongoing: 'badge-info',
            delayed: 'badge-danger', inactive: 'badge-primary',
        }
        return mapBadge[status] || 'badge-primary'
    }

    const formatBudget = (n: number) => {
        if (!n) return 'N/A'
        if (n >= 1e9) return `रु ${(n / 1e9).toFixed(1)}B`
        if (n >= 1e6) return `रु ${(n / 1e6).toFixed(0)}M`
        return `रु ${n.toLocaleString()}`
    }

    return (
        <div className="page-container">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'end', marginBottom: 40, flexWrap: 'wrap', gap: 20 }} className="mobile-stack">
                <div>
                    <h1 className="page-title">National Pride Projects</h1>
                    <p className="page-subtitle" style={{ marginBottom: 0 }}>Monitoring critical infrastructure and development works across Nepal.</p>
                </div>
                <div className="tab-list">
                    <button className={`tab-btn ${viewMode === 'grid' ? 'active' : ''}`} onClick={() => setViewMode('grid')}>📋 List View</button>
                    <button className={`tab-btn ${viewMode === 'map' ? 'active' : ''}`} onClick={() => setViewMode('map')}>🗺️ Map View</button>
                </div>
            </div>

            {/* Filters */}
            <div className="card" style={{ marginBottom: 32, padding: '16px 24px' }}>
                <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
                    <span style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--primary)', textTransform: 'uppercase' }}>Filter by Status:</span>
                    {['', 'ongoing', 'completed', 'delayed', 'inactive'].map(s => (
                        <button key={s} className={`tab-btn ${statusFilter === s ? 'active' : ''}`}
                            onClick={() => setStatusFilter(s)} style={{ fontSize: '0.85rem' }}>
                            {s ? s.charAt(0).toUpperCase() + s.slice(1) : 'All Projects'}
                        </button>
                    ))}
                </div>
            </div>

            {loading ? (
                <div className="loader" style={{ display: 'flex', justifyContent: 'center', padding: '100px 0' }}>
                    <div className="spinner" style={{ width: 40, height: 40, border: '4px solid var(--border-color)', borderTop: '4px solid var(--primary)', borderRadius: '50%', animation: 'spin 1s linear infinite' }} />
                </div>
            ) : data.projects.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '80px 20px' }}>
                    <div style={{ fontSize: '3rem', marginBottom: 16 }}>🔎</div>
                    <h3>No projects matching your search</h3>
                    <p style={{ color: 'var(--text-muted)' }}>Try adjusting your filters to see more results.</p>
                </div>
            ) : viewMode === 'map' ? (
                <div className="card" style={{ height: '600px', padding: 0, overflow: 'hidden' }}>
                    <MapContainer center={[28.3949, 84.124]} zoom={7} style={{ height: '100%', width: '100%' }}>
                        <TileLayer
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        />
                        {data.projects.map((p: any) => p.latitude && p.longitude && (
                            <Marker key={p.id} position={[p.latitude, p.longitude]}>
                                <Popup>
                                    <div style={{ color: 'var(--text-main)', padding: 4 }}>
                                        <h4 style={{ fontSize: '1rem', color: 'var(--primary)', marginBottom: 8 }}>{p.title}</h4>
                                        <span className={`badge ${statusBadge(p.status)}`}>{p.status}</span>
                                        <div style={{ marginTop: 12, fontSize: '0.85rem' }}>
                                            <strong>Budget:</strong> {formatBudget(p.budget)}<br />
                                            <strong>Department:</strong> {p.department}
                                        </div>
                                    </div>
                                </Popup>
                            </Marker>
                        ))}
                    </MapContainer>
                </div>
            ) : (
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(min(100%, 350px), 1fr))', gap: 24 }}>
                    {data.projects.map((p: any) => (
                        <div key={p.id} className="card">
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 16 }}>
                                <span className={`badge ${statusBadge(p.status)}`}>{p.status}</span>
                                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 600 }}>#{p.category}</span>
                            </div>
                            <h3 style={{ fontSize: '1.2rem', marginBottom: 12, lineHeight: 1.4 }}>{p.title}</h3>
                            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginBottom: 20, display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical', overflow: 'hidden' }}>
                                {p.description}
                            </p>

                            <div style={{ padding: '16px 0', borderTop: '1px solid var(--border-color)', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
                                <div>
                                    <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>Allocated Budget</div>
                                    <div style={{ fontWeight: 800, color: 'var(--primary)' }}>{formatBudget(p.budget)}</div>
                                </div>
                                <div>
                                    <div style={{ fontSize: '0.7rem', textTransform: 'uppercase', color: 'var(--text-muted)', fontWeight: 700 }}>Responsible Dept</div>
                                    <div style={{ fontWeight: 700, color: 'var(--text-main)', fontSize: '0.8rem' }}>{p.department}</div>
                                </div>
                            </div>

                            <Link to={`/projects/${p.id}`} className="btn btn-primary" style={{ width: '100%', marginTop: 16 }}>View Full Details</Link>
                        </div>
                    ))}
                </div>
            )}

            <style>{`
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
      `}</style>
        </div>
    )
}
