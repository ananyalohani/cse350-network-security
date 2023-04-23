import { NextFunction, Response } from 'express';
import jwt from 'jsonwebtoken';
import { users } from '../data/users';

export const verifyToken = (req: any, res: Response, next: NextFunction) => {
  if (
    req.headers &&
    req.headers.authorization &&
    req.headers.authorization.split(' ')[0] === 'JWT'
  ) {
    jwt.verify(
      req.headers.authorization.split(' ')[1],
      process.env.API_SECRET as string,
      function (err: any, decoded: any) {
        if (err) req.user = undefined;
        const user = users.find((user) => user.username === decoded.username);
        req.user = user;
        next();
      }
    );
  } else {
    req.user = undefined;
    next();
  }
};
