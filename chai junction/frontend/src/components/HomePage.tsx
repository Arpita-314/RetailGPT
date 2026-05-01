import React from 'react';
import { Box, Typography, Button, Container, CardMedia } from '@mui/material';

const HomePage: React.FC = () => {
  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("/images/hero-bg.jpg")',
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          height: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          textAlign: 'center',
          color: 'white',
          padding: '0 1rem',
          marginTop: '4rem',
        }}
      >
        <Typography variant="h1" sx={{ fontSize: '4rem', marginBottom: '1rem', textShadow: '2px 2px 4px rgba(0,0,0,0.5)' }}>
          A Taste of Authentic India
        </Typography>
        <Typography variant="h5" sx={{ maxWidth: '800px', margin: '0 auto 2rem' }}>
          Experience the rich flavors of traditional Indian chai and street food
        </Typography>
        <Button
          variant="contained"
          href="#menu"
          sx={{
            backgroundColor: 'var(--accent)',
            color: 'white',
            padding: '0.8rem 2rem',
            borderRadius: '50px',
            textTransform: 'uppercase',
            letterSpacing: '1px',
            boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
            '&:hover': {
              backgroundColor: 'var(--primary)',
              transform: 'translateY(-3px)',
              boxShadow: '0 6px 12px rgba(0,0,0,0.3)',
            },
          }}
        >
          Explore Our Menu
        </Button>
      </Box>

      {/* About Section */}
      <Container sx={{ py: 8 }}>
        <Typography variant="h2" align="center" sx={{ mb: 6, color: 'var(--primary)' }}>
          Our Story
        </Typography>
        <Box sx={{ display: 'flex', gap: 4, flexDirection: { xs: 'column', md: 'row' }, alignItems: 'center' }}>
          <Box sx={{ flex: 1 }}>
            <CardMedia
              component="img"
              image="/images/about-chai.jpg"
              alt="Authentic Indian Chai"
              sx={{ borderRadius: '10px', boxShadow: '0 8px 16px rgba(0,0,0,0.1)' }}
            />
          </Box>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h3" sx={{ color: 'var(--primary)', mb: 2 }}>
              Bringing India's Chai Culture to TUM
            </Typography>
            <Typography paragraph>
              Chai Junction was born from a simple desire: to introduce the rich, aromatic experience of authentic Indian chai to the vibrant community at Technical University of Munich.
            </Typography>
            <Typography paragraph>
              Our recipes are passed down through generations, bringing you the genuine taste of Indian street corners where chai is more than just a beverage—it's a way of life.
            </Typography>
            <Box sx={{ mt: 4 }}>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <span style={{ color: 'var(--accent)', marginRight: '1rem' }}>✦</span>
                Authentic Recipes - Using traditional spice blends imported from India
              </Typography>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <span style={{ color: 'var(--accent)', marginRight: '1rem' }}>✦</span>
                Freshly Prepared - Each cup of chai is brewed to order
              </Typography>
              <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center' }}>
                <span style={{ color: 'var(--accent)', marginRight: '1rem' }}>✦</span>
                Perfect Pairings - Complementary snacks that enhance your chai experience
              </Typography>
            </Box>
          </Box>
        </Box>
      </Container>

      {/* Featured Items Section */}
      <Box sx={{ backgroundColor: 'white', py: 8 }}>
        <Container>
          <Typography variant="h2" align="center" sx={{ mb: 6, color: 'var(--primary)' }}>
            Our Specialties
          </Typography>
          <Box sx={{ display: 'flex', gap: 4, flexDirection: { xs: 'column', md: 'row' } }}>
            <Box sx={{ flex: 1, textAlign: 'center' }}>
              <CardMedia
                component="img"
                image="/images/masala-chai.jpg"
                alt="Masala Chai"
                sx={{ 
                  borderRadius: '10px', 
                  boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
                  mb: 2,
                  height: '300px',
                  objectFit: 'cover'
                }}
              />
              <Typography variant="h4" sx={{ color: 'var(--primary)', mb: 1 }}>
                Masala Chai
              </Typography>
              <Typography>
                Our signature blend of spices with premium tea leaves
              </Typography>
            </Box>
            <Box sx={{ flex: 1, textAlign: 'center' }}>
              <CardMedia
                component="img"
                image="/images/samosa.jpg"
                alt="Samosa"
                sx={{ 
                  borderRadius: '10px', 
                  boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
                  mb: 2,
                  height: '300px',
                  objectFit: 'cover'
                }}
              />
              <Typography variant="h4" sx={{ color: 'var(--primary)', mb: 1 }}>
                Samosa
              </Typography>
              <Typography>
                Crispy pastry filled with spiced potatoes and peas
              </Typography>
            </Box>
            <Box sx={{ flex: 1, textAlign: 'center' }}>
              <CardMedia
                component="img"
                image="/images/vada-pav.jpg"
                alt="Vada Pav"
                sx={{ 
                  borderRadius: '10px', 
                  boxShadow: '0 8px 16px rgba(0,0,0,0.1)',
                  mb: 2,
                  height: '300px',
                  objectFit: 'cover'
                }}
              />
              <Typography variant="h4" sx={{ color: 'var(--primary)', mb: 1 }}>
                Vada Pav
              </Typography>
              <Typography>
                Mumbai's favorite street food - spicy potato fritter in a bun
              </Typography>
            </Box>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};

export default HomePage; 