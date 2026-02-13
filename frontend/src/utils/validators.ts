// Email validation
export const validateEmail = (email: string): boolean => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

// Password validation
export const validatePassword = (password: string): boolean => {
  return password.length >= 8
}

// Required field validation
export const validateRequired = (value: string): boolean => {
  return value.trim().length > 0
}

// Min length validation
export const validateMinLength = (value: string, minLength: number): boolean => {
  return value.length >= minLength
}

export default {
  validateEmail,
  validatePassword,
  validateRequired,
  validateMinLength,
}
