import { Outlet, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';
import { useEffect, useState } from 'react';
import '../App.css';

export default function Layout() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [studios, setStudios] = useState([]);

  useEffect(() => {
    if (user) {
      api.get('studios/').then(res => setStudios(res.data));
    }
  }, [user]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="app-container">
      <div className="sidebar">
        <div className="sidebar-header">
          <h2>Creative Studio</h2>
          <p>Hi, {user?.username}</p>
          <button className="create-studio" onClick={() => navigate('/studios/create')}>Create Studio</button>
        </div>
        
        <ul className="studio-list">
          {studios.map(studio => (
            <li key={studio.id} onClick={() => navigate(`/studio/${studio.id}`)}>
              {studio.name}
            </li>
          ))}
        </ul>

        <div className="sidebar-footer">
          <button className="logout-button" onClick={handleLogout}>Logout</button>
        </div>
      </div>

      <div className="main-content">
        <Outlet /> 
      </div>
    </div>
  );
}