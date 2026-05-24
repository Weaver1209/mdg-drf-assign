import { useEffect,useState } from "react";
import api from '..api';

export default function AttachmentList({taskId}){

    const [attachments, setAttachment] = useState
    const [label,setLabel] = useState('');
    const [fileType,setFileType] = useState('other');
    const [file,setFile] = useState(null);

    const fetchAttachments = async () => {
         const res = await api.get(`/attachments/?task_id=${taskId}`);
         setAttachment(res.data)
        }
    
    useEffect(() => {
        fetchAttachments();
    },[taskId]);
    
    
  const uploadAttachment = async (e) => {
        e.preventDefault();
        
         // A raw binary file cannot be sent via standard JSON. 
        // We use FormData to package the text data and the physical file
        const formData = new FormData();
        formData.append('task_id', taskId);
        formData.append('label', label);
        formData.append('file_type', fileType);

        if (file) {
        formData.append('file', file);
        formData.append('file_size', file.size);
        }

        await api.post('/attachments/', formData);

        setLabel('');
        setFile(null);
        setFileType('other');
        fetchAttachments();
   };

    return (
        <div>
        <h3>Attachments</h3>

        {attachments.map((attachment) => (
            <div key={attachment.id}>
            <p>{attachment.label || attachment.file}</p>
            {attachment.file && (
                <a href={attachment.file} target="_blank">
                Open file
                </a>
            )}
            </div>
        ))}
        <form onSubmit={uploadAttachment}>
            <input
            value={label}
            onChange={(e) => setLabel(e.target.value)}
            placeholder="Attachment label"
            />

            <select value={fileType} onChange={(e) => setFileType(e.target.value)}>
            <option value="image">Image</option>
            <option value="video">Video</option>
            <option value="document">Document</option>
            <option value="other">Other</option>
            </select>

            <input type="file" onChange={(e) => setFile(e.target.files[0])} />

            <button type="submit">Upload</button>
        </form>
        </div>
    );
}