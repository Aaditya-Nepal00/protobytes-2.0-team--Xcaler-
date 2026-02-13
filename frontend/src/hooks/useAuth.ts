import { useEffect, useState } from 'react'
import { useAuthStore } from '../store/authStore'
import authService from '../services/auth.service'

export const useAuth = () => {
  const { user, token, isAuthenticated, setUser, setToken, logout } = useAuthStore()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (token) {
      authService.getProfile().then((data) => {
        setUser(data)
        setLoading(false)
      }).catch(() => {
        setLoading(false)
      })
    } else {
      setLoading(false)
    }
  }, [token, setUser])

  return { user, token, isAuthenticated, loading, setToken, logout }
}

export default useAuth
