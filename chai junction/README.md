# Chai Junction

A full-stack chai ordering web app built for the TUM campus. Users browse the menu, add items to a cart, and pay with Stripe. Auth is JWT-based; the backend is a typed Express REST API backed by MongoDB.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, TypeScript, MUI v5, Redux Toolkit, React Router v6 |
| Backend | Node.js 18+, Express 4, TypeScript |
| Database | MongoDB + Mongoose |
| Auth | JWT with bcrypt-hashed passwords |
| Payments | Stripe Payment Intents |
| Image storage | Cloudinary |

## Project Structure

```
chai junction/
├── backend/
│   ├── src/
│   │   ├── controllers/   # auth, menu, orders, users
│   │   ├── middleware/    # JWT auth, error handler, request validation
│   │   ├── models/        # User, MenuItem, Order (Mongoose schemas)
│   │   └── routes/        # Express routers
│   └── .env.example       # copy to .env and fill in secrets
└── frontend/
    ├── src/
    │   ├── components/    # Navbar, HomePage
    │   ├── pages/         # Home, Menu, Cart, Checkout
    │   └── store/         # Redux slices (cart state)
    └── package.json
```

## Getting Started

### Prerequisites

- Node.js 18+
- MongoDB running locally, or a MongoDB Atlas URI
- Stripe test account

### Backend

```bash
cd backend
cp .env.example .env      # fill in your values
npm install
npm run dev               # http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm start                 # http://localhost:3000
```

## API Reference

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register` | — | Register a new user |
| POST | `/api/auth/login` | — | Login, returns JWT |
| POST | `/api/auth/logout` | — | Logout |
| GET | `/api/menu` | — | List all menu items |
| GET | `/api/menu/:id` | — | Get a single menu item |
| POST | `/api/orders` | Bearer JWT | Create order + Stripe payment intent |
| GET | `/api/orders` | Bearer JWT | List the current user's orders |
| GET | `/api/orders/:id` | Bearer JWT | Get a single order |
| PATCH | `/api/orders/:id/status` | Bearer JWT | Update order status |

## Architecture Notes

- **Password hashing** is handled entirely in the Mongoose `pre('save')` hook — controllers pass plaintext and the model takes care of it.
- **Stripe client** is lazily initialised on first use so the server starts cleanly without a key set (returns a `503` if called without one).
- **CORS** is locked to the `CLIENT_URL` environment variable in production.
- **Error handling** uses a single `AppError` class flowing through a centralised Express error middleware — controllers never call `res.status()` directly.
- **Request validation** uses `express-validator` with `validationResult()` and returns all field errors in one response.

## Environment Variables

See [`backend/.env.example`](backend/.env.example) for the full list with descriptions.

## License

MIT
