import api from './api'

const budgetService = {
    async getBudgets(params?: { fiscal_year?: string; sector?: string; level?: string; ministry?: string }) {
        const { data } = await api.get('/budget', { params })
        return data
    },

    async getSummary(fiscal_year?: string) {
        const { data } = await api.get('/budget/summary', { params: { fiscal_year } })
        return data
    },

    async getSectors() {
        const { data } = await api.get('/budget/sectors')
        return data
    },

    async getFiscalYears() {
        const { data } = await api.get('/budget/fiscal-years')
        return data
    },
}

export default budgetService
