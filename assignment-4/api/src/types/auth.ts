export interface User {
  username: string;
  password: string;
  name?: string;
  role: Role;
}

export enum Role {
  STUDENT = 'student',
  REGISTRAR = 'registrar',
  DIRECTOR = 'director',
}

export interface LoginRequest {
  username: string;
  encryptedPassword: string;
}

export type DocType = 'transcript' | 'certificate';
