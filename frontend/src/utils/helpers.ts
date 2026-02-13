// General utilities
export const truncateString = (str: string, length: number): string => {
  return str.length > length ? str.substring(0, length) + '...' : str
}

// Get initials from name
export const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map((n) => n[0])
    .join('')
    .toUpperCase()
}

// Delay function
export const delay = (ms: number): Promise<void> => {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

export default {
  truncateString,
  getInitials,
  delay,
}
