import { encrypt } from '@/helpers/rsa';
import { User } from '@/types';

import jwt_decode from 'jwt-decode';
import { GetServerSideProps } from 'next';
import { Inter } from 'next/font/google';
import { useRouter } from 'next/router';
import nookies, { setCookie } from 'nookies';
import { FormEventHandler, useState } from 'react';

export const getServerSideProps: GetServerSideProps = async (ctx) => {
  const cookies = nookies.get(ctx);
  if (cookies.token) {
    const decoded: any = jwt_decode(cookies.token);

    if (decoded.exp * 1000 < Date.now()) {
      nookies.destroy(ctx, 'token');
      return {
        props: {},
      };
    }

    if (decoded.username === 'user') {
      return {
        redirect: {
          destination: '/transcript',
          permanent: false,
        },
      };
    } else if (
      decoded.username === 'registrar' ||
      decoded.username === 'director'
    ) {
      return {
        redirect: {
          destination: '/sign',
          permanent: false,
        },
      };
    }
  }

  return {
    props: {},
  };
};

const inter = Inter({ subsets: ['latin'] });

export default function Home() {
  const [user, setUser] = useState<User>({ username: '', password: '' });
  const router = useRouter();

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

    if (data.accessToken) {
      setCookie(null, 'token', data.accessToken, {
        maxAge: 30 * 24 * 60 * 60,
        path: '/',
      });

      if (user.username === 'user') {
        router.push('/transcript');
      } else if (
        user.username === 'registrar' ||
        user.username === 'director'
      ) {
        router.push('/sign');
      }
    }

    const res = await fetch('http://localhost:5000/hidden', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `JWT ${data.accessToken}`,
      },
      body: JSON.stringify({
        username: user.username,
      }),
    });
    const d = await res.json();
    console.log(d);
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
