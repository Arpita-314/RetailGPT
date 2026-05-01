import React, { useState } from 'react';
import {
  Box,
  Typography,
  Container,
  Card,
  CardContent,
  TextField,
  Button,
  Divider,
  FormControlLabel,
  Checkbox,
} from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../store';
import { clearCart } from '../store/cartSlice';
import { useNavigate } from 'react-router-dom';

const Checkout: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { items, total } = useSelector((state: RootState) => state.cart);

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    address: '',
    city: '',
    postalCode: '',
    cardNumber: '',
    expiryDate: '',
    cvv: '',
    saveInfo: false,
  });

  const deliveryFee = 2.5;
  const finalTotal = total + deliveryFee;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'saveInfo' ? checked : value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically:
    // 1. Validate the form
    // 2. Process the payment
    // 3. Create an order in the backend
    // 4. Clear the cart
    dispatch(clearCart());
    navigate('/order-confirmation');
  };

  return (
    <Container sx={{ py: 8 }}>
      <Typography variant="h2" align="center" sx={{ mb: 6 }}>
        Checkout
      </Typography>

      <form onSubmit={handleSubmit}>
        <Box sx={{ display: 'flex', gap: 4, flexDirection: { xs: 'column', md: 'row' } }}>
          <Box sx={{ flex: 1 }}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Delivery Information
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <TextField
                    fullWidth
                    label="Full Name"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    required
                  />
                  <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                    <TextField
                      fullWidth
                      label="Email"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                    />
                    <TextField
                      fullWidth
                      label="Phone Number"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      required
                    />
                  </Box>
                  <TextField
                    fullWidth
                    label="Address"
                    name="address"
                    value={formData.address}
                    onChange={handleChange}
                    required
                  />
                  <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                    <TextField
                      fullWidth
                      label="City"
                      name="city"
                      value={formData.city}
                      onChange={handleChange}
                      required
                    />
                    <TextField
                      fullWidth
                      label="Postal Code"
                      name="postalCode"
                      value={formData.postalCode}
                      onChange={handleChange}
                      required
                    />
                  </Box>
                </Box>

                <Divider sx={{ my: 4 }} />

                <Typography variant="h6" gutterBottom>
                  Payment Information
                </Typography>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <TextField
                    fullWidth
                    label="Card Number"
                    name="cardNumber"
                    value={formData.cardNumber}
                    onChange={handleChange}
                    required
                  />
                  <Box sx={{ display: 'flex', gap: 2, flexDirection: { xs: 'column', sm: 'row' } }}>
                    <TextField
                      fullWidth
                      label="Expiry Date"
                      name="expiryDate"
                      placeholder="MM/YY"
                      value={formData.expiryDate}
                      onChange={handleChange}
                      required
                    />
                    <TextField
                      fullWidth
                      label="CVV"
                      name="cvv"
                      value={formData.cvv}
                      onChange={handleChange}
                      required
                    />
                  </Box>
                  <FormControlLabel
                    control={
                      <Checkbox
                        name="saveInfo"
                        checked={formData.saveInfo}
                        onChange={handleChange}
                      />
                    }
                    label="Save my information for next time"
                  />
                </Box>
              </CardContent>
            </Card>
          </Box>

          <Box sx={{ width: { xs: '100%', md: '400px' } }}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Order Summary
                </Typography>
                {items.map((item) => (
                  <Box key={item.id} sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                      <Typography>
                        {item.name} x {item.quantity}
                      </Typography>
                      <Typography>€{(item.price * item.quantity).toFixed(2)}</Typography>
                    </Box>
                  </Box>
                ))}
                <Divider sx={{ my: 2 }} />
                <Box sx={{ mb: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography>Subtotal</Typography>
                    <Typography>€{total.toFixed(2)}</Typography>
                  </Box>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                    <Typography>Delivery Fee</Typography>
                    <Typography>€{deliveryFee.toFixed(2)}</Typography>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography variant="h6">Total</Typography>
                    <Typography variant="h6">€{finalTotal.toFixed(2)}</Typography>
                  </Box>
                  <Button
                    type="submit"
                    variant="contained"
                    fullWidth
                    sx={{
                      backgroundColor: 'var(--accent)',
                      '&:hover': {
                        backgroundColor: 'var(--accent-dark)',
                      },
                    }}
                  >
                    Place Order
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Box>
        </Box>
      </form>
    </Container>
  );
};

export default Checkout; 