// src/pages/AddressesPage.tsx

import { useState, useEffect } from 'react';
import { Layout } from '../components/Layout';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { addressService } from '../services/addressService';
import { Address } from '../types/address';
import styles from './AddressesPage.module.css';

export const AddressesPage: React.FC = () => {
  const [addresses, setAddresses] = useState<Address[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadAddresses();
  }, []);

  const loadAddresses = async () => {
    try {
      setLoading(true);
      const data = await addressService.getAll();
      setAddresses(data);
      setError('');
    } catch (err: any) {
      setError('Erro ao carregar endereços');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Deseja realmente deletar este endereço?')) {
      try {
        await addressService.delete(id);
        setAddresses(addresses.filter((a) => a.id !== id));
      } catch (err: any) {
        setError('Erro ao deletar endereço');
        console.error(err);
      }
    }
  };

  return (
    <Layout>
      <div className={styles.container}>
        <div className={styles.header}>
          <h2>Endereços</h2>
          <button className={styles.addBtn}>+ Novo Endereço</button>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        {loading ? (
          <LoadingSpinner />
        ) : addresses.length === 0 ? (
          <div className={styles.empty}>Nenhum endereço encontrado</div>
        ) : (
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Rua</th>
                  <th>Número</th>
                  <th>Bairro</th>
                  <th>Cidade</th>
                  <th>Estado</th>
                  <th>CEP</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {addresses.map((address) => (
                  <tr key={address.id}>
                    <td>{address.id}</td>
                    <td>{address.rua}</td>
                    <td>{address.numero}</td>
                    <td>{address.bairro}</td>
                    <td>{address.cidade}</td>
                    <td>{address.estado}</td>
                    <td>{address.cep}</td>
                    <td className={styles.actions}>
                      <button className={styles.editBtn}>Editar</button>
                      <button
                        className={styles.deleteBtn}
                        onClick={() => handleDelete(address.id)}
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
