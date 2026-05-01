import { Request, Response } from 'express';
import { Order } from '../models/Order';
import { MenuItem } from '../models/MenuItem';
import { AppError } from '../middleware/errorHandler';
import Stripe from 'stripe';
import { config } from '../config';

const getStripe = (() => {
  let client: Stripe | null = null;
  return () => {
    if (!config.stripe.secretKey) throw new AppError('Stripe is not configured', 503);
    if (!client) client = new Stripe(config.stripe.secretKey, { apiVersion: '2023-10-16' });
    return client;
  };
})();

export const createOrder = async (req: Request, res: Response) => {
  const { items, deliveryAddress, paymentMethod } = req.body;
  const userId = req.user._id;

  // Calculate total amount
  let totalAmount = 0;
  const orderItems = [];

  for (const item of items) {
    const menuItem = await MenuItem.findById(item.menuItemId);
    if (!menuItem) {
      throw new AppError(`Menu item ${item.menuItemId} not found`, 404);
    }
    if (!menuItem.isAvailable) {
      throw new AppError(`Menu item ${menuItem.name} is not available`, 400);
    }

    totalAmount += menuItem.price * item.quantity;
    orderItems.push({
      menuItem: item.menuItemId,
      quantity: item.quantity,
      price: menuItem.price,
    });
  }

  // Create Stripe payment intent
  const paymentIntent = await getStripe().paymentIntents.create({
    amount: Math.round(totalAmount * 100), // Convert to cents
    currency: 'eur',
    payment_method: paymentMethod,
    confirm: true,
  });

  // Create order
  const order = await Order.create({
    user: userId,
    items: orderItems,
    totalAmount,
    deliveryAddress,
    paymentIntentId: paymentIntent.id,
    status: 'pending',
  });

  res.status(201).json({ success: true, data: order });
};

export const getOrders = async (req: Request, res: Response) => {
  const orders = await Order.find({ user: req.user._id })
    .populate('items.menuItem')
    .sort({ createdAt: -1 });
  res.json({ success: true, data: orders });
};

export const getOrder = async (req: Request, res: Response) => {
  const order = await Order.findOne({
    _id: req.params.id,
    user: req.user._id,
  }).populate('items.menuItem');

  if (!order) {
    throw new AppError('Order not found', 404);
  }

  res.json({ success: true, data: order });
};

export const updateOrderStatus = async (req: Request, res: Response) => {
  const { status } = req.body;
  const order = await Order.findByIdAndUpdate(
    req.params.id,
    { status },
    { new: true, runValidators: true }
  ).populate('items.menuItem');

  if (!order) {
    throw new AppError('Order not found', 404);
  }

  res.json({ success: true, data: order });
}; 