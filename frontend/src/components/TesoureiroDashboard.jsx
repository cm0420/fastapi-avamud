import { useState, useEffect } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import {
  LogOut,
  Shield,
  DollarSign,
  CreditCard,
  TrendingUp,
  Search,
  Plus,
  Download,
  Calendar,
  Eye,
  Loader2,
  AlertCircle,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { usePayments } from '../hooks/useApi';
import api from '../api';

export function TesoureiroDashboard({ userName, onLogout }) {
  const [activeMenu, setActiveMenu] = useState("overview");
  
  // Hook para dados financeiros via API
  const { 
    payments, 
    paymentHistory, 
    loading: apiLoading, 
    error: apiError, 
    createPayment, 
    getFinancialStats, 
    getTransactionsForDashboard 
  } = usePayments();

  // Dados das transações vêm da API
  const transactions = getTransactionsForDashboard();
  
  // Mock melhorado: dados sincronizados para demonstração
  const [fallbackTransactions] = useState([
    {
      id: "1",
      date: "2025-11-30",
      description: "Mensalidade - Ana Silva",
      amount: 50.00,
      type: "entrada",
      status: "confirmado",
    },
    {
      id: "2", 
      date: "2025-11-29",
      description: "Mensalidade - Bruno Mendes", 
      amount: 50.00,
      type: "entrada",
      status: "confirmado",
    },
    {
      id: "3",
      date: "2025-11-28", 
      description: "Material de escritório",
      amount: 120.50,
      type: "saida",
      status: "confirmado",
    },
    {
      id: "4",
      date: "2025-11-27",
      description: "Mensalidade - Carla Lima",
      amount: 50.00, 
      type: "entrada",
      status: "pendente",
    },
  ]);

  // Calcular totais com dados reais + mock
  const calculateRealTotals = () => {
    const apiTransactions = transactions.length > 0 ? transactions : [];
    const allTransactions = [...apiTransactions, ...fallbackTransactions];
    
    const entradas = allTransactions
      .filter(t => t.type === "entrada" && t.status === "confirmado")
      .reduce((sum, t) => sum + (t.amount || 0), 0);
    
    const saidas = allTransactions
      .filter(t => t.type === "saida" && t.status === "confirmado")
      .reduce((sum, t) => sum + (t.amount || 0), 0);
    
    const pendentes = allTransactions
      .filter(t => t.status === "pendente").length;
    
    return {
      totalEntradas: entradas,
      totalSaidas: saidas,
      saldoAtual: entradas - saidas,
      transacoesPendentes: pendentes
    };
  };

  const realStats = calculateRealTotals();

  const menuItems = [
    {
      id: "overview",
      label: "Visão Geral",
      icon: TrendingUp,
    },
    {
      id: "relatorios",
      label: "Relatórios",
      icon: Download,
    },
  ];

  // Usar totais calculados que combinam dados reais + mock
  const totalEntradas = realStats.totalEntradas;
  const totalSaidas = realStats.totalSaidas;
  const saldoAtual = realStats.saldoAtual;
  const transacoesPendentes = realStats.transacoesPendentes;

  // Combinar transações da API com mock para exibição
  const displayTransactions = transactions.length > 0 
    ? [...transactions, ...fallbackTransactions] 
    : fallbackTransactions;

  // Export CSV helper
  const exportCsv = (txs) => {
    try {
      const headers = ["Data", "Descrição", "Tipo", "Status", "Valor"];
      const rows = txs.map(t => [t.date || '', t.description || '', t.type || '', t.status || '', Number(t.amount || 0).toFixed(2)]);
      const csvContent = [headers, ...rows].map(r => r.map(cell => `"${String(cell).replace(/"/g,'""')}"`).join(',')).join('\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `relatorio_transacoes_${Date.now()}.csv`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('Erro ao exportar CSV', e);
      alert('Erro ao exportar CSV');
    }
  };

  // Map de paymentId -> lista de documentos
  const [documentsMap, setDocumentsMap] = useState({});

  useEffect(() => {
    let mounted = true;
    const fetchDocs = async () => {
      const map = {};
      for (const t of displayTransactions) {
        // tentar converter id para número para chamadas reais
        const paymentId = Number(t.id);
        if (!isNaN(paymentId) && paymentId > 0) {
          try {
            const res = await api.get(`/payments/${paymentId}/documents`);
            if (mounted) map[paymentId] = res.data || [];
          } catch (e) {
            // ignore, sem documentos ou erro
            if (mounted) map[paymentId] = [];
          }
        }
      }
      if (mounted) setDocumentsMap(map);
    };
    fetchDocs();
    return () => { mounted = false };
  }, [displayTransactions]);

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <aside className="w-64 bg-card shadow-lg flex flex-col border-r">
        {/* Header */}
        <div className="p-6 border-b">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
              <Shield className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h2 className="font-bold text-foreground">AVAMUD</h2>
              <p className="text-xs text-muted-foreground">Tesoureiro</p>
            </div>
          </div>
        </div>

        {/* Menu Items */}
        <nav className="flex-1 p-4">
          <div className="space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeMenu === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveMenu(item.id)}
                  className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? "bg-primary/10 text-primary"
                      : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="text-sm font-medium">{item.label}</span>
                </button>
              );
            })}
          </div>
        </nav>

        {/* User Info & Logout */}
        <div className="p-4 border-t">
          <div className="mb-3 px-2">
            <p className="text-sm font-medium text-foreground">{userName}</p>
            <p className="text-xs text-muted-foreground">Tesoureiro</p>
          </div>
          <Button onClick={onLogout} variant="outline" className="w-full">
            <LogOut className="w-4 h-4 mr-2" />
            Sair
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="p-4 lg:p-8">
          {/* Visão Geral */}
          {activeMenu === "overview" && (
            <div className="space-y-6">
              <div>
                <h1 className="text-2xl font-bold text-foreground">Dashboard Financeiro</h1>
                <p className="text-sm text-muted-foreground mt-1">
                  Visão geral das finanças da associação
                </p>
              </div>

              {/* Cards de Resumo */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Saldo Atual</CardTitle>
                    <DollarSign className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-green-600">
                      R$ {saldoAtual.toFixed(2)}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      +2.5% em relação ao mês passado
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Total Entradas</CardTitle>
                    <TrendingUp className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-green-600">
                      R$ {totalEntradas.toFixed(2)}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Este mês
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Total Saídas</CardTitle>
                    <TrendingUp className="h-4 w-4 text-muted-foreground rotate-180" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-red-600">
                      R$ {totalSaidas.toFixed(2)}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Este mês
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                    <CardTitle className="text-sm font-medium">Pendentes</CardTitle>
                    <Calendar className="h-4 w-4 text-muted-foreground" />
                  </CardHeader>
                  <CardContent>
                    <div className="text-2xl font-bold text-yellow-600">
                      {transacoesPendentes}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      Transações pendentes
                    </p>
                  </CardContent>
                </Card>
              </div>

              {/* Últimas Transações */}
              <Card>
                <CardHeader>
                  <CardTitle>Últimas Transações</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {apiLoading ? (
                      <div className="flex items-center justify-center py-4">
                        <Loader2 className="h-4 w-4 animate-spin mr-2" />
                        <span>Carregando transações...</span>
                      </div>
                    ) : apiError ? (
                      <div className="flex items-center justify-center py-4 text-red-600">
                        <AlertCircle className="h-4 w-4 mr-2" />
                        <span>Erro ao carregar dados: {apiError}</span>
                      </div>
                    ) : displayTransactions.slice(0, 5).map((transaction) => (
                      <div key={transaction.id} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className={`w-2 h-2 rounded-full ${
                            transaction.status === "confirmado" 
                              ? "bg-green-500" 
                              : "bg-yellow-500"
                          }`} />
                          <div>
                            <p className="font-medium text-sm">{transaction.description}</p>
                            <p className="text-xs text-muted-foreground">{transaction.date}</p>
                          </div>
                        </div>
                        <div className="text-right">
                          <p className={`font-medium ${
                            transaction.type === "entrada" 
                              ? "text-green-600" 
                              : "text-red-600"
                          }`}>
                            {transaction.type === "entrada" ? "+" : "-"}R$ {transaction.amount.toFixed(2)}
                          </p>
                          <p className="text-xs text-muted-foreground capitalize">
                            {transaction.status}
                          </p>
                          {/* Mostrar anexos, se houver */}
                          {documentsMap[Number(transaction.id)] && documentsMap[Number(transaction.id)].length > 0 && (
                            <div className="mt-2 flex justify-end gap-2">
                              {documentsMap[Number(transaction.id)].map((doc) => (
                                <a key={doc.id} href={`/documents/${doc.id}/download`} className="text-sm text-primary underline" target="_blank" rel="noreferrer">
                                  <Download className="inline w-4 h-4 mr-1" />
                                  {doc.filename}
                                </a>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Relatórios */}
          {activeMenu === "relatorios" && (
            <div>
              <h1 className="text-2xl font-bold text-foreground mb-4">Relatórios</h1>
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm">Resumo</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-2">Saldo Atual</p>
                    <div className="text-xl font-bold">R$ {saldoAtual.toFixed(2)}</div>
                    <p className="text-xs text-muted-foreground mt-3">Total Entradas: R$ {totalEntradas.toFixed(2)}</p>
                    <p className="text-xs text-muted-foreground">Total Saídas: R$ {totalSaidas.toFixed(2)}</p>
                    <p className="text-xs text-muted-foreground">Transações pendentes: {transacoesPendentes}</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm">Período</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-2">Período selecionado</p>
                    <p className="text-xs text-muted-foreground">Últimos 30 dias (dados combinados)</p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle className="text-sm">Exportar</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-2">Exportar relatório CSV</p>
                    <div className="flex gap-2">
                      <Button onClick={() => exportCsv(displayTransactions)}>
                        <Download className="w-4 h-4 mr-2" />Exportar CSV
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>

              <Card>
                <CardHeader>
                  <CardTitle>Transações (amostra)</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="overflow-x-auto">
                    <table className="w-full table-auto text-sm">
                      <thead className="text-left text-xs text-muted-foreground">
                        <tr>
                          <th className="px-3 py-2">Data</th>
                          <th className="px-3 py-2">Descrição</th>
                          <th className="px-3 py-2">Tipo</th>
                          <th className="px-3 py-2">Status</th>
                          <th className="px-3 py-2">Valor</th>
                        </tr>
                      </thead>
                      <tbody>
                        {displayTransactions.map((t) => (
                          <tr key={t.id} className="border-b">
                            <td className="px-3 py-2">{t.date}</td>
                            <td className="px-3 py-2">{t.description}</td>
                            <td className="px-3 py-2 capitalize">{t.type}</td>
                            <td className="px-3 py-2 capitalize">{t.status}</td>
                            <td className="px-3 py-2">R$ {Number(t.amount || 0).toFixed(2)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* helper to export CSV (client-side) */}
          {/**
           * Export function placed here so it can reference `displayTransactions`.
           * It's fine in this component for now; if it grows, refactor into a util.
           */}
          
        </div>
      </main>
    </div>
  );
}

export default TesoureiroDashboard;
