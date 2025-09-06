# Project TODO List

## Phase 1: Backend Setup (Django)

- [x] Initialize Django project
- [x] Set up Django apps as per the documentation:
  - [x] `accounts`
  - [x] `kyc`
  - [x] `wallet`
  - [x] `payments`
  - [x] `games`
  - [x] `draws`
  - [x] `tickets`
  - [x] `payouts`
  - [x] `adminpanel`
  - [x] `audit`
  - [x] `notifications`
- [x] Configure database (SQLite for now)
- [x] Implement User model (accounts app)
- [x] Implement Wallet and LedgerEntry models (wallet app)
- [x] Implement GameConfig and OddsScheme models (games app)
- [x] Implement Draw model (draws app)
- [x] Implement Ticket model (tickets app)
- [x] Implement Payout model (payouts app)
- [x] Implement KycCheck model (kyc app)
- [x] Implement AuditLog model (audit app)
- [x] Set up Celery and Redis for background tasks.
- [x] Implement basic API endpoints using Django REST Framework.
- [x] Implement user registration and JWT authentication.
- [x] Implement basic deposit initiation (payments app).
- [x] Implement basic payment webhook (payments app).
- [x] Implement basic ticket placement logic.
- [x] Implement basic draw scheduling and execution.
- [x] Implement basic payout processing.
- [x] Implement basic KYC verification logic.
- [x] Implement basic API endpoints for games app.
- [x] Implement basic API endpoints for draws app.
- [x] Implement basic API endpoints for tickets app.
- [x] Implement basic API endpoints for payouts app.
- [x] Implement basic API endpoints for wallet app.
- [x] Implement basic adminpanel app.
- [x] Implement basic audit app.
- [x] Implement basic notifications app.
- [x] Implement permission handling for all apps.

## Phase 2: Frontend Setup (React)

- [x] Initialize React project with Vite and TypeScript.
- [x] Set up project structure with pages, components, features.
- [x] Install and configure Redux Toolkit and RTK Query.
- [x] Implement basic UI components (NumberGrid, StakeInput, etc.).
- [x] Implement pages (Home, Play, Results, Wallet, Tickets, Profile).
- [x] Connect frontend to backend APIs.

## Phase 3: Core Features Implementation

- [x] Implement payment integration (Paystack/Flutterflow).
- [x] Implement ticket placement logic.
- [x] Implement draw scheduling and execution.
- [x] Implement payout processing.

## Phase 4: Testing and Deployment

- [x] Write unit tests for backend and frontend.
- [x] Write integration tests.
- [x] Set up CI/CD pipeline (GitHub Actions).
- [x] Deploy to a staging environment.
- [x] Perform load testing.
- [x] Deploy to production.