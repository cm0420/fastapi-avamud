// src/services/authService.ts

import api from './api';
import { AuthRequest, AuthResponse } from '../types/auth';

export const authService = {
  login: async (username: string, password: string): Promise<string> => {
    const response = await api.post<AuthResponse>('/auth/login', {
      username,
      password,
    });
    const token = response.data.token;
    localStorage.setItem('access_token', token);
    return token;
  },

  logout: () => {
    localStorage.removeItem('access_token');
  },

  getToken: (): string | null => {
    return localStorage.getItem('access_token');
  },

  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('access_token');
  },
};
