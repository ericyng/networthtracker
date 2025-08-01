# PickupKids Mobile App

React Native mobile application for iOS and Android platforms.

## 🚀 Features

### Core Functionality
- **Dashboard:** Quick overview of today's schedules
- **Calendar View:** Monthly/weekly schedule management
- **Family Management:** Add/remove family members
- **Child Profiles:** Manage child information and preferences
- **Location Management:** Add and manage pickup/dropoff locations
- **Push Notifications:** Real-time reminders and updates
- **Offline Support:** Basic functionality without internet

### Mobile-Specific Features
- **Location Services:** GPS tracking for pickup coordination
- **Camera Integration:** Photo capture for child identification
- **Haptic Feedback:** Tactile responses for better UX
- **Background Sync:** Automatic data synchronization
- **Biometric Authentication:** Fingerprint/Face ID support
- **Deep Linking:** Direct navigation to specific schedules

## 🛠️ Tech Stack

- **Framework:** React Native with Expo
- **Navigation:** React Navigation v6
- **State Management:** React Query + Context API
- **UI Components:** React Native Elements + Paper
- **Calendar:** React Native Calendars
- **Maps:** React Native Maps
- **Notifications:** Expo Notifications + Firebase
- **Storage:** AsyncStorage + SecureStore
- **Forms:** React Hook Form

## 🚀 Getting Started

### Prerequisites
- Node.js 16+
- Expo CLI
- iOS Simulator (for iOS development)
- Android Studio (for Android development)
- Backend API running (see backend README)

### Installation

1. **Install Expo CLI:**
```bash
npm install -g @expo/cli
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start development server:**
```bash
npm start
```

5. **Run on device/simulator:**
```bash
# iOS
npm run ios

# Android
npm run android
```

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── common/         # Generic components
│   ├── forms/          # Form components
│   ├── calendar/       # Calendar components
│   └── maps/           # Map components
├── screens/            # Screen components
│   ├── auth/           # Authentication screens
│   ├── dashboard/      # Dashboard screens
│   ├── family/         # Family management
│   ├── schedule/       # Schedule management
│   └── settings/       # App settings
├── navigation/         # Navigation configuration
├── hooks/              # Custom React hooks
├── services/           # API services
├── utils/              # Utility functions
├── types/              # TypeScript type definitions
├── context/            # React context providers
├── assets/             # Images, fonts, etc.
└── constants/          # App constants
```

## 🔧 Configuration

### Environment Variables
```bash
# API Configuration
API_URL=http://localhost:8000/api
WS_URL=ws://localhost:8000/ws

# Maps Configuration
GOOGLE_MAPS_API_KEY=your-google-maps-api-key

# Firebase Configuration
FIREBASE_API_KEY=your-firebase-api-key
FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
FIREBASE_PROJECT_ID=your-project-id
FIREBASE_STORAGE_BUCKET=your-project.appspot.com
FIREBASE_MESSAGING_SENDER_ID=your-sender-id
FIREBASE_APP_ID=your-app-id

# App Configuration
APP_NAME=PickupKids
APP_VERSION=1.0.0
```

### Expo Configuration
```json
{
  "expo": {
    "name": "PickupKids",
    "slug": "pickupkids",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "updates": {
      "fallbackToCacheTimeout": 0
    },
    "assetBundlePatterns": [
      "**/*"
    ],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.pickupkids.app"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#FFFFFF"
      },
      "package": "com.pickupkids.app"
    },
    "web": {
      "favicon": "./assets/favicon.png"
    },
    "plugins": [
      "expo-notifications",
      "expo-location",
      "expo-camera"
    ]
  }
}
```

## 📱 Features

### Authentication
- Login/Register screens
- Biometric authentication
- Auto-login with secure storage
- Password reset functionality

### Dashboard
- Today's schedule overview
- Quick actions for common tasks
- Family member status
- Recent activity feed

### Calendar
- Monthly/weekly/daily views
- Tap-to-schedule functionality
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
- Push notifications
- In-app notification center
- Custom notification sounds
- Notification preferences

### Offline Support
- Basic schedule viewing
- Local data caching
- Sync when online
- Offline indicators

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

### iOS
```bash
# Build for iOS
expo build:ios

# Submit to App Store
expo upload:ios
```

### Android
```bash
# Build for Android
expo build:android

# Submit to Google Play
expo upload:android
```

## 🔒 Security

- Secure storage for sensitive data
- Biometric authentication
- Certificate pinning
- Input validation
- Secure API communication

## 🚀 Deployment

### Expo Application Services (EAS)
```bash
# Install EAS CLI
npm install -g @expo/eas-cli

# Configure EAS
eas build:configure

# Build for production
eas build --platform all

# Submit to stores
eas submit --platform all
```

### Manual Build
```bash
# Eject from Expo
expo eject

# Build manually with React Native CLI
npx react-native run-ios
npx react-native run-android
```

## 📝 Development

### Code Style
- **ESLint** for linting
- **Prettier** for formatting
- **TypeScript** for type safety

### Available Scripts
- `npm start` - Start Expo development server
- `npm run ios` - Run on iOS simulator
- `npm run android` - Run on Android emulator
- `npm test` - Run tests
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## 🔄 API Integration

The mobile app communicates with the Django REST API:

- **Authentication:** JWT tokens with secure storage
- **Real-time:** WebSocket connections
- **Data Fetching:** React Query for caching
- **Error Handling:** Centralized error management
- **Offline Support:** Local data persistence

## 📱 Platform-Specific Features

### iOS
- Face ID/Touch ID integration
- iOS-specific UI components
- Background app refresh
- iOS notification permissions

### Android
- Fingerprint authentication
- Android-specific UI components
- Background services
- Android notification channels

## 🔧 Troubleshooting

### Common Issues
- **Metro bundler issues:** Clear cache with `expo start -c`
- **iOS build issues:** Clean Xcode build folder
- **Android build issues:** Clean Gradle cache
- **Notification issues:** Check device permissions

### Debug Tools
- **React Native Debugger:** For debugging
- **Flipper:** For network inspection
- **Expo DevTools:** For development tools 