import { useState } from 'react';
import { useNavigate, useOutletContext } from 'react-router-dom';
import api from '../api';

export default function CreateStudio() {
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const context = useOutletContext();
  const refreshStudios = context?.refreshStudios;

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('studios/', { name, description });
      if (refreshStudios) {
        refreshStudios();
      }
      navigate('/');
    } catch (err) {
      alert('Failed to create studio');
      console.error(err.response?.data);
    }
  };

  return (
    <div className="page-container">
      <h2>Create a New Studio</h2>
      <p className="text-muted">Create a workspace for your team to manage projects.</p>
      
      <form onSubmit={handleSubmit} style={{ maxWidth: '500px', marginTop: '20px' }}>
        <label>Studio Name</label>
        <input 
          type="text" 
          placeholder="name" 
          value={name} 
          onChange={e => setName(e.target.value)}
          required 
        />
        
        <label>Description</label>
        <textarea 
          placeholder="disc" 
          value={description} 
          onChange={e => setDescription(e.target.value)}
        />
        
        <button type="submit" style={{ marginTop: '16px' }}>Create Studio</button>
      </form>
    </div>
  );
}