# Social Authentication Setup Guide

## Overview
The NetWorth Tracker application now supports social authentication with Google and Facebook. The login page includes buttons for both providers.

## Setup Instructions

### 1. Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" and create an "OAuth 2.0 Client ID"
5. Set the authorized redirect URIs to:
   - `http://localhost:8000/accounts/google/login/callback/` (for development)
   - `https://yourdomain.com/accounts/google/login/callback/` (for production)
6. Note down your Client ID and Client Secret

### 2. Facebook OAuth Setup

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app or select an existing one
3. Add the "Facebook Login" product
4. Configure the OAuth redirect URIs:
   - `http://localhost:8000/accounts/facebook/login/callback/` (for development)
   - `https://yourdomain.com/accounts/facebook/login/callback/` (for production)
5. Note down your App ID and App Secret

### 3. Django Admin Configuration

1. Access your Django admin panel at `/admin/`
2. Go to "Social Applications" under "Social Accounts"
3. Add a new social application for Google:
   - Provider: Google
   - Name: Google
   - Client ID: Your Google Client ID
   - Secret Key: Your Google Client Secret
   - Sites: Add your site (usually localhost:8000 for development)

4. Add a new social application for Facebook:
   - Provider: Facebook
   - Name: Facebook
   - Client ID: Your Facebook App ID
   - Secret Key: Your Facebook App Secret
   - Sites: Add your site (usually localhost:8000 for development)

### 4. Environment Variables (Recommended)

For production, store your OAuth credentials as environment variables:

```bash
# Add to your .env file
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
```

Then update your settings.py to use these environment variables.

## Features

- **Google Sign-In**: Users can sign in with their Google account
- **Facebook Sign-In**: Users can sign in with their Facebook account
- **Automatic Account Creation**: New users are automatically created when they sign in via social providers
- **Profile Information**: Basic profile information (name, email) is automatically imported
- **Seamless Integration**: Social login integrates with the existing authentication system

## Security Notes

- Always use HTTPS in production
- Keep your OAuth secrets secure
- Regularly rotate your OAuth credentials
- Monitor your OAuth usage and set appropriate rate limits

## Troubleshooting

- Ensure your redirect URIs are exactly correct (including trailing slashes)
- Check that your OAuth apps are properly configured and approved
- Verify that the required APIs are enabled in your Google Cloud Console
- Make sure your Facebook app is in the correct mode (development/production) 