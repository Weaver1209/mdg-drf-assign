import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../api';
import '../App.css';

export default function StudioDetail() {
  const { studioId } = useParams();
  const navigate = useNavigate();
  const [members, setMembers] = useState([]);
  const [studio, setStudio] = useState(null);

  useEffect(() => {
    api.get(`studios/${studioId}/`)
    .then(res => setStudio(res.data));
    api.get(`studios/${studioId}/members/`)
    .then(res => setMembers(res.data));
  }, [studioId]);

  if (!studio) return <h1>Loading...</h1>;

  return (
    <div className="page-container">
      <h2>{studio.name}</h2>
      <p className="text-muted">{studio.description}</p>
      
      <button className="primary" onClick={() => navigate(`/studio/${studioId}/projects`)}>
        View Projects
      </button>

      <hr style={{ margin: '20px 0' }} />
      <h3>Team Members</h3>
      <ul className="member-list">
        {members.map(member => (
          <li key={member.id}>
            <strong>{member.username}</strong> - {member.role_display}
          </li>
        ))}
      </ul>
    </div>
  );
}