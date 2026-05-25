import { useEffect, useState } from 'react';
import api from '../api';

export default function CommentSection({ taskId }) {
  const [comments, setComments] = useState([]);
  const [content, setContent] = useState('');

  const fetchComments = async () => {
    const res = await api.get(`/comments/?task_id=${taskId}`);
    setComments(res.data);
  };

  useEffect(() => {
    fetchComments();
  }, [taskId]);

  const submitComment = async (e) => {
    e.preventDefault(); // prevent the browser to refresh and set all the values to initials

    await api.post('/comments/', { 'task_id': taskId,'content': content,});

    setContent('');
    fetchComments();
  };

  return (
    <div>
      <h3>Comments</h3>

      {comments.map((comment) => (
        <div key={comment.id}  className="comment-box">
          <p>{comment.content}</p>
        </div>
      ))}

      <form onSubmit={submitComment}>
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="Write a comment"
        />
        <button type="submit">Post</button>
      </form>
    </div>
  );
}