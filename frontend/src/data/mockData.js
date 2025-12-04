/**
 * Dados Mock para Demonstração do Sistema AVAMUD
 * 
 * Este arquivo contém dados fictícios sincronizados entre os diferentes
 * painéis (Membro, Tesoureiro, Administrador) para demonstrar o funcionamento
 * completo do sistema mesmo quando o backend não está disponível.
 */

// Usuários mock do sistema
export const mockUsers = [
  {
    id: 1,
    nome: "Ana Silva",
    cpf: "123.456.789-00",
    email: "ana.silva@email.com",
    telefone: "(11) 98765-4321",
    endereco: "Rua das Flores, 123, Centro",
    status: "ativo",
    dataDeEntrada: "2024-01-15",
    login: "ana.silva",
  },
  {
    id: 2,
    nome: "Bruno Mendes",
    cpf: "987.654.321-00",
    email: "bruno.mendes@email.com",
    telefone: "(11) 98765-4322",
    endereco: "Av. Principal, 456, Jardim",
    status: "ativo",
    dataDeEntrada: "2024-02-20",
    login: "bruno.mendes",
  },
  {
    id: 3,
    nome: "Carla Lima",
    cpf: "456.789.123-00",
    email: "carla.lima@email.com",
    telefone: "(11) 98765-4323",
    endereco: "Rua dos Pinheiros, 789, Vila Nova",
    status: "ativo",
    dataDeEntrada: "2024-03-10",
    login: "carla.lima",
  },
  {
    id: 4,
    nome: "Daniel Costa",
    cpf: "321.654.987-00",
    email: "daniel.costa@email.com",
    telefone: "(11) 98765-4324",
    endereco: "Alameda das Acácias, 321, Parque",
    status: "inativo",
    dataDeEntrada: "2024-01-05",
    login: "daniel.costa",
  },
];

// Transações financeiras mock
export const mockTransactions = [
  {
    id: "1",
    date: "2025-11-30",
    description: "Mensalidade - Ana Silva",
    amount: 50.00,
    type: "entrada",
    status: "confirmado",
    userId: 1,
    userName: "Ana Silva",
    paymentMethod: "PIX",
  },
  {
    id: "2",
    date: "2025-11-29",
    description: "Mensalidade - Bruno Mendes",
    amount: 50.00,
    type: "entrada",
    status: "confirmado",
    userId: 2,
    userName: "Bruno Mendes",
    paymentMethod: "Transferência",
  },
  {
    id: "3",
    date: "2025-11-28",
    description: "Material de escritório",
    amount: 120.50,
    type: "saida",
    status: "confirmado",
    userId: null,
    userName: "Sistema",
    paymentMethod: "Débito",
  },
  {
    id: "4",
    date: "2025-11-27",
    description: "Mensalidade - Carla Lima",
    amount: 50.00,
    type: "entrada",
    status: "pendente",
    userId: 3,
    userName: "Carla Lima",
    paymentMethod: "PIX",
  },
];

// Histórico de pagamentos mock
export const mockPaymentHistory = [
  {
    id: 1,
    paymentId: 1,
    userId: 1,
    action: "Pagamento confirmado",
    actionDate: "2025-11-30T10:30:00",
    amount: 50.00,
  },
  {
    id: 2,
    paymentId: 2,
    userId: 2,
    action: "Pagamento confirmado",
    actionDate: "2025-11-29T14:20:00",
    amount: 50.00,
  },
  {
    id: 3,
    paymentId: 4,
    userId: 3,
    action: "Comprovante enviado - Aguardando validação",
    actionDate: "2025-11-27T09:15:00",
    amount: 50.00,
  },
];

// Estatísticas financeiras calculadas
export const calculateMockStats = () => {
  const entradas = mockTransactions
    .filter(t => t.type === "entrada" && t.status === "confirmado")
    .reduce((sum, t) => sum + t.amount, 0);

  const saidas = mockTransactions
    .filter(t => t.type === "saida" && t.status === "confirmado")
    .reduce((sum, t) => sum + t.amount, 0);

  const pendentes = mockTransactions
    .filter(t => t.status === "pendente").length;

  return {
    totalEntradas: entradas,
    totalSaidas: saidas,
    saldoAtual: entradas - saidas,
    transacoesPendentes: pendentes,
    totalMembros: mockUsers.filter(u => u.status === "ativo").length,
    totalUsuarios: mockUsers.length,
  };
};

// Função para adicionar novo usuário ao mock
export const addMockUser = (userData) => {
  const newUser = {
    id: Math.max(...mockUsers.map(u => u.id)) + 1,
    ...userData,
    dataDeEntrada: new Date().toISOString().split('T')[0],
    status: userData.status || "ativo",
  };
  mockUsers.push(newUser);
  return newUser;
};

// Função para atualizar usuário no mock
export const updateMockUser = (userId, userData) => {
  const index = mockUsers.findIndex(u => u.id === userId);
  if (index !== -1) {
    mockUsers[index] = { ...mockUsers[index], ...userData };
    return mockUsers[index];
  }
  return null;
};

// Função para remover usuário do mock
export const deleteMockUser = (userId) => {
  const index = mockUsers.findIndex(u => u.id === userId);
  if (index !== -1) {
    mockUsers.splice(index, 1);
    return true;
  }
  return false;
};

// Função para adicionar transação ao mock
export const addMockTransaction = (transactionData) => {
  const newTransaction = {
    id: (Math.max(...mockTransactions.map(t => parseInt(t.id))) + 1).toString(),
    date: new Date().toISOString().split('T')[0],
    status: "confirmado",
    ...transactionData,
  };
  mockTransactions.push(newTransaction);
  return newTransaction;
};

export default {
  mockUsers,
  mockTransactions,
  mockPaymentHistory,
  calculateMockStats,
  addMockUser,
  updateMockUser,
  deleteMockUser,
  addMockTransaction,
};
