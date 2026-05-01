import express from 'express';
import { body } from 'express-validator';
import {
  getMenuItems,
  getMenuItem,
  createMenuItem,
  updateMenuItem,
  deleteMenuItem,
} from '../controllers/menu';
import { validateRequest } from '../middleware/validateRequest';
import { auth } from '../middleware/auth';

const router = express.Router();

// Public routes
router.get('/', getMenuItems);
router.get('/:id', getMenuItem);

// Protected routes (admin only)
router.post(
  '/',
  auth,
  [
    body('name').notEmpty().withMessage('Name is required'),
    body('description').notEmpty().withMessage('Description is required'),
    body('price').isFloat({ min: 0 }).withMessage('Price must be a positive number'),
    body('category').notEmpty().withMessage('Category is required'),
  ],
  validateRequest,
  createMenuItem
);

router.put(
  '/:id',
  auth,
  [
    body('name').optional().notEmpty().withMessage('Name cannot be empty'),
    body('description').optional().notEmpty().withMessage('Description cannot be empty'),
    body('price').optional().isFloat({ min: 0 }).withMessage('Price must be a positive number'),
    body('category').optional().notEmpty().withMessage('Category cannot be empty'),
  ],
  validateRequest,
  updateMenuItem
);

router.delete('/:id', auth, deleteMenuItem);

export { router as menuRoutes }; 