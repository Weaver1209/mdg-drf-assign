import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import TaskDetail from './TaskDetail';

export default function TaskBoard() {
  //fetching the studioId and projectId from the URL
  const { studioId, projectId } = useParams();
  
  const [tasks, setTasks] = useState([]); //list of the task from the backend
  const [selectedTask, setSelectedTask] = useState(null); // task which user clicked
  const [loading, setLoading] = useState(false); //while API is loading
  const [error, setError] = useState(''); //to show any error message
  

  const [title, setTitle] = useState(''); 
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('MED');
  const [searchText, setSearchText] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');
  const [stageFilter, setStageFilter] = useState('');
  const [assignee, setAssignee] = useState('');
  const [deadline, setDeadline] = useState('');
  const [tags, setTags] = useState([]);
  const [memberOptions, setMemberOptions] = useState([]);
  const [tagOptions, setTagOptions] = useState([]);
  const [newTagName, setNewTagName] = useState('');
  const [newTagColor, setNewTagColor] = useState('#FF5733');
  
  //function for fetching the tasks with search/filter parameters
  const fetchTasks = async (searchVal = searchText, priorityVal = priorityFilter, stageVal = stageFilter) => {
    setLoading(true);
    setError('');

    try {
       const params = new URLSearchParams();
       if (searchVal) params.append('search', searchVal);
       if (priorityVal) params.append('priority', priorityVal);
       if (stageVal) params.append('stage', stageVal);
       const queryString = params.toString();
       const url = queryString 
         ? `/studios/${studioId}/projects/${projectId}/tasks/?${queryString}` 
         : `/studios/${studioId}/projects/${projectId}/tasks/`;
       const res = await api.get(url);
       setTasks(res.data); 
    }
    catch (err) {
        setError('Could not load tasks');
        console.error('Fetch error:', err);
    }
    finally {
        setLoading(false);
    }
  }

  const CreateTask = async (e) => {
        setError('');
        e.preventDefault();
        try{
                        const validTagIds = tags
                  .map((t) => parseInt(t, 10))
                  .filter((id) => Number.isInteger(id) && id > 0);
                const assigneeId = assignee ? parseInt(assignee, 10) : null;
                const payload = {
                  title,
                  description,
                  priority,
                  deadline: deadline ? new Date(deadline).toISOString() : null,
                  assignee: Number.isInteger(assigneeId) ? assigneeId : null,
                  tags: validTagIds
                };

                const res = await api.post(`/studios/${studioId}/projects/${projectId}/tasks/`, payload);
                setTitle('');
                setDescription('');
                setPriority('MED');
                setAssignee('');
                setDeadline('');
                setTags([]);
                fetchTasks(searchText, priorityFilter, stageFilter);
        }   
        catch (err){
            const errorMsg = err.response?.data || err.message;
            setError('Could not create task: ' + JSON.stringify(errorMsg));
            console.error('Create task error:', errorMsg);
        }
  }

  const fetchMembers = async () => {
    try {
      const res = await api.get(`/studios/${studioId}/members/`);
      setMemberOptions(res.data);
    } catch (err) {
      console.error('Failed to load members', err);
    }
  };

  const fetchTagsData = async () => {
    try {
      const res = await api.get(`/studios/${studioId}/tags/`);
      setTagOptions(res.data);
    } catch (err) {
      console.error('Failed to load tags', err);
    }
  };

  const createTag = async (e) => {
    e.preventDefault();
    if (!newTagName.trim()) {
      alert('Tag name cannot be empty');
      return;
    }
    try {
      const res = await api.post(`/studios/${studioId}/tags/`, {
        name: newTagName,
        color: newTagColor
      });

      setNewTagName('');
      setNewTagColor('#FF5733');
      fetchTagsData();
    } catch (err) {
      const errorMsg = err.response?.data || err.message;
      console.error('Failed to create tag:', errorMsg);
      alert('Failed to create tag: ' + JSON.stringify(errorMsg));
    }
  };

  useEffect(() => {
    if (studioId && projectId) {
      fetchTasks(searchText, priorityFilter, stageFilter);
      fetchMembers();
      fetchTagsData();
    }
  }, [studioId, projectId, searchText, priorityFilter, stageFilter]);
  return (
    <>
        {loading && <p>Loading tasks...</p>}

        {error && <p>{error}</p>}

        {tasks.length === 0 && !loading && <p>No tasks yet.</p>}
        <div className="task-board-filters">
          <input
            type="text"
            placeholder="Search tasks"
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
          />

          <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)}>
            <option value="">All priorities</option>
            <option value="LOW">Low</option>
            <option value="MED">Medium</option>
            <option value="HIGH">High</option>
            <option value="URG">Urgent</option>
          </select>

          <select value={stageFilter} onChange={(e) => setStageFilter(e.target.value)}>
            <option value="">All stages</option>
            <option value="DRAFT">Draft</option>
            <option value="REVIEW">Review</option>
            <option value="REVISION">Revision</option>
            <option value="APPROVED">Approved</option>
            <option value="COMPLETED">Completed</option>
          </select>
        </div>

        {tasks.map((task) => (
        <div key={task.id} className="task-card" onClick={() => setSelectedTask(task)}>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <p>Stage: {task.stage}</p>
            <p>Priority: {task.priority}</p>
        </div>
        ))}

        {/*form for creating a tag*/}
        <div className="tag-creation-section">
          <h3>Create New Tag</h3>
          <form onSubmit={createTag}>
            <input
              type="text"
              value={newTagName}
              onChange={(e) => setNewTagName(e.target.value)}
              placeholder="Tag name"
              required
            />
            <input
              type="color"
              value={newTagColor}
              onChange={(e) => setNewTagColor(e.target.value)}
              title="Pick a color"
            />
            <button type="submit">Create Tag</button>
          </form>
        </div>

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
        <select value={assignee} onChange={e => setAssignee(e.target.value)}>
          <option value="">Assign to</option>
          {memberOptions.map(member => (
            <option key={member.id} value={String(member.user)}>
              {member.username}
            </option>
          ))}
        </select>

        <input
          type="date"
          value={deadline}
          onChange={e => setDeadline(e.target.value)}
        />

        <select multiple value={tags} onChange={e => setTags(Array.from(e.target.selectedOptions, opt => opt.value))}>
          <option value="" disabled>-- Select Tags --</option>
          {tagOptions.length > 0 ? (
            tagOptions.map(tag => (
              <option key={tag.id} value={tag.id}>
                {tag.name}
              </option>
            ))
          ) : (
            <option disabled>No tags available</option>
          )}
        </select>

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