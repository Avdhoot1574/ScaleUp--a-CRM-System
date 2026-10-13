import { Navigate, Route, Routes } from 'react-router-dom';
import AppLayout from './components/AppLayout';
import ProtectedRoute from './components/ProtectedRoute';
import { LoginPage, RegisterPage } from './pages/AuthPages';
import Dashboard from './pages/Dashboard';
import ResourcePage from './pages/ResourcePage';
import Profile from './pages/Profile';
import { useAuth } from './context/AuthContext';

function HomeRedirect(){const {user,loading}=useAuth();if(loading)return <div className="screen-loading"><span className="spinner"/>Loading workspace…</div>;return <Navigate to={user?'/dashboard':'/login'} replace/>;}
export default function App(){return <Routes>
  <Route path="/" element={<HomeRedirect/>}/>
  <Route path="/login" element={<LoginPage/>}/>
  <Route path="/register" element={<RegisterPage/>}/>
  <Route element={<ProtectedRoute/>}><Route element={<AppLayout/>}>
    <Route path="/dashboard" element={<Dashboard/>}/>
    <Route path="/companies" element={<ResourcePage resource="companies"/>}/>
    <Route path="/contacts" element={<ResourcePage resource="contacts"/>}/>
    <Route path="/leads" element={<ResourcePage resource="leads"/>}/>
    <Route path="/deals" element={<ResourcePage resource="deals"/>}/>
    <Route path="/activities" element={<ResourcePage resource="activities"/>}/>
    <Route path="/tasks" element={<ResourcePage resource="tasks"/>}/>
    <Route path="/profile" element={<Profile/>}/>
    <Route element={<ProtectedRoute adminOnly/>}><Route path="/users" element={<ResourcePage resource="users"/>}/></Route>
  </Route></Route>
  <Route path="*" element={<HomeRedirect/>}/>
</Routes>}
