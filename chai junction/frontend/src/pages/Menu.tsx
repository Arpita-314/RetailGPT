import React, { useState } from 'react';
import {
  Box,
  Typography,
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
  Tabs,
  Tab,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';

interface MenuItem {
  id: string;
  name: string;
  description: string;
  price: number;
  image: string;
  category: string;
}

const Menu: React.FC = () => {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState('all');

  // Mock data - replace with API call
  const menuItems: MenuItem[] = [
    {
      id: '1',
      name: 'Masala Chai',
      description: 'Traditional spiced tea with milk',
      price: 2.5,
      image: '/images/masala-chai.jpg',
      category: 'drinks',
    },
    {
      id: '2',
      name: 'Samosa',
      description: 'Crispy pastry filled with spiced potatoes',
      price: 3.0,
      image: '/images/samosa.jpg',
      category: 'snacks',
    },
    // Add more items...
  ];

  const categories = [
    { id: 'all', label: 'All' },
    { id: 'drinks', label: 'Drinks' },
    { id: 'snacks', label: 'Snacks' },
    { id: 'meals', label: 'Meals' },
  ];

  const filteredItems = selectedCategory === 'all'
    ? menuItems
    : menuItems.filter(item => item.category === selectedCategory);

  return (
    <Container sx={{ py: 8 }}>
      <Typography variant="h2" align="center" sx={{ mb: 6 }}>
        Our Menu
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 4 }}>
        <Tabs
          value={selectedCategory}
          onChange={(_, newValue) => setSelectedCategory(newValue)}
          variant="scrollable"
          scrollButtons="auto"
        >
          {categories.map((category) => (
            <Tab
              key={category.id}
              value={category.id}
              label={category.label}
            />
          ))}
        </Tabs>
      </Box>

      <Grid container spacing={4}>
        {filteredItems.map((item) => (
          <Grid item xs={12} sm={6} md={4} key={item.id}>
            <Card
              sx={{
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                transition: 'transform 0.2s',
                '&:hover': {
                  transform: 'scale(1.02)',
                },
              }}
            >
              <CardMedia
                component="img"
                height="200"
                image={item.image}
                alt={item.name}
              />
              <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h5" component="h2" gutterBottom>
                  {item.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {item.description}
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="h6" color="primary">
                    €{item.price.toFixed(2)}
                  </Typography>
                  <Button
                    variant="contained"
                    size="small"
                    onClick={() => navigate(`/menu/${item.id}`)}
                    sx={{
                      backgroundColor: 'var(--accent)',
                      '&:hover': {
                        backgroundColor: 'var(--accent-dark)',
                      },
                    }}
                  >
                    Add to Cart
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Menu; 