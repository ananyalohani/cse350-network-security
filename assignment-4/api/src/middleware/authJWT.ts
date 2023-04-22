import jwt from 'jsonwebtoken';
import { users } from '../data/users';
import { NextFunction, Request, Response } from 'express';

export const verifyToken = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  if (
    req.headers &&
    req.headers.authorization &&
    req.headers.authorization.split(' ')[0] === 'JWT'
  ) {
    jwt.verify(
      req.headers.authorization.split(' ')[1],
      process.env.API_SECRET as string,
      function (err, decode) {
        // @ts-ignore
        if (err) req.user = undefined;
        const user = users.find((user) => user.username === req.body.username);
        // @ts-ignore
        req.user = user;
        next();
      }
    );
  } else {
    // @ts-ignore
    req.user = undefined;
    next();
  }
};
