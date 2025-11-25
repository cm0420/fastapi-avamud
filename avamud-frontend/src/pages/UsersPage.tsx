// src/pages/UsersPage.tsx

import { useState, useEffect } from 'react';
import { Layout } from '../components/Layout';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { userService } from '../services/userService';
import { User } from '../types/user';
import styles from './UsersPage.module.css';

export const UsersPage: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      const data = await userService.getAll();
      setUsers(data);
      setError('');
    } catch (err: any) {
      setError('Erro ao carregar usuários');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Deseja realmente deletar este usuário?')) {
      try {
        await userService.delete(id);
        setUsers(users.filter((u) => u.id !== id));
      } catch (err: any) {
        setError('Erro ao deletar usuário');
        console.error(err);
      }
    }
  };

  return (
    <Layout>
      <div className={styles.container}>
        <div className={styles.header}>
          <h2>Usuários</h2>
          <button className={styles.addBtn}>+ Novo Usuário</button>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        {loading ? (
          <LoadingSpinner />
        ) : users.length === 0 ? (
          <div className={styles.empty}>Nenhum usuário encontrado</div>
        ) : (
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Nome</th>
                  <th>Email</th>
                  <th>Login</th>
                  <th>Telefone</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.nome}</td>
                    <td>{user.email}</td>
                    <td>{user.login}</td>
                    <td>{user.telefone}</td>
                    <td className={styles.actions}>
                      <button className={styles.editBtn}>Editar</button>
                      <button
                        className={styles.deleteBtn}
                        onClick={() => handleDelete(user.id)}
                      >
                        Deletar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </Layout>
  );
};
