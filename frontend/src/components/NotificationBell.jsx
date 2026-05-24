import { useEffect, useState } from "react";
import api from '../api';

export default function NotificationBell() {
    const [notifications, setNotifications] = useState([]);
    const [open,setOpen] = useState(false);

    const fetchNotifications = async () => {
        const res = await api.get('/notifications/');
        setNotifications(res.data);
    }

    useEffect(() => {
        fetchNotifications();
    },[]);


    const markAsRead = async (id) => {
        await api.patch(`/notifications/${id}/mark_as_read/`);
        fetchNotifications();
    }
    return (
    <div className="notification-wrapper">
    <button onClick={() => setOpen(!open)}>
        Notifications (
            {notifications.filter(
                (item) => !item.is_read
            ).length}
        )
    </button>

      {open && ( <div className="notification-dropdown">
            {notifications.length === 0 && (
            <p>No notifications yet</p>
             )}

          {notifications.map((notification) => (
            <div key={notification.id}     style={{
        backgroundColor: notification.is_read ? '#f5f5f5' : '#dbeafe', padding: '8px',marginBottom: '5px',borderRadius: '5px'
    }}>
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