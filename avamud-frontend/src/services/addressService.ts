// src/services/addressService.ts

import api from './api';
import { Address, AddressCreate, AddressUpdate } from '../types/address';

export const addressService = {
  getAll: async (): Promise<Address[]> => {
    const response = await api.get<Address[]>('/addresses');
    return response.data;
  },

  getById: async (id: number): Promise<Address> => {
    const response = await api.get<Address>(`/addresses/${id}`);
    return response.data;
  },

  getByUserId: async (userId: number): Promise<Address[]> => {
    const response = await api.get<Address[]>(`/addresses/user/${userId}`);
    return response.data;
  },

  create: async (address: AddressCreate): Promise<Address> => {
    const response = await api.post<Address>('/addresses', address);
    return response.data;
  },

  update: async (id: number, address: AddressUpdate): Promise<Address> => {
    const response = await api.put<Address>(`/addresses/${id}`, address);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/addresses/${id}`);
  },
};
