import express from 'express';
import { body } from 'express-validator';
import {
  createOrder,
  getOrders,
  getOrder,
  updateOrderStatus,
} from '../controllers/orders';
import { validateRequest } from '../middleware/validateRequest';
import { auth } from '../middleware/auth';

const router = express.Router();

// Protected routes
router.post(
  '/',
  auth,
  [
    body('items').isArray().withMessage('Items must be an array'),
    body('items.*.menuItemId').notEmpty().withMessage('Menu item ID is required'),
    body('items.*.quantity').isInt({ min: 1 }).withMessage('Quantity must be at least 1'),
    body('deliveryAddress').notEmpty().withMessage('Delivery address is required'),
    body('paymentMethod').notEmpty().withMessage('Payment method is required'),
  ],
  validateRequest,
  createOrder
);

router.get('/', auth, getOrders);
router.get('/:id', auth, getOrder);

// Admin only route
router.patch(
  '/:id/status',
  auth,
  [
    body('status').isIn(['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled'])
      .withMessage('Invalid status'),
  ],
  validateRequest,
  updateOrderStatus
);

export { router as orderRoutes }; 