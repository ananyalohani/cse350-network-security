import { Role, User } from '../types/auth';

export const users: User[] = [
  {
    username: '2019018',
    password: 'password',
    name: 'Ananya Lohani',
    role: Role.STUDENT,
  },
  {
    username: '2019061',
    password: 'password',
    name: 'Mihir Chaturvedi',
    role: Role.STUDENT,
  },
  {
    username: 'registrar',
    password: 'password',
    role: Role.REGISTRAR,
  },
  {
    username: 'director',
    password: 'password',
    role: Role.DIRECTOR,
  },
];
