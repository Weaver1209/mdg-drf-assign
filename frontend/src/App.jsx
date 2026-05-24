import { BrowserRouter,Route,Routes, Navigate} from "react-router-dom";
import TaskBoard from "./pages/TaskBoard";
import NotificationBell from "./components/NotificationBell";
export default function App(){
   return (
    <BrowserRouter>
    <div
        style={{
            display: 'flex',
            justifyContent: 'flex-end',
            padding: '10px'
        }}
    >
        <NotificationBell />
    </div>
    <Routes>
        <Route
          path="/studio/:studioId/project/:projectId/tasks"
          element={<TaskBoard />}
        />
    </Routes>
    </BrowserRouter>
   );
}