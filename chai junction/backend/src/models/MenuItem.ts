import mongoose from 'mongoose';

interface IMenuItem extends mongoose.Document {
  name: string;
  description: string;
  price: number;
  category: string;
  imageUrl?: string;
  isAvailable: boolean;
  rating?: number;
  reviewCount?: number;
}

const menuItemSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true,
  },
  description: {
    type: String,
    required: true,
  },
  price: {
    type: Number,
    required: true,
    min: 0,
  },
  category: {
    type: String,
    required: true,
    enum: ['chai', 'snacks', 'desserts', 'seasonal'],
  },
  imageUrl: {
    type: String,
  },
  isAvailable: {
    type: Boolean,
    default: true,
  },
  rating: {
    type: Number,
    default: 0,
    min: 0,
    max: 5,
  },
  reviewCount: {
    type: Number,
    default: 0,
  },
}, {
  timestamps: true,
});

export const MenuItem = mongoose.model<IMenuItem>('MenuItem', menuItemSchema); 