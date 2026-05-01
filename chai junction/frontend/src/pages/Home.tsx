import React from 'react';
import { Box, Typography, Button, Container, Grid } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          backgroundColor: 'primary.main',
          height: '80vh',
          display: 'flex',
          alignItems: 'center',
          position: 'relative',
        }}
      >
        <Container>
          <Box sx={{ position: 'relative', zIndex: 1, color: 'white' }}>
            <Typography variant="h1" sx={{ mb: 2, fontWeight: 'bold' }}>
              Welcome to Chai Junction
            </Typography>
            <Typography variant="h5" sx={{ mb: 4 }}>
              Authentic Indian Chai & Snacks at TUM
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/menu')}
              sx={{
                backgroundColor: 'var(--accent)',
                '&:hover': {
                  backgroundColor: 'var(--accent-dark)',
                },
              }}
            >
              View Our Menu
            </Button>
          </Box>
        </Container>
      </Box>

      {/* Featured Items */}
      <Container sx={{ py: 8 }}>
        <Typography variant="h2" align="center" sx={{ mb: 6 }}>
          Our Specialties
        </Typography>
        <Grid container spacing={4}>
          {[
            {
              title: 'Masala Chai',
              description: 'Traditional spiced tea with milk',
              price: '€2.50',
            },
            {
              title: 'Samosa',
              description: 'Crispy pastry filled with spiced potatoes',
              price: '€3.00',
            },
            {
              title: 'Vada Pav',
              description: 'Spicy potato fritter in a bun',
              price: '€4.00',
            },
          ].map((item) => (
            <Grid item xs={12} md={4} key={item.title}>
              <Box
                sx={{
                  p: 3,
                  textAlign: 'center',
                  border: '1px solid #ddd',
                  borderRadius: 2,
                  height: '100%',
                }}
              >
                <Typography variant="h5" sx={{ mb: 2 }}>
                  {item.title}
                </Typography>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  {item.description}
                </Typography>
                <Typography variant="h6" color="primary">
                  {item.price}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default Home; 