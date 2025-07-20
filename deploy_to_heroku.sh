#!/bin/bash

# PostVelocity Heroku Deployment Script
# Run this script to deploy PostVelocity to Heroku

echo "🚀 PostVelocity Heroku Deployment Script"
echo "========================================"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found!"
    echo "📥 Please install it from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

echo "✅ Heroku CLI found"

# Check if user is logged in
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku first:"
    heroku login
fi

echo "✅ Heroku login confirmed"

# Get app name
echo ""
read -p "📝 Enter your app name (e.g., postvelocity-prod): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name is required"
    exit 1
fi

# Create the app
echo "🏗️  Creating Heroku app: $APP_NAME"
heroku create $APP_NAME

# Add buildpacks
echo "🔧 Adding buildpacks..."
heroku buildpacks:add heroku/nodejs -a $APP_NAME
heroku buildpacks:add heroku/python -a $APP_NAME

# Get API keys
echo ""
echo "🔑 Please provide your API keys:"
read -p "📋 Claude API Key (sk-ant-api03-...): " CLAUDE_KEY
read -p "💳 Stripe API Key (sk_test_... or sk_live_...): " STRIPE_KEY
read -p "🗄️  MongoDB URL (mongodb+srv://...): " MONGO_URL

# Set environment variables
echo "⚙️  Setting environment variables..."
heroku config:set CLAUDE_API_KEY="$CLAUDE_KEY" -a $APP_NAME
heroku config:set STRIPE_API_KEY="$STRIPE_KEY" -a $APP_NAME
heroku config:set MONGO_URL="$MONGO_URL" -a $APP_NAME
heroku config:set ENVIRONMENT=production -a $APP_NAME
heroku config:set DEBUG=False -a $APP_NAME
heroku config:set NODE_ENV=production -a $APP_NAME
heroku config:set REACT_APP_ENVIRONMENT=production -a $APP_NAME

# Deploy
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku: PostVelocity ready" || true
heroku git:remote -a $APP_NAME
git push heroku main

echo ""
echo "🎉 Deployment Complete!"
echo "✅ Your app is live at: https://$APP_NAME.herokuapp.com"
echo ""
echo "🧪 Testing your deployment..."
curl -s "https://$APP_NAME.herokuapp.com/api/health" > /dev/null
if [ $? -eq 0 ]; then
    echo "✅ Health check passed!"
else
    echo "⚠️  Health check failed - check logs: heroku logs --tail -a $APP_NAME"
fi

echo ""
echo "📋 Next Steps:"
echo "1. Visit: https://$APP_NAME.herokuapp.com"
echo "2. Test all functionality"
echo "3. Set up custom domain if needed"
echo "4. Check logs: heroku logs --tail -a $APP_NAME"
echo ""
echo "🎊 PostVelocity is now live!"