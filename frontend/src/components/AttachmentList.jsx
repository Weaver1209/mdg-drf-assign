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

        </div>
    );
}