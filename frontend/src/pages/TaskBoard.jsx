import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

export default function TaskBoard() {
  //fetching the studioId and projectId from the URL
  const { studioId, projectId } = useParams();
  
  //creating different states for fetching of the tasks
  const [tasks, setTasks] = useState([]); //list of the task from the backend
  const [selectedTask, setSelectedTask] = useState(null); // task user clicked
  const [loading, setLoading] = useState(false); //while API is loading
  
  const [error, setError] = useState(''); //to show any error message
  
  //function for fetching the tasks
  const fetchTasks = async () => {
    setLoading(true);
    setError('');

    try {
       const res = await api.get(`/studios/${studioId}/projects/${projectId}/tasks/`);
       setTasks(res.data); 
    }
    catch (err) {
        setError('Could not load tasks');
    }
    finally {
        setLoading(false);
    }
  }
  useEffect(() => {
    fetchTasks();
  },[studioId,projectId]);
  
  //states for the creating a task form, states includes the parameters and attributes required by the task model
  const [title, setTitle] = useState(''); 
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('MED');

  const CreateTask = async (e) => {
        setError('');
        e.preventDefault(); //stops the browser to completely refreshing the page after form submission
        try{
                await api.post(`/studios/${studioId}/projects/${projectId}/tasks/`, {title, description, priority,});
                setTitle('');
                setDescription('');
                setPriority('MED');
                fetchTasks();
        }   
        catch (err){
            setError('Could not create task');
        }
  }
  return (
    <>
        {loading && <p>Loading tasks...</p>}

        {error && <p>{error}</p>}

        {tasks.length === 0 && !loading && <p>No tasks yet.</p>}

        {tasks.map((task) => (
        <div key={task.id} onClick={() => setSelectedTask(task)}>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <p>Stage: {task.stage}</p>
            <p>Priority: {task.priority}</p>
        </div>
        ))}

        {/*form for creating or adding a task*/}
        <form onSubmit={CreateTask}>
        <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Task title"
            required
        />

        <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Task description"
        />

        <select value={priority} onChange={(e) => setPriority(e.target.value)}>
            <option value="LOW">Low</option>
            <option value="MED">Medium</option>
            <option value="HIGH">High</option>
            <option value="URG">Urgent</option>
        </select>

        <button type="submit">Create Task</button>
        </form>
        
        {/*if any of the task is selected then we will call the taskdetail then asking the other page to return a task detail by passing some properties or props*/}
        {selectedTask && ( <TaskDetail
          task={selectedTask} //passing the entire task object
          studioId={studioId} //passing it's studio and project id will help in building the url
          projectId={projectId}
          onTaskUpdated={fetchTasks}  //passing this so that taskdetail.jsx can update the state 
        />
      )}   
    </>

  );
}