# Simple Ecommerce: Fullstack
**Stack:** Django + DRF + simplejwt · Vue 3 + Axios + Pinia · SQLite (dev)

---

## Overview

A simple ecommerce app: browse products, manage a cart, place orders.
No payments. Just the core fullstack loop.

**Features:**
- Register / login / logout (JWT)
- Browse products (public)
- Add to cart, remove items (auth required)
- Place an order (cart → order)
- View order history (auth required)

---

## Project Structure

```
ecommerce-project/
├── backend/
│   ├── ecommerce/       ← Django project folder (settings, urls, wsgi)
│   ├── accounts/        ← App: auth + registration
│   ├── products/        ← App: product listing
│   ├── orders/          ← App: cart + orders
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/            ← Vue 3 app
```

---

## Phase 1 — Django Setup

**Goal:** Get Django running with the right packages installed.

1. Create a virtual environment and activate it.
2. Install these packages: `django djangorestframework djangorestframework-simplejwt django-cors-headers psycopg2-binary pillow`
3. Freeze to `requirements.txt`.
4. Create a Django project called `ecommerce`.
5. Create three apps: `accounts`, `products`, `orders`.
6. In `settings.py`:
   - Add `rest_framework`, `corsheaders`, and your three apps to `INSTALLED_APPS`.
   - Add `corsheaders.middleware.CorsMiddleware` at the top of `MIDDLEWARE`.
   - Add a `REST_FRAMEWORK` config block setting `DEFAULT_AUTHENTICATION_CLASSES` to `JWTAuthentication` and `DEFAULT_PERMISSION_CLASSES` to `IsAuthenticatedOrReadOnly`.
   - Add `CORS_ALLOWED_ORIGINS` with `http://localhost:5173` (Vite's dev server port).
   - Add `MEDIA_URL` and `MEDIA_ROOT` for image uploads.

**Test Phase 1:**
- Run `python manage.py runserver` — should start without errors.
- Visit `http://localhost:8000/` — Django welcome page confirms it's working.

---

## Phase 2 — Models

**Goal:** Define the database structure.

### accounts
No custom model needed. Django's built-in `User` handles auth.

### products
Create a `Product` model with these fields:
- `name` — CharField
- `description` — TextField (optional)
- `price` — DecimalField
- `stock` — PositiveIntegerField
- `image` — ImageField (optional, upload to `products/`)
- `created_at` — DateTimeField (auto)

### orders
Create four models:

**Cart** — one per user (OneToOneField to User)

**CartItem** — one row per product in the cart
- FK to Cart, FK to Product
- `quantity` field
- Set `unique_together = ('cart', 'product')` so the same product can't appear twice

**Order** — a placed order
- FK to User
- `status` field with choices: pending / shipped / delivered
- `total` DecimalField
- `created_at` DateTimeField

**OrderItem** — snapshot of each product at time of purchase
- FK to Order
- `product_name` CharField (not a FK — see note below)
- `product_price` DecimalField (not a FK)
- `quantity` PositiveIntegerField

> **Why snapshot?** Store the name and price directly on OrderItem instead of a FK to Product. If the product price changes later or the product gets deleted, your order history stays accurate. This is a real-world pattern worth knowing.

Run `makemigrations` and `migrate` after.

**Test Phase 2:**
- Register `Product` in `products/admin.py` with `admin.site.register(Product)`.
- Run `createsuperuser`, go to `http://localhost:8000/admin`, and add 2–3 products manually.
- Confirm they appear in the admin list.

---

## Phase 3 — Serializers

**Goal:** Tell DRF how to convert your models to/from JSON.

> **What is a serializer?** It's like a schema. It defines which fields get included in the API response and handles validation on input. Read the DRF serializers docs before writing these.

### accounts
Write a `RegisterSerializer` using `ModelSerializer` on Django's `User` model. Include `username`, `email`, `password`. Mark `password` as `write_only=True`. Override `create()` to call `User.objects.create_user()` so the password gets hashed.

### products
Write a `ProductSerializer` using `ModelSerializer`. Include all fields.

### orders
Write four serializers:

- `CartItemSerializer` — include `id`, `product` (FK id), `quantity`. Add read-only source fields for `product_name` and `product_price` pulled from the related product.
- `CartSerializer` — include `id`, `created_at`, and a nested `items` (many=True, read_only).
- `OrderItemSerializer` — include `id`, `product_name`, `product_price`, `quantity`.
- `OrderSerializer` — include `id`, `status`, `total`, `created_at`, and nested `items`.

**Test Phase 3:**
No URL needed yet. Open `python manage.py shell` and test manually:
```python
from products.models import Product
from products.serializers import ProductSerializer
p = Product.objects.first()
print(ProductSerializer(p).data)
```
Should print a dict of the product's fields.

---

## Phase 4 — Views & URLs

**Goal:** Expose your data as API endpoints.

> **APIView vs ViewSet:** `APIView` gives you full control — you write `get()`, `post()`, `delete()` methods yourself. `ViewSet` is higher-level and handles CRUD automatically. Use `ReadOnlyModelViewSet` for products (list + retrieve only). Use `APIView` for cart logic since it needs custom behavior.

### accounts
- Write a `RegisterView` using `generics.CreateAPIView` with `AllowAny` permission.
- Wire up URLs: `register/`, `token/` (simplejwt's `TokenObtainPairView`), `token/refresh/`.

### products
- Write a `ProductViewSet` using `ReadOnlyModelViewSet`. Set permission to `AllowAny`.
- Register it with a `DefaultRouter` at prefix `products`.

### orders
Write these views using `APIView`, all requiring `IsAuthenticated`:

- **CartView (GET):** Get or create the user's cart, return it serialized.
- **CartView (POST):** Add a product to the cart. If the item already exists, increment quantity. Otherwise create it.
- **CartItemView (DELETE):** Delete a specific CartItem by id, scoped to the current user's cart.
- **PlaceOrderView (POST):** Calculate total from cart items, create an Order, create OrderItems as snapshots, clear cart items, return the order.
- **OrderListView (GET):** Return all orders for the current user using `generics.ListAPIView`.

Wire all URLs into the main `ecommerce/urls.py`. Include media file serving for dev.

**Test Phase 4 — use a REST client (Bruno, Insomnia, or Postman):**

1. `POST /api/auth/register/` with username/email/password → should return user data.
2. `POST /api/auth/token/` with username/password → should return `access` and `refresh` tokens. Copy the access token.
3. `GET /api/products/` → should return your seeded products (no auth needed).
4. Set `Authorization: Bearer <token>` header, then `GET /api/cart/` → should return an empty cart.
5. `POST /api/cart/` with `{ "product": 1, "quantity": 1 }` → cart should now have an item.
6. `POST /api/cart/checkout/` → should return a new order and clear the cart.
7. `GET /api/cart/orders/` → should list your order.

If any step fails, check the error message — DRF returns descriptive errors.

---

## Phase 5 — Vue 3 Frontend

**Goal:** Build a Vue app that talks to your API.

### Setup
Scaffold a new Vite + Vue project. Install `axios`, `vue-router`, and `pinia`.

### Folder structure to create
```
src/
├── api/axios.js         ← configured axios instance
├── stores/auth.js       ← pinia store: login, logout, token
├── stores/cart.js       ← pinia store: fetch, add, remove, checkout
├── router/index.js      ← routes + navigation guard
└── views/
    ├── LoginView.vue
    ├── RegisterView.vue
    ├── ProductsView.vue
    ├── CartView.vue
    └── OrdersView.vue
```

### Step-by-step

**1. axios.js**
Create an axios instance with `baseURL` pointing to your Django server. Add a request interceptor that reads the JWT from `localStorage` and attaches it as `Authorization: Bearer <token>` on every request.
> Look up: axios interceptors

**2. auth store (Pinia)**
State: `access` token (read from localStorage on init).
Actions: `login()` calls `/auth/token/`, saves token to state + localStorage. `logout()` clears both. `register()` calls `/auth/register/`.
Getter: `isLoggedIn` returns true if token exists.
> Look up: Pinia defineStore, actions, getters

**3. router**
Define routes for `/`, `/cart`, `/orders`, `/login`, `/register`. Mark cart and orders routes with `meta: { requiresAuth: true }`. Add a `beforeEach` navigation guard that redirects to `/login` if the route requires auth and the user isn't logged in.
> Look up: Vue Router navigation guards

**4. LoginView**
Two inputs (username, password), a button. On click, call `auth.login()`, redirect to `/` on success, show error message on failure.

**5. RegisterView**
Same pattern as login but calls `auth.register()`, then redirects to `/login`.

**6. ProductsView**
On `onMounted`, fetch `/api/products/` and store in a ref. Render each product with name, price, description, and an "Add to Cart" button that calls the cart store.

**7. CartView**
On `onMounted`, call `cart.fetchCart()`. Render each item with product name, price, quantity, and a remove button. Add a "Place Order" button that calls `cart.checkout()` and redirects to `/orders`.

**8. OrdersView**
On `onMounted`, fetch `/api/cart/orders/`. Render each order with id, status, total, and its items.

**9. App.vue**
Add a simple nav with links to Products, Cart, Orders. Show Login/Register when logged out, Logout button when logged in.

**10. main.js**
Register Pinia and Vue Router with the app before mounting.

**Test Phase 5:**

1. Run `npm run dev`. Open `http://localhost:5173`.
2. Go to `/register` — create an account. Should redirect to login.
3. Log in — should redirect to `/`.
4. Products page should list your seeded products.
5. Click "Add to Cart" — then go to `/cart` — item should appear.
6. Click "Place Order" — should redirect to `/orders` with the order listed.
7. Open browser devtools → Network tab. Watch the requests go out and confirm the `Authorization` header is on authenticated calls.
8. Try navigating to `/cart` while logged out — should redirect to `/login`.

---

## Phase 6 — API Reference

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/auth/register/` | No | Create account |
| POST | `/api/auth/token/` | No | Login, get JWT |
| POST | `/api/auth/token/refresh/` | No | Refresh access token |
| GET | `/api/products/` | No | List all products |
| GET | `/api/products/:id/` | No | Single product |
| GET | `/api/cart/` | Yes | View cart |
| POST | `/api/cart/` | Yes | Add item to cart |
| DELETE | `/api/cart/item/:id/` | Yes | Remove cart item |
| POST | `/api/cart/checkout/` | Yes | Place order |
| GET | `/api/cart/orders/` | Yes | Order history |

---

## Build Order

Follow this strictly. Don't jump ahead.

1. Django setup + settings
2. Models → migrate → seed via admin
3. Serializers → test in Django shell
4. Views + URLs → test with REST client
5. Vue setup + axios instance
6. Auth store + login/register views
7. Router with navigation guard
8. Products view
9. Cart store + cart view
10. Orders view + App.vue nav

---

## Key Concepts to Look Up

Look these up **when you hit them**, not all upfront.

- **DRF Serializers** — how Django converts models to JSON and validates input
- **DRF APIView vs ViewSet** — two styles of writing API views
- **JWT** — what access vs refresh tokens are and why there are two
- **Axios interceptors** — how to run code before every HTTP request
- **Pinia** — Vue's global state management
- **Vue Router navigation guards** — how to protect routes

---

## After MVP

- Add product stock validation (can't add to cart if stock is 0)
- Add quantity selector on cart (not just remove)
- Add search/filter on products page
- Deploy backend to Railway, frontend to Vercel
