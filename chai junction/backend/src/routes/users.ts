import express from 'express';
import { body } from 'express-validator';
import {
  getProfile,
  updateProfile,
  updatePassword,
} from '../controllers/users';
import { validateRequest } from '../middleware/validateRequest';
import { auth } from '../middleware/auth';

const router = express.Router();

// Protected routes
router.get('/profile', auth, getProfile);

router.patch(
  '/profile',
  auth,
  [
    body('name').optional().notEmpty().withMessage('Name cannot be empty'),
    body('email').optional().isEmail().withMessage('Please provide a valid email'),
  ],
  validateRequest,
  updateProfile
);

router.patch(
  '/password',
  auth,
  [
    body('currentPassword').notEmpty().withMessage('Current password is required'),
    body('newPassword')
      .isLength({ min: 6 })
      .withMessage('New password must be at least 6 characters long'),
  ],
  validateRequest,
  updatePassword
);

export { router as userRoutes }; 