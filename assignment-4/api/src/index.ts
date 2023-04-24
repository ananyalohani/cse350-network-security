import cors from 'cors';
import 'dotenv/config';
import express from 'express';
import jwt from 'jsonwebtoken';
import { users } from './data/users';
import { decrypt } from './helpers/rsa';
import { verifyToken } from './middleware/authJWT';
import { Role } from './types/auth';
import { generatePdfForStudents } from './helpers/pdf';
import { addWatermark, directorSign, registrarSign } from './helpers/sign';
import fs from 'fs';

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
      username,
    },
    message: 'Login successful',
    accessToken: token,
  });
});

app.get('/transcript', verifyToken, (req: any, res) => {
  if (req.user.role !== Role.STUDENT) {
    return res.status(403).json({ message: 'Forbidden' });
  }

  const { rollNumber, name } = req.query;
  if (!rollNumber || !name) {
    return res.status(400).json({ message: 'Bad Request' });
  }

  const file = fs.readFileSync(`./files/transcripts/${rollNumber}.pdf`);
  res.contentType('application/json');
  res.json({ file });
});

app.listen(PORT, async () => {
  console.log(`Example app listening at http://localhost:${PORT}`);
  await generatePdfForStudents();
  const students = users.filter((user) => user.role === Role.STUDENT);
  students.forEach(async (student) => {
    const { username: rollNumber } = student;
    await directorSign(`${rollNumber}.pdf`);
    await registrarSign(`${rollNumber}.pdf`);
    await addWatermark(
      `${rollNumber}.pdf`,
      `Signed by Director IIITD on ${new Date().toDateString()}`,
      'bottom-left'
    );
    await addWatermark(
      `${rollNumber}.pdf`,
      `Signed by Registrar IIITD on ${new Date().toDateString()}`,
      'bottom-right'
    );
  });
});
