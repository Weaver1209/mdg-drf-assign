import { BrowserRouter,Route,Routes, Navigate} from "react-router-dom";
import TaskBoard from "./pages/TaskBoard";

export default function App(){
   return (
    <BrowserRouter>
    <Routes>
        <Route
          path="/studio/:studioId/project/:projectId/tasks"
          element={<TaskBoard />}
        />
    </Routes>
    </BrowserRouter>
   );
}