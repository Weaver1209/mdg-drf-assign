import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api';

export default function StudioDetail() {
  const { studioId } = useParams();
  const { user: currentUser } = useAuth();
  const navigate = useNavigate();

  const [studio, setStudio] = useState(null);
  const [members, setMembers] = useState([]);
  const [allUsers, setAllUsers] = useState([]); 

  
  const [selectedUser, setSelectedUser] = useState('');
  const [selectedRole, setSelectedRole] = useState('DESIGNER');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const fetchStudioDetails = () => {
    api.get(`studios/${studioId}/`)
      .then(res => setStudio(res.data))
      .catch(err => console.error(err));

    api.get(`studios/${studioId}/members/`)
      .then(res => setMembers(res.data))
      .catch(err => console.error(err));
  };

  const fetchAllUsers = () => {
    api.get('users/')
      .then(res => setAllUsers(res.data))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    if (studioId) {
      fetchStudioDetails();
      fetchAllUsers();
    }
  }, [studioId]);

  const handleInvite = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!selectedUser) {
      setError('Please select a user to invite.');
      return;
    }

    try {
      await api.post(`studios/${studioId}/members/`, {
        user: parseInt(selectedUser, 10),
        studio: parseInt(studioId, 10),
        role: selectedRole
      });
      setSuccess('Member added successfully!');
      setSelectedUser('');
      fetchStudioDetails();
    } catch (err) {
      setError(err.response?.data?.non_field_errors?.[0] || 'Failed to add member.');
    }
  };

  if (!studio) return <h1>Loading...</h1>;

  
  const userMembership = members.find(m => m.user === currentUser?.id);
  const canInvite = userMembership && (userMembership.role === 'ADMIN' || userMembership.role === 'LEAD');

  return (
    <div className="page-container">
      <h2>{studio.name}</h2>
      <p className="text-muted">{studio.description}</p>
      
      <button className="primary" onClick={() => navigate(`/studio/${studioId}/projects`)}>
        View Projects
      </button>

      <hr style={{ margin: '20px 0' }} />

      
      {canInvite && (
        <div className="card" style={{ marginBottom: '20px' }}>
          <h3>Invite Team Member</h3>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          {success && <p style={{ color: 'green' }}>{success}</p>}
          
          <form onSubmit={handleInvite} style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
            <select 
              value={selectedUser} 
              onChange={e => setSelectedUser(e.target.value)}
              required
            >
              <option value="">-- Select User --</option>
              {allUsers
                .filter(u => !members.some(m => m.user === u.id))
                .map(u => (
                  <option key={u.id} value={u.id}>{u.username}</option>
                ))
              }
            </select>

            <select 
              value={selectedRole} 
              onChange={e => setSelectedRole(e.target.value)}
            >
              <option value="ADMIN">Studio Admin</option>
              <option value="LEAD">Project Lead</option>
              <option value="DESIGNER">Designer</option>
              <option value="WRITER">Writer</option>
              <option value="REVIEWER">Reviewer</option>
              <option value="VIEWER">Client Viewer</option>
            </select>

            <button type="submit" className="btn btn-success">Invite</button>
          </form>
        </div>
      )}

      <h3>Team Members</h3>
      <ul className="member-list">
        {members.map(member => (
          <li key={member.id}>
            <strong>{member.username}</strong> - {member.role}
          </li>
        ))}
      </ul>
    </div>
  );
}