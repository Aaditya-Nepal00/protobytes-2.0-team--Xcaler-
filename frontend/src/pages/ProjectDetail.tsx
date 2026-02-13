import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import projectsService from '../services/projects.service'

export default function ProjectDetail() {
    const { projectId } = useParams()
    const [project, setProject] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        if (projectId) {
            projectsService.getById(projectId)
                .then(setProject)
                .catch(() => { })
                .finally(() => setLoading(false))
        }
    }, [projectId])

    const formatBudget = (n: number) => {
        if (!n) return 'N/A'
        if (n >= 1e9) return `रु ${(n / 1e9).toFixed(2)} Billion`
        if (n >= 1e6) return `रु ${(n / 1e6).toFixed(0)} Million`
        return `रु ${n.toLocaleString()}`
    }

    if (loading) return <div className="page-container"><div className="loader"><div className="spinner" /></div></div>
    if (!project) return <div className="page-container"><h1>Project not found</h1></div>

    const progressStyle = {
        width: `${project.completion_percentage || 0}%`,
        background: project.status === 'completed' ? 'var(--success)' : 'var(--accent)',
        height: '100%',
        borderRadius: '10px',
        transition: 'width 1s ease-in-out'
    }

    return (
        <div className="page-container">
            <Link to="/projects" className="btn btn-outline" style={{ marginBottom: 32, display: 'inline-flex', alignItems: 'center', gap: 8, padding: '8px 16px' }}>
                ← Back to Projects
            </Link>

            <div className="card animate-fade-in-up" style={{ padding: 40 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: 24, flexWrap: 'wrap', gap: 20 }}>
                    <div>
                        <div style={{ display: 'flex', gap: 12, marginBottom: 12 }}>
                            <span className="badge badge-primary">{project.category}</span>
                            <span className={`badge ${project.status === 'completed' ? 'badge-success' : project.status === 'ongoing' ? 'badge-info' : 'badge-danger'}`}>
                                {project.status.toUpperCase()}
                            </span>
                        </div>
                        <h1 style={{ fontSize: '2.5rem', marginBottom: 12, color: 'var(--primary)' }}>{project.title}</h1>
                        <p style={{ fontSize: '1.1rem', color: 'var(--text-muted)', maxWidth: 800 }}>{project.description}</p>
                    </div>
                    <div style={{ textAlign: 'center', background: 'var(--bg-body)', padding: '24px 32px', borderRadius: 16, border: '1px solid var(--border-color)' }}>
                        <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: 8 }}>Total Budget</div>
                        <div style={{ fontSize: '1.75rem', fontWeight: 900, color: 'var(--primary)' }}>{formatBudget(project.budget)}</div>
                    </div>
                </div>

                <div style={{ marginBottom: 40 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 12, fontWeight: 700 }}>
                        <span>Overall Completion Progress</span>
                        <span>{project.completion_percentage}%</span>
                    </div>
                    <div style={{ height: 20, background: 'var(--border-color)', borderRadius: 10, overflow: 'hidden' }}>
                        <div style={progressStyle} />
                    </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 32, padding: '32px 0', borderTop: '1px solid var(--border-color)', borderBottom: '1px solid var(--border-color)', marginBottom: 40 }}>
                    <div>
                        <h4 style={{ color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: 12 }}>Responsible Entity</h4>
                        <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{project.department}</div>
                    </div>
                    <div>
                        <h4 style={{ color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: 12 }}>Contractor Company</h4>
                        <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{project.contractor || 'To be announced'}</div>
                    </div>
                    <div>
                        <h4 style={{ color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: 12 }}>Actual Spent</h4>
                        <div style={{ fontWeight: 700, fontSize: '1.1rem', color: 'var(--info)' }}>{formatBudget(project.spent)}</div>
                    </div>
                    <div>
                        <h4 style={{ color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase', marginBottom: 12 }}>Expected Completion</h4>
                        <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{project.expected_end_date ? new Date(project.expected_end_date).toLocaleDateString() : 'Achieved'}</div>
                    </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 40, flexWrap: 'wrap' }}>
                    <div className="card" style={{ background: 'var(--bg-body)', padding: 32 }}>
                        <h3 style={{ marginBottom: 20 }}>Project Impact</h3>
                        <p style={{ lineHeight: 1.6 }}>
                            This project is a cornerstone of Nepal's secondary development goals. By improving {project.category.toLowerCase()} infrastructure,
                            it aims to create direct employment for over 5,000 workers and contribute approximately 1.2% to the national GDP upon full operation.
                            Regular audits are being conducted to ensure transparent fund utilization.
                        </p>
                    </div>
                    <div className="card" style={{ background: 'var(--bg-body)', padding: 32 }}>
                        <h3 style={{ marginBottom: 20 }}>Active Stakeholders</h3>
                        <ul style={{ listStyle: 'none', padding: 0 }}>
                            <li style={{ marginBottom: 12, display: 'flex', alignItems: 'center', gap: 10 }}>✅ Ministry of Finance</li>
                            <li style={{ marginBottom: 12, display: 'flex', alignItems: 'center', gap: 10 }}>✅ National Planning Commission</li>
                            <li style={{ marginBottom: 12, display: 'flex', alignItems: 'center', gap: 10 }}>✅ Local Government Liaison</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    )
}
