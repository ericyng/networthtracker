# Social Authentication Setup Guide

This guide will help you set up Google, Facebook, and Apple OAuth authentication for your NetWorth Tracker application.

## Prerequisites

- Django project with django-allauth installed
- Admin access to configure providers
- Developer accounts for each platform

## 1. Google OAuth Setup

### Step 1: Create Google OAuth Application
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Configure the OAuth consent screen
6. Set application type to "Web application"
7. Add authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/` (development)
   - `https://yourdomain.com/accounts/google/login/callback/` (production)
8. Note down the Client ID and Client Secret

### Step 2: Configure in Django Admin
1. Go to Django Admin → Sites → Add site
   - Domain name: `localhost:8000` (development) or your domain
   - Display name: `NetWorth Tracker`
2. Go to Django Admin → Social Applications → Add social application
   - Provider: `Google`
   - Name: `Google OAuth`
   - Client ID: Your Google Client ID
   - Secret key: Your Google Client Secret
   - Sites: Select your site

## 2. Facebook OAuth Setup

### Step 1: Create Facebook App
1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app (Consumer type)
3. Add Facebook Login product
4. Configure Facebook Login settings:
   - Valid OAuth Redirect URIs:
     - `http://localhost:8000/accounts/facebook/login/callback/` (development)
     - `https://yourdomain.com/accounts/facebook/login/callback/` (production)
5. Note down the App ID and App Secret

### Step 2: Configure in Django Admin
1. Go to Django Admin → Social Applications → Add social application
   - Provider: `Facebook`
   - Name: `Facebook OAuth`
   - Client ID: Your Facebook App ID
   - Secret key: Your Facebook App Secret
   - Sites: Select your site

## 3. Apple OAuth Setup

### Step 1: Create Apple App
1. Go to [Apple Developer](https://developer.apple.com/)
2. Create a new App ID
3. Enable "Sign In with Apple" capability
4. Create a Services ID for web authentication
5. Configure the Services ID:
   - Domain: `localhost` (development) or your domain
   - Return URLs:
     - `http://localhost:8000/accounts/apple/login/callback/` (development)
     - `https://yourdomain.com/accounts/apple/login/callback/` (production)
6. Create a private key for the Services ID
7. Note down the Services ID, Team ID, and Key ID

### Step 2: Configure in Django Admin
1. Go to Django Admin → Social Applications → Add social application
   - Provider: `Apple`
   - Name: `Apple OAuth`
   - Client ID: Your Apple Services ID
   - Secret key: Your Apple private key (PEM format)
   - Key: Your Apple Key ID
   - Sites: Select your site

## 4. Environment Variables (Recommended)

For production, store sensitive credentials in environment variables:

```bash
# .env file
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
FACEBOOK_APP_ID=your_facebook_app_id
FACEBOOK_APP_SECRET=your_facebook_app_secret
APPLE_CLIENT_ID=your_apple_services_id
APPLE_CLIENT_SECRET=your_apple_private_key
APPLE_KEY_ID=your_apple_key_id
```

Then update your settings.py to use these variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': os.getenv('GOOGLE_CLIENT_ID'),
            'secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        }
    },
    'facebook': {
        'APP': {
            'client_id': os.getenv('FACEBOOK_APP_ID'),
            'secret': os.getenv('FACEBOOK_APP_SECRET'),
        }
    },
    'apple': {
        'APP': {
            'client_id': os.getenv('APPLE_CLIENT_ID'),
            'secret': os.getenv('APPLE_CLIENT_SECRET'),
            'key': os.getenv('APPLE_KEY_ID'),
        }
    }
}
```

## 5. Testing

1. Start your Django development server
2. Go to `/accounts/login/`
3. You should see the social login buttons
4. Test each provider by clicking the buttons
5. Verify that users can sign in and are redirected properly

## 6. Troubleshooting

### Common Issues:

1. **"Social login not configured" message**
   - Check that providers are added in Django Admin
   - Verify sites are configured correctly

2. **Redirect URI mismatch errors**
   - Ensure redirect URIs match exactly (including trailing slashes)
   - Check for typos in domain names

3. **"Invalid client" errors**
   - Verify Client ID and Secret are correct
   - Check that the app is properly configured on the provider's platform

4. **Apple Sign In issues**
   - Ensure the private key is in PEM format
   - Verify the Services ID is configured for web authentication
   - Check that the domain matches your configuration

### Debug Mode:
Enable debug mode in your Django settings to see detailed error messages:

```python
DEBUG = True
```

## 7. Production Considerations

1. **HTTPS Required**: All OAuth providers require HTTPS in production
2. **Domain Verification**: Some providers require domain verification
3. **Rate Limits**: Be aware of API rate limits
4. **Security**: Store secrets securely and never commit them to version control
5. **Monitoring**: Set up logging to monitor authentication failures

## 8. Additional Resources

- [Django Allauth Documentation](https://django-allauth.readthedocs.io/)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Facebook Login Documentation](https://developers.facebook.com/docs/facebook-login/)
- [Apple Sign In Documentation](https://developer.apple.com/documentation/sign_in_with_apple)

## Support

If you encounter issues:
1. Check the provider's developer console for error messages
2. Review Django logs for detailed error information
3. Verify all configuration steps were completed correctly
4. Test with a fresh browser session (clear cookies/cache) 