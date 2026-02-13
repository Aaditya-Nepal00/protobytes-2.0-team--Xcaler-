import api from './api'

const forumService = {
    async getThreads(params?: { page?: number; sort?: string; category?: string }) {
        const { data } = await api.get('/forum/threads', { params })
        return data
    },

    async getThread(id: string) {
        const { data } = await api.get(`/forum/threads/${id}`)
        return data
    },

    async createThread(payload: { title: string; content: string; category?: string; is_anonymous?: boolean; tags?: string[] }) {
        const { data } = await api.post('/forum/threads', payload)
        return data
    },

    async voteThread(threadId: string, vote_type: 'upvote' | 'downvote') {
        const { data } = await api.post(`/forum/threads/${threadId}/vote`, { vote_type })
        return data
    },

    async createComment(threadId: string, payload: { content: string; parent_id?: string; is_anonymous?: boolean }) {
        const { data } = await api.post(`/forum/threads/${threadId}/comments`, payload)
        return data
    },

    async voteComment(commentId: string, vote_type: 'upvote' | 'downvote') {
        const { data } = await api.post(`/forum/comments/${commentId}/vote`, { vote_type })
        return data
    },

    async getCategories() {
        const { data } = await api.get('/forum/categories')
        return data
    },
}

export default forumService
