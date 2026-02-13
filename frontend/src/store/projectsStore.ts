import { create } from 'zustand'

interface Project {
  id: string
  title: string
  description: string
  status: string
}

interface ProjectsStore {
  projects: Project[]
  setProjects: (projects: Project[]) => void
  addProject: (project: Project) => void
}

export const useProjectsStore = create<ProjectsStore>((set) => ({
  projects: [],
  setProjects: (projects) => set({ projects }),
  addProject: (project) => set((state) => ({ projects: [...state.projects, project] })),
}))

export default useProjectsStore
