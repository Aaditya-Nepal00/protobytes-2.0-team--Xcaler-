import { useEffect, useState } from 'react'
import tendersService from '../services/tenders.service'

export const useTenders = () => {
  const [tenders, setTenders] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    tendersService.getAll().then((data) => {
      setTenders(data)
      setLoading(false)
    })
  }, [])

  return { tenders, loading }
}

export default useTenders
