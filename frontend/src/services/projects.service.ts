import api from './api'

const projectsService = {
    async getAll(params?: { page?: number; status?: string; category?: string; district?: string; province?: string }) {
        const { data } = await api.get('/projects', { params })
        return data
    },

    async getById(id: string) {
        const { data } = await api.get(`/projects/${id}`)
        return data
    },

    async getStats() {
        const { data } = await api.get('/projects/stats')
        return data
    },
}

export default projectsService
