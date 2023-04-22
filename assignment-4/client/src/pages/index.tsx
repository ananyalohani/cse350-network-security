import { Inter } from 'next/font/google';
import { FormEventHandler, useEffect, useState } from 'react';
import { GetServerSideProps } from 'next';
import { encrypt } from '@/helpers/rsa';
import { User } from '@/types';

const inter = Inter({ subsets: ['latin'] });

export default function Home() {
  const [user, setUser] = useState<User>({ username: '', password: '' });

  const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();
    const response = await fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: user.username,
        encryptedPassword: encrypt(user.password),
      }),
    });
    const data = await response.json();
    console.log(data);
  };

  return (
    <main
      className={`flex min-h-screen flex-col items-center p-24 ${inter.className}`}
    >
      <h1 className='text-3xl font-bold'>User Login</h1>
      <form className='flex flex-col space-y-2 mt-8' onSubmit={handleSubmit}>
        <input
          type='text'
          placeholder='Username'
          className='border border-gray-200 rounded py-1 px-2'
          onChange={(e) => {
            setUser({ ...user, username: e.target.value });
          }}
        />
        <input
          type='password'
          placeholder='Password'
          className='border border-gray-200 rounded py-1 px-2'
          onChange={(e) => {
            setUser({ ...user, password: e.target.value });
          }}
        />
        <button
          type='submit'
          className='bg-blue-500 rounded py-1 px-2 text-white'
        >
          Login
        </button>
      </form>
    </main>
  );
}
