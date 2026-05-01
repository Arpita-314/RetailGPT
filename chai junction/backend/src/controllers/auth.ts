import { Request, Response } from 'express';
import jwt from 'jsonwebtoken';
import { User } from '../models/User';
import { config } from '../config';
import { AppError } from '../middleware/errorHandler';

export const register = async (req: Request, res: Response) => {
  const { email, password, name } = req.body;

  // Check if user already exists
  const existingUser = await User.findOne({ email });
  if (existingUser) {
    throw new AppError('User already exists', 400);
  }

  // Create user — password hashing is handled by the User model pre-save hook
  const user = await User.create({
    email,
    password,
    name,
  });

  // Generate JWT token
  const token = jwt.sign(
    { userId: user._id },
    config.jwtSecret,
    { expiresIn: config.jwtExpiresIn }
  );

  res.status(201).json({
    success: true,
    token,
    user: {
      id: user._id,
      email: user.email,
      name: user.name,
    },
  });
};

export const login = async (req: Request, res: Response) => {
  const { email, password } = req.body;

  // Check if user exists
  const user = await User.findOne({ email });
  if (!user) {
    throw new AppError('Invalid credentials', 401);
  }

  // Check password using the model's comparePassword method
  const isMatch = await user.comparePassword(password);
  if (!isMatch) {
    throw new AppError('Invalid credentials', 401);
  }

  // Generate JWT token
  const token = jwt.sign(
    { userId: user._id },
    config.jwtSecret,
    { expiresIn: config.jwtExpiresIn }
  );

  res.json({
    success: true,
    token,
    user: {
      id: user._id,
      email: user.email,
      name: user.name,
    },
  });
};

export const logout = (req: Request, res: Response) => {
  res.json({ success: true, message: 'Logged out successfully' });
}; 