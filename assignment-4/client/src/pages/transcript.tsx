import { PDFViewer } from '@/components/PDFViewer';
import { Inter } from 'next/font/google';
import { parseCookies } from 'nookies';
import React from 'react';

type Props = {};

const inter = Inter({ subsets: ['latin'] });

interface Student {
  name: string;
  rollNumber: string;
}

export default function Transcript({}: Props) {
  const [student, setStudent] = React.useState<Student>({
    name: '',
    rollNumber: '',
  });
  const [buffer, setBuffer] = React.useState<Uint8Array | null>(null);

  const cookies = parseCookies(null);

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    fetch(
      'http://localhost:5000/transcript?name=' +
        student.name +
        '&rollNumber=' +
        student.rollNumber,
      {
        headers: {
          Authorization: `JWT ${cookies.token}`,
        },
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log({ data });
        const signedData = data.signedData;
        const signature = data.signature;
        console.log(Buffer.from(signedData).toString('base64'));
        setTimeout(() => setBuffer(new Uint8Array(data.file.data)), 1000);
      });
  };

  return (
    <div
      className={`flex min-h-screen flex-col items-center p-24 ${inter.className}`}
    >
      <h1 className='text-3xl font-bold'>Transcript</h1>
      {buffer ? (
        <PDFViewer buffer={buffer} />
      ) : (
        <form className='flex flex-col mt-8 space-y-2' onSubmit={handleSubmit}>
          <input
            type='text'
            placeholder='Name'
            className='px-2 py-1 border border-gray-200 rounded'
            onChange={(e) => setStudent({ ...student, name: e.target.value })}
          />
          <input
            type='text'
            placeholder='Roll Number'
            className='px-2 py-1 border border-gray-200 rounded'
            onChange={(e) =>
              setStudent({ ...student, rollNumber: e.target.value })
            }
          />
          <button
            type='submit'
            className='px-2 py-1 text-white bg-blue-500 rounded'
          >
            Request Transcript
          </button>
        </form>
      )}
    </div>
  );
}
