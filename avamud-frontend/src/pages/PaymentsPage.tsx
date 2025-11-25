// src/pages/PaymentsPage.tsx

import { useState, useEffect } from 'react';
import { Layout } from '../components/Layout';
import { LoadingSpinner } from '../components/LoadingSpinner';
import { paymentService } from '../services/paymentService';
import { Payment } from '../types/payment';
import styles from './PaymentsPage.module.css';

export const PaymentsPage: React.FC = () => {
  const [payments, setPayments] = useState<Payment[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadPayments();
  }, []);

  const loadPayments = async () => {
    try {
      setLoading(true);
      const data = await paymentService.getAll();
      setPayments(data);
      setError('');
    } catch (err: any) {
      setError('Erro ao carregar pagamentos');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (confirm('Deseja realmente deletar este pagamento?')) {
      try {
        await paymentService.delete(id);
        setPayments(payments.filter((p) => p.id !== id));
      } catch (err: any) {
        setError('Erro ao deletar pagamento');
        console.error(err);
      }
    }
  };

  const formatCurrency = (value: number | string) => {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL',
    }).format(num);
  };

  return (
    <Layout>
      <div className={styles.container}>
        <div className={styles.header}>
          <h2>Pagamentos</h2>
          <button className={styles.addBtn}>+ Novo Pagamento</button>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        {loading ? (
          <LoadingSpinner />
        ) : payments.length === 0 ? (
          <div className={styles.empty}>Nenhum pagamento encontrado</div>
        ) : (
          <div className={styles.tableWrapper}>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Valor</th>
                  <th>Data</th>
                  <th>Usuário ID</th>
                  <th>Ações</th>
                </tr>
              </thead>
              <tbody>
                {payments.map((payment) => (
                  <tr key={payment.id}>
                    <td>{payment.id}</td>
                    <td>{formatCurrency(payment.valor)}</td>
                    <td>{new Date(payment.dataPagamento).toLocaleDateString()}</td>
                    <td>{payment.user_id}</td>
                    <td className={styles.actions}>
                      <button className={styles.editBtn}>Editar</button>
                      <button
                        className={styles.deleteBtn}
                        onClick={() => handleDelete(payment.id)}
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
