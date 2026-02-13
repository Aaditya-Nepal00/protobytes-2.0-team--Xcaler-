// App constants
export const APP_NAME = 'Project Sachet'
export const APP_VERSION = '0.1.0'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

export const ROLES = {
  USER: 'user',
  ADMIN: 'admin',
  MODERATOR: 'moderator',
} as const

export const PROJECT_STATUS = {
  PLANNING: 'planning',
  ACTIVE: 'active',
  COMPLETED: 'completed',
  ON_HOLD: 'on-hold',
} as const

export default {
  APP_NAME,
  APP_VERSION,
  API_BASE_URL,
  ROLES,
  PROJECT_STATUS,
}
