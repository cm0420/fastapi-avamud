// src/context/AuthContext.tsx

import { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { authService } from '../services/authService';
import { AuthContextType } from '../types/auth';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(() => {
    return localStorage.getItem('access_token');
  });

  const login = async (username: string, password: string) => {
    const newToken = await authService.login(username, password);
    setToken(newToken);
  };

  const logout = () => {
    authService.logout();
    setToken(null);
  };

  const value: AuthContextType = {
    token,
    isAuthenticated: !!token,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
