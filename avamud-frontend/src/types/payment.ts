// src/types/payment.ts

import { Decimal } from 'decimal.js';

export interface Payment {
  id: number;
  valor: number | string;
  dataPagamento: string;
  user_id: number;
}

export interface PaymentCreate extends Omit<Payment, 'id'> {
  valor: number | string;
}

export interface PaymentUpdate extends Partial<Omit<Payment, 'id'>> {}
