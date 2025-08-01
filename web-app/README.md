# PickupKids Web Application

React.js web application for the PickupKids coordination platform.

## 🚀 Features

### Core Functionality
- **Dashboard:** Overview of all pickup/dropoff schedules
- **Calendar View:** Visual schedule management
- **Family Management:** Add/remove family members
- **Child Profiles:** Manage child information
- **Location Management:** Add and manage pickup/dropoff locations
- **Real-time Updates:** Live schedule changes and notifications
- **Push Notifications:** Browser notifications for reminders

### User Interface
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Modern UI:** Clean, intuitive interface
- **Dark/Light Mode:** User preference support
- **Accessibility:** WCAG compliant design

## 🛠️ Tech Stack

- **Framework:** React 18 with TypeScript
- **Styling:** Tailwind CSS
- **State Management:** React Query + Context API
- **Routing:** React Router v6
- **Forms:** React Hook Form
- **Calendar:** React Big Calendar
- **Maps:** Mapbox GL
- **Real-time:** Socket.io Client
- **Notifications:** Web Push API

## 🚀 Getting Started

### Prerequisites
- Node.js 16+
- npm or yarn
- Backend API running (see backend README)

### Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Set up environment variables:**
```bash
cp .env.example .env.local
# Edit .env.local with your configuration
```

3. **Start development server:**
```bash
npm start
```

4. **Open in browser:**
```
http://localhost:3000
```

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── common/         # Generic components
│   ├── forms/          # Form components
│   ├── layout/         # Layout components
│   └── calendar/       # Calendar components
├── pages/              # Page components
│   ├── auth/           # Authentication pages
│   ├── dashboard/      # Dashboard pages
│   ├── family/         # Family management
│   └── schedule/       # Schedule management
├── hooks/              # Custom React hooks
├── services/           # API services
├── utils/              # Utility functions
├── types/              # TypeScript type definitions
├── context/            # React context providers
└── styles/             # Global styles
```

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000/ws

# Map Configuration
REACT_APP_MAPBOX_TOKEN=your-mapbox-token

# Firebase (Push Notifications)
REACT_APP_FIREBASE_API_KEY=your-firebase-api-key
REACT_APP_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
REACT_APP_FIREBASE_PROJECT_ID=your-project-id
REACT_APP_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
REACT_APP_FIREBASE_APP_ID=your-app-id
```

## 🧪 Testing

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with coverage
npm test -- --coverage
```

## 🏗️ Building for Production

```bash
# Build for production
npm run build

# Preview production build
npm run serve
```

## 📱 Features

### Authentication
- Login/Register forms
- JWT token management
- Protected routes
- Auto-logout on token expiry

### Dashboard
- Overview of today's schedules
- Quick actions for common tasks
- Recent activity feed
- Family member status

### Calendar
- Monthly/weekly/daily views
- Drag-and-drop scheduling
- Recurring schedule support
- Conflict detection

### Family Management
- Add/remove family members
- Child profile management
- Permission management
- Invitation system

### Location Management
- Interactive map integration
- Address autocomplete
- Location favorites
- Route optimization

### Notifications
- Browser push notifications
- In-app notification center
- Email notifications
- SMS integration (optional)

## 🔒 Security

- JWT token authentication
- Secure API communication
- Input validation
- XSS protection
- CSRF protection

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel
```

### Deploy to Netlify
```bash
npm run build
# Upload dist/ folder to Netlify
```

## 📝 Development

### Code Style
- **ESLint** for linting
- **Prettier** for formatting
- **TypeScript** for type safety

### Available Scripts
- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm run lint` - Run ESLint
- `npm run format` - Format code with Prettier

## 🔄 API Integration

The web app communicates with the Django REST API:

- **Authentication:** JWT tokens
- **Real-time:** WebSocket connections
- **Data Fetching:** React Query for caching
- **Error Handling:** Centralized error management

## 📱 Mobile Responsiveness

- **Mobile-first design**
- **Touch-friendly interface**
- **Progressive Web App (PWA) support**
- **Offline functionality** 