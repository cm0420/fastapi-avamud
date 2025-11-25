// src/services/userService.ts

import api from './api';
import { User, UserCreate, UserUpdate } from '../types/user';

export const userService = {
  getAll: async (): Promise<User[]> => {
    const response = await api.get<User[]>('/users');
    return response.data;
  },

  getById: async (id: number): Promise<User> => {
    const response = await api.get<User>(`/users/${id}`);
    return response.data;
  },

  create: async (user: UserCreate): Promise<User> => {
    const response = await api.post<User>('/users', user);
    return response.data;
  },

  update: async (id: number, user: UserUpdate): Promise<User> => {
    const response = await api.put<User>(`/users/${id}`, user);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/users/${id}`);
  },
};
