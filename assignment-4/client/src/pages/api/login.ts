// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { User } from '@/types';
import type { NextApiRequest, NextApiResponse } from 'next';
import NodeRSA from 'node-rsa';

type Data = {
  publicKey: string;
  user: User;
};

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { publicKey, user } = req.body;
  const key = new NodeRSA(publicKey, 'public');
  return key.encrypt(user, 'base64');
}
