// src/types/user.ts

export interface User {
  id: number;
  nome: string;
  cpf: string;
  cnpj: string;
  email: string;
  login: string;
  telefone: string;
  dataDeEntrada?: string;
}

export interface UserCreate extends Omit<User, 'id' | 'dataDeEntrada'> {
  senha: string;
}

export interface UserUpdate extends Partial<Omit<User, 'id'>> {
  senha?: string;
}
