import api from './api'

export interface CorruptionReportPayload {
    title: string
    description: string
    department?: string
    district?: string
    province?: string
    category?: string
    severity?: string
    anonymous?: boolean
    location?: string
    amount_involved?: number
}

const corruptionService = {
    async getReports(params?: { page?: number; status?: string; severity?: string; category?: string }) {
        const { data } = await api.get('/corruption/reports', { params })
        return data
    },

    async submitReport(report: CorruptionReportPayload) {
        const { data } = await api.post('/corruption/reports', report)
        return data
    },

    async trackReport(trackingId: string) {
        const { data } = await api.get(`/corruption/reports/track/${trackingId}`)
        return data
    },

    async getStats() {
        const { data } = await api.get('/corruption/stats')
        return data
    },
}

export default corruptionService
