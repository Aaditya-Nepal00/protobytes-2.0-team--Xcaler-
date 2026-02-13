// Format date to readable format
export const formatDate = (date: Date | string): string => {
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(date))
}

// Format currency
export const formatCurrency = (amount: number, currency: string = 'USD'): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency,
  }).format(amount)
}

// Format percentage
export const formatPercentage = (value: number, decimals: number = 2): string => {
  return (value * 100).toFixed(decimals) + '%'
}

export default {
  formatDate,
  formatCurrency,
  formatPercentage,
}
