import { create } from 'zustand'

interface ForumStore {
  forumThreads: any[]
  setForumThreads: (threads: any[]) => void
}

export const useForumStore = create<ForumStore>((set) => ({
  forumThreads: [],
  setForumThreads: (threads) => set({ forumThreads: threads }),
}))

export default useForumStore
