import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout from './components/Layout';
import Login from './pages/Login';
import Register from './pages/Register';
import CreateStudio from './pages/CreateStudio';
import StudioDetail from './pages/StudioDetail';
import ProjectList from './pages/ProjectList';
import TaskBoard from './pages/TaskBoard';

function ProtectedRoute({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <h1>Loading...</h1>;
  return user ? children : <Navigate to="/login" />;
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
            <Route path="studios/create" element={<CreateStudio />} />
            
            <Route path="studio/:studioId" element={<StudioDetail />} />
            <Route path="studio/:studioId/projects" element={<ProjectList />} />
            <Route path="studio/:studioId/project/:projectId/tasks" element={<TaskBoard />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;