import { useEffect, useState } from "react";
import api from '../api';

export default function NotificationBell() {
    const [notifications, setNotifications] = useState([]);
    const [open,setOpen] = useState(false);

    const fetchNotifications = async () => {
        const res = await api.get('/notifications/');
        setNotifications(res.data);
    }

    useState(() => {
        fetchNotifications();
    },[]);

    
    const markAsRead = async () => {
        await api.patch(`/notifications/${id}/mark_as_read/`);
        fetchNotifications();
    }
    return (
    <div>
      <button onClick={() => setOpen(!open)}>
        Notifications 
      </button>

      {open && ( <div>
          {notifications.map((notification) => (
            <div key={notification.id}>
              <p>{notification.message}</p>
              <p>{notification.notification_type}</p>

              {!notification.is_read && (
                <button onClick={() => markAsRead(notification.id)}>
                  Mark read
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}