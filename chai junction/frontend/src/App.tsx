import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';
import Home from './pages/Home.tsx';
import Menu from './pages/Menu.tsx';
import Cart from './pages/Cart.tsx';
import Checkout from './pages/Checkout.tsx';

const theme = createTheme({
  palette: {
    primary: {
      main: '#D35400', // Chai Junction orange
    },
    secondary: {
      main: '#8E44AD', // Chai Junction purple
    },
    background: {
      default: '#FCF5E9', // Light cream background
    },
  },
  typography: {
    fontFamily: '"Segoe UI", Tahoma, Geneva, Verdana, sans-serif',
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        ':root': {
          '--accent': '#F39C12',
          '--accent-dark': '#E67E22',
        },
      },
    },
  },
});

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/menu" element={<Menu />} />
            <Route path="/cart" element={<Cart />} />
            <Route path="/checkout" element={<Checkout />} />
          </Routes>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App; 