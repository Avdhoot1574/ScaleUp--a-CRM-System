import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
export default function ProtectedRoute({ adminOnly = false }) {
  const { user, loading } = useAuth(); const location = useLocation();
  if (loading) return <div className="screen-loading"><span className="spinner" />Checking session…</div>;
  if (!user) return <Navigate to="/login" replace state={{ from: location }} />;
  if (adminOnly && user.role !== 'ADMIN') return <Navigate to="/dashboard" replace />;
  return <Outlet />;
}
