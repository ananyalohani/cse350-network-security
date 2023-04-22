import express from 'express';
import { users } from './data/users';
import NodeRSA from 'node-rsa';
import jwt from 'jsonwebtoken';
import 'dotenv/config';

const key = new NodeRSA({ b: 512 });

const app = express();
const PORT = 3000;

app.use(express.json());

app.get('/', (req, res) => {
  return res.json({ message: 'Hello World!' });
});

app.post('/login/user', (req, res) => {
  const { username, encryptedPassword } = req.body;
  const user = users.find((user) => user.username === username);
  if (!user) {
    return res.status(404).json({ message: 'User not found' });
  }

  const password = key.decrypt(encryptedPassword, 'utf8');
  if (user.password !== password) {
    return res.status(401).json({ message: 'Invalid password' });
  }

  const token = jwt.sign({ username }, process.env.API_SECRET, {
    expiresIn: '86400',
  });

  return res.send({
    user: {
      username: username,
      role: username,
    },
    message: 'Login successful',
    accessToken: token,
  });
});

app.listen(PORT, () => {
  console.log(`Example app listening at http://localhost:${PORT}`);
});
