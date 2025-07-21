# PostVelocity - AI-Powered Social Media Management Platform

## Quick Setup for Heroku Deployment

### Required API Keys
You need to get these API keys and add them to Heroku (NOT in the code):

1. **Claude API Key**: Get from https://console.anthropic.com
2. **MongoDB URL**: Get from https://mongodb.com/atlas  
3. **Stripe API Key**: Get from https://stripe.com/dashboard
4. **Music API Key**: Provided by your service
5. **AITurbo API Key**: Provided by your service

### Heroku Setup Steps
1. Create Heroku app
2. Connect to this GitHub repository
3. Add API keys in Heroku Settings → Config Vars
4. Deploy from GitHub

### Environment Variables for Heroku
Add these in Heroku Settings → Config Vars:
- `CLAUDE_API_KEY` = your-claude-key
- `MONGO_URL` = your-mongodb-connection-string
- `STRIPE_API_KEY` = your-stripe-key
- `MUSIC_API_KEY` = your-music-key
- `AITURBO_API_KEY` = your-aiturbo-key
- `SECRET_KEY` = your-secret-key

## Features
- AI-powered content generation
- Multi-platform social media management
- Analytics and ROI tracking
- Payment system with Stripe
- OAuth integration for 20 platforms