import api from './api'

const authService = {
    async login(email: string, password: string) {
        const { data } = await api.post('/auth/login', { email, password })
        return data
    },

    async register(email: string, name: string, password: string) {
        const { data } = await api.post('/auth/register', { email, name, password })
        return data
    },

    async getProfile() {
        const { data } = await api.get('/auth/profile')
        return data
    },

    async updateProfile(updates: { name?: string; avatar?: string }) {
        const { data } = await api.put('/auth/profile', updates)
        return data
    },
}

export default authService
