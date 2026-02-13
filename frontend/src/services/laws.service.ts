import api from './api'

const lawsService = {
    async getLaws(params?: { page?: number; per_page?: number; category?: string; search?: string }) {
        const { data } = await api.get('/laws', { params })
        return data
    },

    async getLawById(id: string) {
        const { data } = await api.get(`/laws/${id}`)
        return data
    },

    async getCategories() {
        const { data } = await api.get('/laws/categories')
        return data
    },
}

export default lawsService
