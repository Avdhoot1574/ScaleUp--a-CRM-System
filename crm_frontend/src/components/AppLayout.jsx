import { useState } from 'react';
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { Activity, Building2, CheckSquare, ChevronDown, CircleHelp, Contact, Handshake, LayoutDashboard, LogOut, Menu, Search, Settings2, Users, UserRound, X, Target } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const nav = [
  { label: 'Workspace', items: [
    { to: '/dashboard', label: 'Overview', icon: LayoutDashboard },
    { to: '/leads', label: 'Leads', icon: Target },
    { to: '/deals', label: 'Deals', icon: Handshake },
    { to: '/tasks', label: 'Tasks', icon: CheckSquare },
  ]},
  { label: 'Relationships', items: [
    { to: '/companies', label: 'Companies', icon: Building2 },
    { to: '/contacts', label: 'Contacts', icon: Contact },
    { to: '/activities', label: 'Activities', icon: Activity },
  ]},
];
export default function AppLayout() {
  const { user, logout } = useAuth(); const [open, setOpen] = useState(false); const [profileOpen, setProfileOpen] = useState(false); const [helpVisible, setHelpVisible] = useState(true);
  const location = useLocation(); const navigate = useNavigate();
  const page = [...nav.flatMap(g => g.items), {to:'/users',label:'User management'}].find(i => location.pathname === i.to)?.label || 'Overview';
  return <div className="app-shell">
    {open && <button className="mobile-scrim" aria-label="Close navigation" onClick={() => setOpen(false)} />}
    <aside className={`sidebar ${open ? 'sidebar-open' : ''}`}>
      <div className="brand"><div className="brand-mark">N</div><div><strong>ScaleUp</strong><span>CRM WORKSPACE</span></div><button className="icon-button mobile-close" onClick={() => setOpen(false)} aria-label="Close menu"><X size={18}/></button></div>
      <div className="workspace-switch"><div className="workspace-symbol">NS</div><div><strong>ScaleUp Inc.</strong><span>Sales workspace</span></div><ChevronDown size={15}/></div>
      <nav className="side-nav">
        {nav.map(group => <div className="nav-group" key={group.label}><div className="nav-label">{group.label}</div>{group.items.map(item => <NavLink onClick={() => setOpen(false)} className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`} to={item.to} key={item.to}><item.icon size={18}/><span>{item.label}</span></NavLink>)}</div>)}
        {user?.role === 'ADMIN' && <div className="nav-group"><div className="nav-label">Administration</div><NavLink onClick={() => setOpen(false)} className={({isActive}) => `nav-link ${isActive ? 'active' : ''}`} to="/users"><Users size={18}/><span>User management</span></NavLink></div>}
      </nav>
      <div className="sidebar-bottom">{helpVisible && <div className="help-card"><button className="help-dismiss" onClick={() => setHelpVisible(false)} aria-label="Dismiss help card" title="Dismiss"><X size={15}/></button><div className="help-icon"><CircleHelp size={17}/></div><strong>Need a hand?</strong><p>Manage your pipeline and keep your team aligned.</p><button className="help-action" onClick={() => navigate('/activities')}>View activities <span>→</span></button></div>}<div className="sidebar-foot"><span className="status-dot"/> All systems operational</div></div>
    </aside>
    <main className="main-area">
      <header className="topbar"><div className="topbar-left"><button className="icon-button mobile-menu" onClick={() => setOpen(true)} aria-label="Open menu"><Menu size={20}/></button><div className="breadcrumbs">Workspace <span>/</span> <strong>{page}</strong></div></div><div className="topbar-actions"><div className="api-status"><span className="status-dot"/> API connected</div><button className="search-shortcut" onClick={() => navigate('/leads')}><Search size={16}/><span>Search records</span><kbd>⌘ K</kbd></button><div className="profile-wrap"><button className="profile-button" onClick={() => setProfileOpen(v => !v)}><div className="avatar">{user?.name?.split(' ').map(s => s[0]).slice(0,2).join('').toUpperCase() || 'U'}</div><div className="profile-meta"><strong>{user?.name || 'User'}</strong><span>{user?.role === 'ADMIN' ? 'Administrator' : 'Sales representative'}</span></div><ChevronDown size={15}/></button>{profileOpen && <div className="profile-menu"><div className="profile-menu-user"><strong>{user?.name}</strong><span>{user?.email}</span></div><button onClick={() => { setProfileOpen(false); navigate('/profile'); }}><UserRound size={16}/> My profile</button><button onClick={() => { logout(); navigate('/login'); }}><LogOut size={16}/> Sign out</button></div>}</div></div></header>
      <div className="page-content"><Outlet/></div>
      <footer className="app-footer"><span>ScaleUp CRM</span><span>Connected to your FastAPI workspace</span></footer>
    </main>
  </div>;
}
