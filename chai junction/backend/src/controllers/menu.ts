import { Request, Response } from 'express';
import { MenuItem } from '../models/MenuItem';
import { AppError } from '../middleware/errorHandler';

export const getMenuItems = async (req: Request, res: Response) => {
  const { category } = req.query;
  const query = category ? { category } : {};

  const menuItems = await MenuItem.find(query).sort({ createdAt: -1 });
  res.json({ success: true, data: menuItems });
};

export const getMenuItem = async (req: Request, res: Response) => {
  const menuItem = await MenuItem.findById(req.params.id);
  if (!menuItem) {
    throw new AppError('Menu item not found', 404);
  }
  res.json({ success: true, data: menuItem });
};

export const createMenuItem = async (req: Request, res: Response) => {
  const menuItem = await MenuItem.create(req.body);
  res.status(201).json({ success: true, data: menuItem });
};

export const updateMenuItem = async (req: Request, res: Response) => {
  const menuItem = await MenuItem.findByIdAndUpdate(
    req.params.id,
    req.body,
    { new: true, runValidators: true }
  );
  if (!menuItem) {
    throw new AppError('Menu item not found', 404);
  }
  res.json({ success: true, data: menuItem });
};

export const deleteMenuItem = async (req: Request, res: Response) => {
  const menuItem = await MenuItem.findByIdAndDelete(req.params.id);
  if (!menuItem) {
    throw new AppError('Menu item not found', 404);
  }
  res.json({ success: true, data: {} });
}; 