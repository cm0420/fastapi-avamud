import { useState, useEffect } from 'react';
import { userService, paymentService, reportService } from '../services/apiService';

// Hook para gerenciar usuários
export function useUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Carregar todos os usuários
  const loadUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await userService.getAllUsers();
      setUsers(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Criar usuário
  const createUser = async (userData) => {
    setLoading(true);
    setError(null);
    try {
      console.log('Criando usuário com dados:', userData);
      
      // Mapear papel para role do backend
      let role = 'MEMBER'; // padrão
      if (userData.papel === 'administrador') {
        role = 'ADMIN';
      } else if (userData.papel === 'tesoureiro') {
        role = 'TREASURER';
      }
      
      // Ajustar dados para backend
      const backendUserData = {
        nome: userData.nome,
        cpf: userData.cpf.replace(/\D/g, ''), // Remove formatação
        cnpj: userData.cnpj || userData.cpf.replace(/\D/g, ''), // Usar CPF se CNPJ não fornecido
        email: userData.email,
        telefone: userData.telefone.replace(/\D/g, ''),
        senha: userData.senha || '123456',
        login: userData.login || userData.email.split('@')[0],
        role: role
      };

      console.log('Dados enviados para backend:', backendUserData);

      const newUser = await userService.createUser(backendUserData);
      setUsers(prev => [...prev, newUser]);
      return newUser;
    } catch (err) {
      console.error('Erro ao criar usuário:', err);
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Atualizar usuário
  const updateUser = async (id, userData) => {
    setLoading(true);
    setError(null);
    try {
      const backendUserData = {
        nome: userData.nome,
        cpf: userData.cpf.replace(/\D/g, ''),
        cnpj: userData.cnpj || '',
        email: userData.email,
        telefone: userData.telefone.replace(/\D/g, ''),
        login: userData.login || userData.email, // Manter ou usar email como login
        addresses: userData.endereco ? [{
          rua: userData.endereco.split(',')[0] || userData.endereco,
          numero: userData.numero || '',
          bairro: userData.bairro || '',
          cidade: userData.cidade || '',
          estado: userData.estado || '',
          cep: userData.cep || ''
        }] : []
      };

      // Se senha foi fornecida, incluir no update
      if (userData.senha && userData.senha.trim() !== '') {
        backendUserData.senha = userData.senha;
      }

      console.log('Atualizando usuário:', id, backendUserData);

      const updatedUser = await userService.updateUser(id, backendUserData);
      setUsers(prev => prev.map(user => user.id === id ? updatedUser : user));
      return updatedUser;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Deletar usuário
  const deleteUser = async (id) => {
    setLoading(true);
    setError(null);
    try {
      await userService.deleteUser(id);
      setUsers(prev => prev.filter(user => user.id !== id));
      return true;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Mapear dados do backend para frontend
  const mapUserForFrontend = (backendUser) => {
    if (!backendUser) return null;
    
    const address = backendUser.addresses?.[0];
    
    // Mapear role do backend para papel do frontend
    let papel = 'membro';
    if (backendUser.role === 'ADMIN') {
      papel = 'administrador';
    } else if (backendUser.role === 'TREASURER') {
      papel = 'tesoureiro';
    }
    
    return {
      id: backendUser.id,
      nome: backendUser.nome,
      cpf: backendUser.cpf,
      email: backendUser.email,
      telefone: backendUser.telefone,
      login: backendUser.login,
      papel: papel,
      role: backendUser.role,
      endereco: address ? `${address.rua}, ${address.numero}` : '',
      status: backendUser.active ? 'ativo' : 'inativo',
      dataDeEntrada: backendUser.dataDeEntrada
    };
  };

  useEffect(() => {
    loadUsers();
  }, []);

  return {
    users: Array.isArray(users) ? users.map(mapUserForFrontend) : [],
    loading,
    error,
    loadUsers,
    createUser,
    updateUser,
    deleteUser
  };
}

// Hook para gerenciar pagamentos e dados financeiros
export function usePayments() {
  const [payments, setPayments] = useState([]);
  const [paymentHistory, setPaymentHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Carregar todos os pagamentos
  const loadPayments = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await paymentService.getAllPayments();
      setPayments(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Carregar histórico de pagamentos
  const loadPaymentHistory = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await paymentService.getAllPaymentHistory();
      setPaymentHistory(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Criar pagamento
  const createPayment = async (paymentData) => {
    setLoading(true);
    setError(null);
    try {
      const newPayment = await paymentService.createPayment(paymentData);
      setPayments(prev => [...prev, newPayment]);
      return newPayment;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Calcular estatísticas financeiras
  const getFinancialStats = () => {
    const totalEntradas = payments.reduce((sum, payment) => {
      return sum + parseFloat(payment.valor || 0);
    }, 0);

    // Para demonstração, vamos assumir que todas as entradas são positivas
    // Em um cenário real, você teria um campo 'tipo' ou 'categoria'
    const totalSaidas = 0; // Implementar quando houver saídas no backend
    const saldoAtual = totalEntradas - totalSaidas;
    
    return {
      totalEntradas,
      totalSaidas,
      saldoAtual,
      transacoesPendentes: 0 // Implementar quando houver status no backend
    };
  };

  // Mapear pagamentos para formato do dashboard
  const getTransactionsForDashboard = () => {
    return payments.map(payment => ({
      id: payment.id.toString(),
      date: new Date(payment.dataPagamento).toLocaleDateString('pt-BR'),
      description: `Pagamento #${payment.id}`,
      amount: parseFloat(payment.valor),
      type: 'entrada', // Por padrão, todos são entradas
      status: 'confirmado' // Por padrão, todos são confirmados
    }));
  };

  useEffect(() => {
    loadPayments();
    loadPaymentHistory();
  }, []);

  return {
    payments,
    paymentHistory,
    loading,
    error,
    loadPayments,
    loadPaymentHistory,
    createPayment,
    getFinancialStats,
    getTransactionsForDashboard
  };
}

// Hook para gerenciar relatórios
export function useReports() {
  const [inadimplentes, setInadimplentes] = useState([]);
  const [arrecadacao, setArrecadacao] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Carregar relatório de inadimplência
  const loadInadimplencia = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await reportService.getInadimplencia();
      setInadimplentes(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Carregar relatório de arrecadação
  const loadArrecadacao = async (ano = new Date().getFullYear()) => {
    setLoading(true);
    setError(null);
    try {
      const data = await reportService.getArrecadacao(ano);
      setArrecadacao(data);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  // Buscar usuários com status financeiro específico
  const getUsersWithFinancialStatus = async (status = null, activeOnly = false) => {
    setLoading(true);
    setError(null);
    try {
      const data = await reportService.getUsersWithFinancialStatus(status, activeOnly);
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return {
    inadimplentes,
    arrecadacao,
    loading,
    error,
    loadInadimplencia,
    loadArrecadacao,
    getUsersWithFinancialStatus
  };
}