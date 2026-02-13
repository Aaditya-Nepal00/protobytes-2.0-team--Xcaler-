import api from './api'

const tendersService = {
    async getAll(params?: { page?: number; status?: string; q?: string }) {
        const { data } = await api.get('/tenders', { params })
        return data
    },

    async getById(id: string) {
        const { data } = await api.get(`/tenders/${id}`)
        return data
    },

    async getStats() {
        const { data } = await api.get('/tenders/stats')
        return data
    },
}

export default tendersService
