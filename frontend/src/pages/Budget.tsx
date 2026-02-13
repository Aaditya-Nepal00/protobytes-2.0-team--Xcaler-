import { useEffect, useState } from 'react'
import budgetService from '../services/budget.service'
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js'
import { Doughnut, Bar } from 'react-chartjs-2'

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement)

export default function Budget() {
    const [summary, setSummary] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        budgetService.getSummary()
            .then(setSummary)
            .catch(() => { })
            .finally(() => setLoading(false))
    }, [])

    const formatAmount = (n: number) => {
        if (!n) return '0'
        if (n >= 1e9) return `रु ${(n / 1e9).toFixed(1)} Arba`
        if (n >= 1e6) return `रु ${(n / 1e6).toFixed(0)} Karod`
        return `रु ${n.toLocaleString()}`
    }

    const sectorColors: Record<string, string> = {
        education: '#1a2a4e', health: '#ef4444', infrastructure: '#f5a623',
        agriculture: '#10b981', energy: '#3b82f6', defense: '#64748b',
        tourism: '#8b5cf6', 'social welfare': '#ec4899',
    }

    const chartData = summary ? {
        labels: Object.keys(summary.sectors).map(s => s.charAt(0).toUpperCase() + s.slice(1)),
        datasets: [{
            data: Object.values(summary.sectors).map((s: any) => s.allocated),
            backgroundColor: Object.keys(summary.sectors).map(s => sectorColors[s] || '#1a2a4e'),
            borderWidth: 2,
            borderColor: 'white',
        }]
    } : null

    const barData = summary ? {
        labels: Object.keys(summary.sectors).map(s => s.charAt(0).toUpperCase() + s.slice(1)),
        datasets: [
            {
                label: 'Allocated',
                data: Object.values(summary.sectors).map((s: any) => s.allocated / 1e9),
                backgroundColor: '#1a2a4e',
            },
            {
                label: 'Spent',
                data: Object.values(summary.sectors).map((s: any) => s.spent / 1e9),
                backgroundColor: '#f5a623',
            }
        ]
    } : null

    return (
        <div className="page-container">
            <div style={{ marginBottom: 48 }} className="mobile-stack">
                <h1 className="page-title">National Budget Overview</h1>
                <p className="page-subtitle">Visualizing the flow of public funds across ministries and national sectors.</p>
            </div>

            {loading ? (
                <div className="loader"><div className="spinner" /></div>
            ) : !summary ? (
                <div className="card" style={{ textAlign: 'center', padding: 80 }}>
                    <p>No budget data available currently.</p>
                </div>
            ) : (
                <>
                    {/* Overview Cards */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 24, marginBottom: 40 }}>
                        {[
                            { label: 'Fiscal Year', value: summary.fiscal_year, sub: 'Current Operating Year' },
                            { label: 'Total Allocated', value: formatAmount(summary.total_allocated), sub: 'Approved Budget' },
                            { label: 'Total Spent', value: formatAmount(summary.total_spent), sub: 'Actual Expenditure' },
                            { label: 'Avg Utilization', value: summary.utilization_rate + '%', sub: 'Spending Efficiency' }
                        ].map((item, i) => (
                            <div key={i} className="card animate-fade-in-up" style={{ padding: 24, background: i === 0 ? 'var(--primary)' : 'var(--bg-card)' }}>
                                <div style={{ color: i === 0 ? 'rgba(255,255,255,0.7)' : 'var(--text-muted)', fontSize: '0.75rem', fontWeight: 700, textTransform: 'uppercase' }}>{item.label}</div>
                                <div style={{ fontSize: '1.5rem', fontWeight: 800, color: i === 0 ? 'white' : 'var(--primary)', margin: '8px 0' }}>{item.value}</div>
                                <div style={{ fontSize: '0.8rem', color: i === 0 ? 'rgba(255,255,255,0.6)' : 'var(--text-muted)' }}>{item.sub}</div>
                            </div>
                        ))}
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: 32, marginBottom: 60 }}>
                        <div className="card">
                            <h3 style={{ marginBottom: 24, fontSize: '1.2rem' }}>Sector Allocation Analysis</h3>
                            <div style={{ height: 350, display: 'flex', justifyContent: 'center' }}>
                                {chartData && <Doughnut data={chartData} options={{ maintainAspectRatio: false, plugins: { legend: { position: 'right' } } }} />}
                            </div>
                        </div>
                        <div className="card">
                            <h3 style={{ marginBottom: 24, fontSize: '1.2rem' }}>Allocation vs Actual Spending (Billion NPR)</h3>
                            <div style={{ height: 350 }}>
                                {barData && <Bar data={barData} options={{ maintainAspectRatio: false }} />}
                            </div>
                        </div>
                    </div>

                    {/* Sector Breakdown Table */}
                    <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
                        <div style={{ padding: '20px 24px', background: 'var(--bg-body)', borderBottom: '1px solid var(--border-color)', fontWeight: 700, color: 'var(--primary)' }}>
                            Detailed Sector Breakdown
                        </div>
                        <div style={{ overflowX: 'auto' }}>
                            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                                <thead>
                                    <tr style={{ borderBottom: '1px solid var(--border-color)' }}>
                                        <th style={{ padding: '16px 24px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>Sector Name</th>
                                        <th style={{ padding: '16px 24px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>Allocated</th>
                                        <th style={{ padding: '16px 24px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>Spent</th>
                                        <th style={{ padding: '16px 24px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>Progress</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {Object.entries(summary.sectors || {}).map(([sector, data]: [string, any], i) => (
                                        <tr key={sector} style={{ borderBottom: i === Object.keys(summary.sectors).length - 1 ? 'none' : '1px solid var(--border-color)' }}>
                                            <td style={{ padding: '16px 24px', fontWeight: 600, color: 'var(--primary)', textTransform: 'capitalize' }}>{sector}</td>
                                            <td style={{ padding: '16px 24px' }}>{formatAmount(data.allocated)}</td>
                                            <td style={{ padding: '16px 24px' }}>{formatAmount(data.spent)}</td>
                                            <td style={{ padding: '16px 24px' }}>
                                                <div style={{ width: 140 }}>
                                                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.7rem', marginBottom: 4 }}>
                                                        <span>{((data.spent / data.allocated) * 100).toFixed(0)}% Utilized</span>
                                                    </div>
                                                    <div style={{ height: 6, background: 'var(--border-color)', borderRadius: 3, overflow: 'hidden' }}>
                                                        <div style={{ height: '100%', width: `${(data.spent / data.allocated) * 100}%`, background: sectorColors[sector] || 'var(--primary)' }} />
                                                    </div>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </>
            )}
        </div>
    )
}
