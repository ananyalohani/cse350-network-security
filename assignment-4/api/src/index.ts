import cors from 'cors';
import 'dotenv/config';
import express from 'express';
import jwt from 'jsonwebtoken';
import { users } from './data/users';
import { decrypt } from './helpers/rsa';
import { verifyToken } from './middleware/authJWT';
import { Role } from './types/auth';
import { generatePdfForStudents } from './helpers/pdf';

const app = express();
const PORT = 5000;

app.use(express.json());

app.use(
  cors({
    origin: [process.env.CLIENT_ORIGIN as string],
    methods: 'GET, HEAD, PUT, PATCH, POST, DELETE, OPTIONS',
    credentials: true,
  })
);

app.get('/', (req, res) => {
  return res.json({ message: 'Hello World!' });
});

app.post('/login', (req, res) => {
  const { username, encryptedPassword } = req.body;
  const user = users.find((user) => user.username === username);
  if (!user) {
    return res.status(404).json({ message: 'User not found' });
  }

  const password = decrypt(encryptedPassword);
  if (user.password !== password) {
    return res.status(401).json({ message: 'Invalid password' });
  }

  const token = jwt.sign({ username }, process.env.API_SECRET as string, {
    expiresIn: '86400',
  });

  return res.send({
    user: {
      username: username,
    },
    message: 'Login successful',
    accessToken: token,
  });
});

app.post('/hidden', verifyToken, (req: any, res) => {
  if (!req.user) {
    return res.status(401).json({ message: 'Unauthorized' });
  }
  if (req.user.username !== 'admin') {
    return res.status(403).json({ message: 'Forbidden' });
  }
  return res.json({ message: 'This is a secret message' });
});

app.get('/transcript', verifyToken, (req: any, res) => {
  if (req.user.role !== Role.STUDENT) {
    return res.status(403).json({ message: 'Forbidden' });
  }

  const { rollNumber, name } = req.query;
  if (!rollNumber || !name) {
    return res.status(400).json({ message: 'Bad Request' });
  }
});

app.listen(PORT, async () => {
  console.log(`Example app listening at http://localhost:${PORT}`);
  await generatePdfForStudents();
});
