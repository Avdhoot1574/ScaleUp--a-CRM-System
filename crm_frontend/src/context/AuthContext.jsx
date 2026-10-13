import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { api } from '../lib/api';

const AuthContext = createContext(null);
export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem('crm_user') || 'null'); } catch { return null; }
  });
  const [loading, setLoading] = useState(Boolean(localStorage.getItem('crm_access_token')));

  const loadMe = useCallback(async () => {
    const token = localStorage.getItem('crm_access_token');
    if (!token) { setUser(null); setLoading(false); return null; }
    try {
      const { data } = await api.get('/auth/me');
      setUser(data); localStorage.setItem('crm_user', JSON.stringify(data)); return data;
    } catch (error) { setUser(null); throw error; }
    finally { setLoading(false); }
  }, []);

  useEffect(() => { if (localStorage.getItem('crm_access_token')) loadMe().catch(() => {}); else setLoading(false); }, [loadMe]);

  const login = async (email, password) => {
    const { data } = await api.post('/auth/login', { email, password });
    localStorage.setItem('crm_access_token', data.access_token);
    const { data: profile } = await api.get('/auth/me');
    localStorage.setItem('crm_user', JSON.stringify(profile)); setUser(profile); return profile;
  };
  const register = async (payload) => (await api.post('/auth/register', payload)).data;
  const logout = () => { localStorage.removeItem('crm_access_token'); localStorage.removeItem('crm_user'); setUser(null); };
  return <AuthContext.Provider value={{ user, loading, login, register, logout, loadMe }}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);
