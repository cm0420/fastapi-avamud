// src/components/Layout.tsx

import { ReactNode } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import styles from './Layout.module.css';

interface LayoutProps {
  children: ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <div className={styles.navbar}>
          <h1>Avamud</h1>
          <nav className={styles.nav}>
            <a href="/users">Usuários</a>
            <a href="/payments">Pagamentos</a>
            <a href="/addresses">Endereços</a>
            <button onClick={handleLogout} className={styles.logoutBtn}>
              Logout
            </button>
          </nav>
        </div>
      </header>
      <main className={styles.main}>
        {children}
      </main>
    </div>
  );
};
