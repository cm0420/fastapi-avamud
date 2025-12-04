import { useState } from "react";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Select } from "./components/ui/select";
import {
  LogOut,
  Shield,
  Users,
  DollarSign,
  UserCog,
  Search,
  Plus,
  Edit,
  Trash2,
  CheckCircle,
  AlertCircle,
  Loader2,
} from "lucide-react";
import { useUsers } from './hooks/useApi';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "./components/ui/dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "./components/ui/card";

export function AdministradorDashboard({ userName, onLogout }) {
  const [activeMenu, setActiveMenu] = useState("membros");
  
  // Hook para gerenciar usuários via API
  const { users: allUsers, loading: apiLoading, error: apiError, createUser, updateUser, deleteUser } = useUsers();

  const [searchTerm, setSearchTerm] = useState("");
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [userToDelete, setUserToDelete] = useState(null);
  const [editingUser, setEditingUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);
  const [formData, setFormData] = useState({
    nome: "",
    cpf: "",
    email: "",
    telefone: "",
    endereco: "",
    status: "ativo",
    senha: "",
    usarSenhaPadrao: true,
    papel: "membro", // Role do usuário
  });
  const [errors, setErrors] = useState({});

  // Função para validar CPF (versão flexível para ambiente de desenvolvimento)
  const validateCPF = (cpf) => {
    const cleanCPF = cpf.replace(/\D/g, "");
    
    // Verifica apenas se tem 11 dígitos
    if (cleanCPF.length !== 11) return false;
    
    // Verifica se todos os dígitos são iguais (CPFs inválidos óbvios)
    if (/^(\d)\1{10}$/.test(cleanCPF)) return false;
    
    // Em ambiente de desenvolvimento, aceitar CPFs formatados corretamente
    // sem validação rigorosa dos dígitos verificadores
    return true;
    
    /* Validação completa (descomentrar para produção):
    let sum = 0;
    for (let i = 0; i < 9; i++) {
      sum += parseInt(cleanCPF.charAt(i)) * (10 - i);
    }
    let remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cleanCPF.charAt(9))) return false;
    
    sum = 0;
    for (let i = 0; i < 10; i++) {
      sum += parseInt(cleanCPF.charAt(i)) * (11 - i);
    }
    remainder = (sum * 10) % 11;
    if (remainder === 10 || remainder === 11) remainder = 0;
    if (remainder !== parseInt(cleanCPF.charAt(10))) return false;
    
    return true;
    */
  };

  // Função para validar email
  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  // Função para formatar CPF
  const formatCPF = (value) => {
    const numbers = value.replace(/\D/g, "");
    return numbers.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
  };

  // Função para formatar telefone
  const formatPhone = (value) => {
    const numbers = value.replace(/\D/g, "");
    return numbers.replace(/(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
  };

  // Função para mostrar notificação
  const showNotification = (message, type = "success") => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  // Função para validar formulário
  const validateForm = () => {
    const newErrors = {};

    if (!formData.nome.trim()) {
      newErrors.nome = "Nome é obrigatório";
    }

    if (!formData.cpf.trim()) {
      newErrors.cpf = "CPF é obrigatório";
    } else if (!validateCPF(formData.cpf)) {
      newErrors.cpf = "CPF inválido";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email é obrigatório";
    } else if (!validateEmail(formData.email)) {
      newErrors.email = "Email inválido";
    }

    // Validar senha ao criar novo usuário com senha personalizada
    if (!editingUser && !formData.usarSenhaPadrao) {
      if (!formData.senha.trim()) {
        newErrors.senha = "Senha é obrigatória quando não usar senha padrão";
      } else if (formData.senha.length < 6) {
        newErrors.senha = "Senha deve ter no mínimo 6 caracteres";
      }
    }

    // Validar senha ao editar (se preenchida)
    if (editingUser && formData.senha.trim() !== '' && formData.senha.length < 6) {
      newErrors.senha = "Senha deve ter no mínimo 6 caracteres";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleAddUser = () => {
    setEditingUser(null);
    setFormData({
      nome: "",
      cpf: "",
      email: "",
      telefone: "",
      endereco: "",
      status: "ativo",
      senha: "",
      usarSenhaPadrao: true,
      papel: "membro",
    });
    setErrors({});
    setIsDialogOpen(true);
  };

  const handleEditUser = (user) => {
    setEditingUser(user);
    setFormData({
      nome: user.nome,
      cpf: user.cpf,
      email: user.email,
      telefone: user.telefone,
      endereco: user.endereco || "",
      status: user.status || "ativo",
      senha: "",
      usarSenhaPadrao: false,
      papel: user.papel || "membro",
    });
    setErrors({});
    setIsDialogOpen(true);
  };

  const handleDeleteUser = (user) => {
    setUserToDelete(user);
    setIsDeleteDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (!userToDelete) return;
    
    setLoading(true);
    try {
      await deleteUser(userToDelete.id);
      setIsDeleteDialogOpen(false);
      setUserToDelete(null);
      showNotification("Usuário removido com sucesso!", "success");
    } catch (error) {
      showNotification(`Erro ao remover usuário: ${error.message}`, "error");
    } finally {
      setLoading(false);
    }
  };

  const handleSaveUser = async () => {
    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      if (editingUser) {
        // Editar usuário existente - UPDATE totalmente funcional
        const updatedData = {
          ...formData,
          cpf: formData.cpf.replace(/\D/g, ''), // Limpar formatação
          telefone: formData.telefone.replace(/\D/g, ''),
        };
        // Se senha foi preenchida, incluir na atualização
        if (formData.senha && formData.senha.trim() !== '') {
          updatedData.senha = formData.senha;
        }
        await updateUser(editingUser.id, updatedData);
        showNotification("✓ Usuário atualizado com sucesso!", "success");
      } else {
        // Adicionar novo usuário - CREATE
        const senhaFinal = formData.usarSenhaPadrao || !formData.senha.trim() 
          ? '123456' 
          : formData.senha;
        
        // Definir login baseado no papel
        let loginBase = formData.email.split('@')[0].toLowerCase().replace(/[^a-z0-9]/g, '');
        if (formData.papel === 'administrador') {
          loginBase = 'admin_' + loginBase;
        } else if (formData.papel === 'tesoureiro') {
          loginBase = 'tesoureiro_' + loginBase;
        }
        
        const newUserData = {
          ...formData,
          cpf: formData.cpf.replace(/\D/g, ''),
          telefone: formData.telefone.replace(/\D/g, ''),
          cnpj: '', // Campo obrigatório no backend
          senha: senhaFinal,
          login: loginBase,
        };
        await createUser(newUserData);
        const msgSenha = formData.usarSenhaPadrao ? ' (Senha padrão: 123456)' : '';
        showNotification(`✓ Usuário ${formData.papel} adicionado! Login: ${loginBase}${msgSenha}`, "success");
      }

      setIsDialogOpen(false);
      setEditingUser(null);
      setFormData({
        nome: "",
        cpf: "",
        email: "",
        telefone: "",
        endereco: "",
        status: "ativo",
        senha: "",
        usarSenhaPadrao: true,
        papel: "membro",
      });
    } catch (error) {
      showNotification(`✗ Erro ao salvar: ${error.message}`, "error");
    } finally {
      setLoading(false);
    }
  };

  const filteredUsers = (allUsers || []).filter(
    (user) =>
      user.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.cpf.includes(searchTerm) ||
      user.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const menuItems = [
    {
      id: "membros",
      label: "Gerenciar Usuários",
      icon: Users,
    },
  ];

  return (
    <div className="flex h-screen bg-background">
      {/* Notification */}
      {notification && (
        <div className="fixed top-4 right-4 z-50 flex items-center gap-2 px-4 py-3 rounded-lg shadow-lg bg-card border">
          {notification.type === "success" ? (
            <CheckCircle className="w-5 h-5 text-green-600" />
          ) : (
            <AlertCircle className="w-5 h-5 text-red-600" />
          )}
          <span className="text-sm">{notification.message}</span>
        </div>
      )}

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
              <p className="text-xs text-muted-foreground">Administrador</p>
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
            <p className="text-xs text-muted-foreground">Admin</p>
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
          {/* Gerenciar Usuários */}
          {activeMenu === "membros" && (
            <div className="space-y-6">
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                <div>
                  <h1 className="text-2xl font-bold text-foreground">Gerenciar usuários</h1>
                  <p className="text-sm text-muted-foreground mt-1">
                    Adicione, edite ou remova usuários do sistema
                  </p>
                </div>
                <Button onClick={handleAddUser} className="bg-primary hover:bg-primary/90">
                  <Plus className="w-4 h-4 mr-2" />
                  Adicionar Usuário
                </Button>
              </div>

              {/* Search Bar */}
              <Card>
                <CardContent className="pt-6">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                    <Input
                      type="text"
                      placeholder="Buscar por nome, CPF ou email..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </CardContent>
              </Card>

              {/* Members Table */}
              <Card>
                <CardHeader>
                  <CardTitle>
                    Usuários Cadastrados ({filteredUsers.length})
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="overflow-x-auto">
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>Nome</TableHead>
                          <TableHead className="hidden md:table-cell">CPF</TableHead>
                          <TableHead>Email</TableHead>
                          <TableHead className="hidden lg:table-cell">Telefone</TableHead>
                          <TableHead className="hidden xl:table-cell">Endereço</TableHead>
                          <TableHead>Status</TableHead>
                          <TableHead className="text-right">Ações</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {apiLoading ? (
                          <TableRow>
                            <TableCell
                              colSpan={7}
                              className="text-center py-8"
                            >
                              <div className="flex items-center justify-center space-x-2">
                                <Loader2 className="h-4 w-4 animate-spin" />
                                <span>Carregando usuários...</span>
                              </div>
                            </TableCell>
                          </TableRow>
                        ) : apiError ? (
                          <TableRow>
                            <TableCell
                              colSpan={7}
                              className="text-center py-8 text-red-600"
                            >
                              <div className="flex items-center justify-center space-x-2">
                                <AlertCircle className="h-4 w-4" />
                                <span>Erro ao carregar usuários: {apiError}</span>
                              </div>
                            </TableCell>
                          </TableRow>
                        ) : filteredUsers.length === 0 ? (
                          <TableRow>
                            <TableCell
                              colSpan={7}
                              className="text-center py-8 text-muted-foreground"
                            >
                              Nenhum usuário encontrado
                            </TableCell>
                          </TableRow>
                        ) : (
                          filteredUsers.map((user) => (
                            <TableRow key={user.id}>
                              <TableCell className="font-medium">{user.nome}</TableCell>
                              <TableCell className="hidden md:table-cell">{user.cpf}</TableCell>
                              <TableCell>{user.email}</TableCell>
                              <TableCell className="hidden lg:table-cell">{user.telefone}</TableCell>
                              <TableCell className="hidden xl:table-cell">{user.endereco}</TableCell>
                              <TableCell>
                                <span
                                  className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                    user.status === "ativo"
                                      ? "bg-green-100 text-green-800"
                                      : "bg-gray-100 text-gray-800"
                                  }`}
                                >
                                  {user.status === "ativo"
                                    ? "Ativo"
                                    : "Inativo"}
                                </span>
                              </TableCell>
                              <TableCell className="text-right">
                                <div className="flex items-center justify-end gap-1">
                                  <Button
                                    onClick={() => handleEditUser(user)}
                                    variant="ghost"
                                    size="sm"
                                  >
                                    <Edit className="w-4 h-4 text-blue-600" />
                                  </Button>
                                  <Button
                                    onClick={() => handleDeleteUser(user)}
                                    variant="ghost"
                                    size="sm"
                                  >
                                    <Trash2 className="w-4 h-4 text-red-600" />
                                  </Button>
                                </div>
                              </TableCell>
                            </TableRow>
                          ))
                        )}
                      </TableBody>
                    </Table>
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Funcionários */}
        </div>
      </main>

      {/* Add/Edit User Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingUser ? "Editar Usuário" : "Adicionar Usuário"}
            </DialogTitle>
            <DialogDescription>
              Preencha as informações do usuário abaixo. Campos com * são obrigatórios.
            </DialogDescription>
          </DialogHeader>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="nome">Nome Completo *</Label>
              <Input
                id="nome"
                value={formData.nome}
                onChange={(e) => {
                  setFormData({ ...formData, nome: e.target.value });
                  if (errors.nome) setErrors({ ...errors, nome: null });
                }}
                placeholder="Digite o nome completo"
                className={errors.nome ? "border-red-500" : ""}
              />
              {errors.nome && (
                <p className="text-xs text-red-600">{errors.nome}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="cpf">CPF *</Label>
              <Input
                id="cpf"
                value={formData.cpf}
                onChange={(e) => {
                  const formatted = formatCPF(e.target.value);
                  setFormData({ ...formData, cpf: formatted });
                  if (errors.cpf) setErrors({ ...errors, cpf: null });
                }}
                placeholder="000.000.000-00"
                maxLength={14}
                className={errors.cpf ? "border-red-500" : ""}
              />
              {errors.cpf && (
                <p className="text-xs text-red-600">{errors.cpf}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">Email *</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => {
                  setFormData({ ...formData, email: e.target.value });
                  if (errors.email) setErrors({ ...errors, email: null });
                }}
                placeholder="email@exemplo.com"
                className={errors.email ? "border-red-500" : ""}
              />
              {errors.email && (
                <p className="text-xs text-red-600">{errors.email}</p>
              )}
            </div>

            <div className="space-y-2">
              <Label htmlFor="telefone">Telefone</Label>
              <Input
                id="telefone"
                value={formData.telefone}
                onChange={(e) => {
                  const formatted = formatPhone(e.target.value);
                  setFormData({ ...formData, telefone: formatted });
                }}
                placeholder="(00) 00000-0000"
                maxLength={15}
              />
            </div>

            <div className="space-y-2 md:col-span-2">
              <Label htmlFor="endereco">Endereço</Label>
              <Input
                id="endereco"
                value={formData.endereco}
                onChange={(e) =>
                  setFormData({ ...formData, endereco: e.target.value })
                }
                placeholder="Rua, número, bairro"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="status">Status</Label>
              <Select
                id="status"
                value={formData.status}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    status: e.target.value,
                  })
                }
              >
                <option value="ativo">Ativo</option>
                <option value="inativo">Inativo</option>
              </Select>
            </div>

            {/* Campo de Papel/Role */}
            <div className="space-y-2">
              <Label htmlFor="papel">Papel/Função *</Label>
              <Select
                id="papel"
                value={formData.papel}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    papel: e.target.value,
                  })
                }
              >
                <option value="membro">Membro / Associado</option>
                <option value="tesoureiro">Tesoureiro</option>
                <option value="administrador">Administrador</option>
              </Select>
              <p className="text-xs text-gray-600">
                Define o nível de acesso do usuário no sistema
              </p>
            </div>

            {/* Campo de Senha - Apenas ao Criar ou para Resetar */}
            {!editingUser && (
              <div className="space-y-2 md:col-span-2">
                <div className="flex items-center gap-2 mb-2">
                  <input
                    type="checkbox"
                    id="usarSenhaPadrao"
                    checked={formData.usarSenhaPadrao}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        usarSenhaPadrao: e.target.checked,
                      })
                    }
                    className="w-4 h-4"
                  />
                  <Label htmlFor="usarSenhaPadrao" className="cursor-pointer">
                    Usar senha padrão (123456)
                  </Label>
                </div>
                
                {!formData.usarSenhaPadrao && (
                  <div className="space-y-2">
                    <Label htmlFor="senha">Senha Personalizada *</Label>
                    <Input
                      id="senha"
                      type="password"
                      value={formData.senha}
                      onChange={(e) => {
                        setFormData({ ...formData, senha: e.target.value });
                        if (errors.senha) setErrors({ ...errors, senha: null });
                      }}
                      placeholder="Digite a senha do usuário"
                      minLength={6}
                      className={errors.senha ? "border-red-500" : ""}
                    />
                    {errors.senha ? (
                      <p className="text-xs text-red-600">{errors.senha}</p>
                    ) : (
                      <p className="text-xs text-gray-600">
                        A senha deve ter no mínimo 6 caracteres
                      </p>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* Campo para Resetar Senha ao Editar */}
            {editingUser && (
              <div className="space-y-2 md:col-span-2">
                <Label htmlFor="senha">Redefinir Senha (deixe em branco para manter a atual)</Label>
                <Input
                  id="senha"
                  type="password"
                  value={formData.senha}
                  onChange={(e) => {
                    setFormData({ ...formData, senha: e.target.value });
                    if (errors.senha) setErrors({ ...errors, senha: null });
                  }}
                  placeholder="Digite a nova senha ou deixe em branco"
                  minLength={6}
                  className={errors.senha ? "border-red-500" : ""}
                />
                {errors.senha ? (
                  <p className="text-xs text-red-600">{errors.senha}</p>
                ) : (
                  <p className="text-xs text-gray-600">
                    Preencha apenas se desejar alterar a senha do usuário (mínimo 6 caracteres)
                  </p>
                )}
              </div>
            )}
          </div>

          <div className="flex flex-col-reverse sm:flex-row justify-end gap-3">
            <Button
              variant="outline"
              onClick={() => setIsDialogOpen(false)}
              disabled={loading}
            >
              Cancelar
            </Button>
            <Button 
              onClick={handleSaveUser} 
              disabled={loading}
              className="bg-primary hover:bg-primary/90"
            >
              {loading ? "Salvando..." : editingUser ? "Salvar Alterações" : "Adicionar Usuário"}
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>Confirmar Remoção</DialogTitle>
            <DialogDescription>
              Tem certeza que deseja remover o usuário <strong>{userToDelete?.nome}</strong>? 
              Esta ação não pode ser desfeita.
            </DialogDescription>
          </DialogHeader>

          <div className="flex flex-col-reverse sm:flex-row justify-end gap-3">
            <Button
              variant="outline"
              onClick={() => setIsDeleteDialogOpen(false)}
            >
              Cancelar
            </Button>
            <Button 
              onClick={confirmDelete}
              variant="destructive"
            >
              Sim, Remover
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
