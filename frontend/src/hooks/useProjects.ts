import { useEffect } from 'react'
import { useProjectsStore } from '../store/projectsStore'
import projectsService from '../services/projects.service'

export const useProjects = () => {
  const { projects, setProjects } = useProjectsStore()

  useEffect(() => {
    projectsService.getAll().then(setProjects)
  }, [setProjects])

  return { projects, setProjects }
}

export default useProjects
