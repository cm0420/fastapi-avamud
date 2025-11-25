// src/services/paymentService.ts

import api from './api';
import { Payment, PaymentCreate, PaymentUpdate } from '../types/payment';

export const paymentService = {
  getAll: async (): Promise<Payment[]> => {
    const response = await api.get<Payment[]>('/payments');
    return response.data;
  },

  getById: async (id: number): Promise<Payment> => {
    const response = await api.get<Payment>(`/payments/${id}`);
    return response.data;
  },

  getByUserId: async (userId: number): Promise<Payment[]> => {
    const response = await api.get<Payment[]>(`/payments/user/${userId}`);
    return response.data;
  },

  create: async (payment: PaymentCreate): Promise<Payment> => {
    const response = await api.post<Payment>('/payments', payment);
    return response.data;
  },

  update: async (id: number, payment: PaymentUpdate): Promise<Payment> => {
    const response = await api.put<Payment>(`/payments/${id}`, payment);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/payments/${id}`);
  },
};
