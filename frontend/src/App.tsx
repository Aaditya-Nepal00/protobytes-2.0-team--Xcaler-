import { Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import LawBot from './components/common/LawBot'
import Home from './pages/Home'
import Projects from './pages/Projects'
import Tenders from './pages/Tenders'
import Budget from './pages/Budget'
import CorruptionReport from './pages/CorruptionReport'
import Laws from './pages/Laws'
import Forum from './pages/Forum'
import ForumThread from './pages/ForumThread'
import Login from './pages/Login'
import Register from './pages/Register'
import ProjectDetail from './pages/ProjectDetail'
import TenderDetail from './pages/TenderDetail'

function App() {
  return (
    <div className="app">
      <Navbar />
      <main style={{ minHeight: 'calc(100vh - 160px)' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/projects/:projectId" element={<ProjectDetail />} />
          <Route path="/tenders" element={<Tenders />} />
          <Route path="/tenders/:tenderId" element={<TenderDetail />} />
          <Route path="/budget" element={<Budget />} />
          <Route path="/reports" element={<CorruptionReport />} />
          <Route path="/laws" element={<Laws />} />
          <Route path="/forum" element={<Forum />} />
          <Route path="/forum/:threadId" element={<ForumThread />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Routes>
      </main>
      <Footer />
      <LawBot />
    </div>
  )
}

export default App
