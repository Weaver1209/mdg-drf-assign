import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import '../App.css';

export default function ProjectList() {
  const { studioId } = useParams();
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [newProject, setNewProject] = useState({ name: '', description: '' });

  const fetchProjects = () => {
    api.get(`studios/${studioId}/projects/`).then(res => setProjects(res.data));
  };

  useEffect(() => { fetchProjects(); }, [studioId]);

  const handleCreate = async (e) => {
    e.preventDefault();
    await api.post(`studios/${studioId}/projects/`, newProject);
    setShowForm(false);
    setNewProject({ name: '', description: '' });
    fetchProjects();
  };

  return (
    <div className="page-container">
      <div className="header-row">
        <h2>Projects</h2>
        <button className="primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Create Project'}
        </button>
      </div>

      {showForm && (
        <form className="card" onSubmit={handleCreate} style={{ marginBottom: '20px' }}>
          <input 
            type="text" 
            placeholder="Project Name" 
            value={newProject.name} 
            onChange={e => setNewProject({...newProject, name: e.target.value})}
            required 
          />
          <textarea 
            placeholder="Description" 
            value={newProject.description} 
            onChange={e => setNewProject({...newProject, description: e.target.value})}
          />
          <button type="submit" className="btn btn-success">Save Project</button>
        </form>
      )}

      <div className="grid-container">
        {projects.map(project => (
          <div 
            key={project.id} 
            className="card clickable" 
            onClick={() => navigate(`/studio/${studioId}/project/${project.id}/tasks`)}
          >
            <h3>{project.name}</h3>
            <p className="text-muted">{project.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}