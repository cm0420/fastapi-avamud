 import api from '../api';

// Serviços para gerenciamento de usuários (membros)
export const userService = {
  // Listar todos os usuários
  async getAllUsers() {
    try {
      const response = await api.get('/api/v1/users');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar usuários:', error);
      throw error;
    }
  },

  // Buscar usuário por ID
  async getUserById(id) {
    try {
      const response = await api.get(`/api/v1/users/${id}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar usuário:', error);
      throw error;
    }
  },

  // Criar novo usuário
  async createUser(userData) {
    try {
      const response = await api.post('/api/v1/users', userData);
      return response.data;
    } catch (error) {
      console.error('Erro ao criar usuário:', error);
      throw error;
    }
  },

  // Atualizar usuário
  async updateUser(id, userData) {
    try {
      const response = await api.put(`/api/v1/users/${id}`, userData);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar usuário:', error);
      throw error;
    }
  },

  // Deletar usuário
  async deleteUser(id) {
    try {
      await api.delete(`/api/v1/users/${id}`);
      return true;
    } catch (error) {
      console.error('Erro ao deletar usuário:', error);
      throw error;
    }
  }
};

// Serviços para gerenciamento de pagamentos
export const paymentService = {
  // Listar todos os pagamentos
  async getAllPayments() {
    try {
      const response = await api.get('/api/v1/payments');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar pagamentos:', error);
      throw error;
    }
  },

  // Buscar pagamento por ID
  async getPaymentById(id) {
    try {
      const response = await api.get(`/api/v1/payments/${id}`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar pagamento:', error);
      throw error;
    }
  },

  // Criar novo pagamento
  async createPayment(paymentData) {
    try {
      const response = await api.post('/api/v1/payments', paymentData);
      return response.data;
    } catch (error) {
      console.error('Erro ao criar pagamento:', error);
      throw error;
    }
  },

  // Atualizar pagamento
  async updatePayment(id, paymentData) {
    try {
      const response = await api.put(`/api/v1/payments/${id}`, paymentData);
      return response.data;
    } catch (error) {
      console.error('Erro ao atualizar pagamento:', error);
      throw error;
    }
  },

  // Deletar pagamento
  async deletePayment(id) {
    try {
      await api.delete(`/api/v1/payments/${id}`);
      return true;
    } catch (error) {
      console.error('Erro ao deletar pagamento:', error);
      throw error;
    }
  },

  // Buscar histórico de um pagamento específico
  async getPaymentHistory(paymentId) {
    try {
      const response = await api.get(`/api/v1/payments/${paymentId}/history`);
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar histórico do pagamento:', error);
      throw error;
    }
  },

  // Buscar todo o histórico de pagamentos
  async getAllPaymentHistory() {
    try {
      const response = await api.get('/api/v1/payments/history');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar histórico de pagamentos:', error);
      throw error;
    }
  }
};

// Serviços para autenticação
export const authService = {
  // Login com validação real
  async login(credentials) {
    try {
      // Mapear dados para formato do backend
      const loginData = {
        username: credentials.login || credentials.username,
        password: credentials.password
      };
      
      const response = await api.post('/api/v1/auth/login', loginData);
      const { token, username, role } = response.data;
      
      if (!token) {
        throw new Error('Token de acesso não recebido');
      }
      
      // Armazenar token no localStorage
      localStorage.setItem('authToken', token);
      
      return { 
        token, 
        username, 
        role, 
        success: true 
      };
    } catch (error) {
      console.error('Erro no login:', error);
      const message = error.response?.data?.error || 
                     error.response?.data?.message || 
                     'Credenciais inválidas';
      throw new Error(message);
    }
  },

  // Logout
  logout() {
    localStorage.removeItem('authToken');
  },

  // Verificar se está logado
  isAuthenticated() {
    return !!localStorage.getItem('authToken');
  },

  // Obter token
  getToken() {
    return localStorage.getItem('authToken');
  }
};

// Serviços para relatórios
export const reportService = {
  // Relatório de inadimplência
  async getInadimplencia() {
    try {
      const response = await api.get('/api/v1/reports/inadimplencia');
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar relatório de inadimplência:', error);
      throw error;
    }
  },

  // Relatório de arrecadação
  async getArrecadacao(ano = new Date().getFullYear()) {
    try {
      const response = await api.get('/api/v1/reports/arrecadacao', {
        params: { ano }
      });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar relatório de arrecadação:', error);
      throw error;
    }
  },

  // Buscar usuários com status financeiro
  async getUsersWithFinancialStatus(status = null, activeOnly = false) {
    try {
      const params = {};
      if (status) params.financial_status = status;
      if (activeOnly) params.active_only = true;

      const response = await api.get('/api/v1/users/', { params });
      return response.data;
    } catch (error) {
      console.error('Erro ao buscar usuários com status financeiro:', error);
      throw error;
    }
  }
};