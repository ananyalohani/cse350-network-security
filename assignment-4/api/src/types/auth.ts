export interface User {
  username: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  encryptedPassword: string;
}
