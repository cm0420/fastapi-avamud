import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Label } from "./ui/label";
import { Input } from "./ui/input";
import { Button } from "./ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./ui/select";
import { LogIn, Shield, User, Wallet, Loader2, AlertCircle } from "lucide-react";
import { authService } from '../services/apiService';

export function LoginCard({ onLogin }) {
  const [userType, setUserType] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    
    if (!userType) {
      setError("Selecione o tipo de usuário");
      return;
    }
    
    if (!email || !password) {
      setError("Preencha todos os campos");
      return;
    }
    
    setLoading(true);
    
    try {
      // Tentar autenticar com o backend
      const credentials = {
        login: email, // Pode ser login ou email
        password: password
      };
      
      const result = await authService.login(credentials);
      
      if (result.success) {
        // Mapear role do backend (ADMIN, MEMBER) para userType do frontend (administrador, membro, tesoureiro)
        const roleMap = {
          'ADMIN': 'administrador',
          'MEMBER': 'membro',
          'TREASURER': 'tesoureiro'
        };
        
        const userRole = roleMap[result.role] || result.role.toLowerCase();
        
        // Validar se o papel do usuário corresponde ao tipo selecionado
        if (userRole !== userType) {
          setError(`Este usuário não tem permissão de ${userType}. Papel do usuário: ${userRole}`);
          setLoading(false);
          return;
        }
        
        // Extrair nome do username para exibição
        const userName = result.username || email.split("@")[0] || "Usuário";
        
        // Login bem-sucedido - redirecionar para dashboard
        onLogin(userType, userName);
      }
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const getUserIcon = () => {
    switch (userType) {
      case "administrador":
        return <Shield className="w-5 h-5 text-red-600" />;
      case "tesoureiro":
        return <Wallet className="w-5 h-5 text-green-600" />;
      case "membro":
        return <User className="w-5 h-5 text-blue-600" />;
      default:
        return <LogIn className="w-5 h-5 text-gray-600" />;
    }
  };

  const getCardColor = () => {
    switch (userType) {
      case "administrador":
        return "border-red-200 bg-red-50/30";
      case "tesoureiro":
        return "border-green-200 bg-green-50/30";
      case "membro":
        return "border-blue-200 bg-blue-50/30";
      default:
        return "border-gray-200";
    }
  };

  return (
    <Card className={`shadow-lg transition-all duration-300 ${getCardColor()}`}>
      <CardHeader className="space-y-1">
        <div className="flex items-center gap-2 mb-2">
          {getUserIcon()}
          <CardTitle>Acesso ao Sistema</CardTitle>
        </div>
        <CardDescription>
          Entre com suas credenciais para acessar o sistema AVAMUD
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleLogin} className="space-y-4">
          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md flex items-center gap-2">
              <AlertCircle className="h-4 w-4" />
              <span className="text-sm">{error}</span>
            </div>
          )}
          
          {/* User Type Selection */}
          <div className="space-y-2">
            <Label htmlFor="userType">Tipo de Usuário</Label>
            <Select value={userType} onValueChange={setUserType}>
              <SelectValue placeholder="Selecione o tipo de acesso" />
              <SelectItem value="membro">
                <div className="flex items-center gap-2">
                  <User className="w-4 h-4 text-blue-600" />
                  <span>Membro / Associado</span>
                </div>
              </SelectItem>
              <SelectItem value="tesoureiro">
                <div className="flex items-center gap-2">
                  <Wallet className="w-4 h-4 text-green-600" />
                  <span>Tesoureiro</span>
                </div>
              </SelectItem>
              <SelectItem value="administrador">
                <div className="flex items-center gap-2">
                  <Shield className="w-4 h-4 text-red-600" />
                  <span>Administrador</span>
                </div>
              </SelectItem>
            </Select>
          </div>

          {/* Email */}
          <div className="space-y-2">
            <Label htmlFor="email">Login/Email *</Label>
            <Input
              id="email"
              type="text"
              placeholder="Digite seu login ou email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          {/* Password */}
          <div className="space-y-2">
            <Label htmlFor="password">Senha *</Label>
            <Input
              id="password"
              type="password"
              placeholder="Digite sua senha"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {/* Login Button */}
          <Button 
            type="submit" 
            className="w-full"
            disabled={!userType || !email || !password || loading}
          >
            {loading ? (
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <LogIn className="w-4 h-4 mr-2" />
            )}
            {loading ? 'Verificando...' : 'Entrar no Sistema'}
          </Button>

          {/* Additional Links */}
          <div className="text-center space-y-2 pt-2">
            <a href="#" className="text-sm text-blue-600 hover:underline block">
              Esqueci minha senha
            </a>
            <a href="#" className="text-sm text-gray-600 hover:underline block">
              Solicitar cadastro como associado
            </a>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}

export default LoginCard;
