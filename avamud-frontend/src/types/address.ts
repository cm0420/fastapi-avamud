// src/types/address.ts

export interface Address {
  id: number;
  rua: string;
  numero: string;
  bairro: string;
  cidade: string;
  estado: string;
  cep: string;
  user_id: number;
}

export interface AddressCreate extends Omit<Address, 'id'> {}

export interface AddressUpdate extends Partial<Omit<Address, 'id'>> {}
