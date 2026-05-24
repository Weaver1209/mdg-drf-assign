import { useState } from 'react';
import api from '../api';

const STAGES = ['DRAFT', 'REVIEW', 'REVISION', 'APPROVED', 'COMPLETED'];  //different stages for the task

export default function TaskDetail({ task, studioId, projectId, onTaskUpdated}) {

    const [stage, setStage] = useState(task.stage); 
    const [error, setError] = useState('');

    //function for updating the stage of the task
    const updateStage = async (newStage) => {
        setStage(newStage);
        setError('');

        try{
            await api.patch(`/studios/${studioId}/projects/${projectId}/tasks/${task.id}/`, {stage: newStage}); //only sending the field needed to be changed
            onTaskUpdated();
        } 
        catch{
            setStage(task.stage)
            setError('Could not update task stage');
        } 
    };
    return (
    <div>
      {/* Task Info */}
      <h2>{task.title}</h2>
      <p>{task.description}</p>
      <p>Priority: {task.priority}</p>

      {/* Error */}
      {error && <p>{error}</p>}

      {/* For selection of new stage  */}
      <label>Stage</label>
      <select value={stage} onChange={(e) => updateStage(e.target.value)}>
        {stages.map((item) => (
          <option key={item} value={item}>
            {item}
          </option>
        ))}
      </select>


    </div>
  );
}
