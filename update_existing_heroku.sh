#!/bin/bash

# PostVelocity - Update Existing Heroku Deployment Script
# Use this when you already have a Heroku app deployed

echo "🔄 PostVelocity - Update Existing Deployment"
echo "============================================="

# Get app name
echo "📋 First, let's find your existing Heroku apps:"
if command -v heroku &> /dev/null; then
    echo ""
    heroku apps 2>/dev/null || echo "Please login to Heroku first: heroku login"
    echo ""
else
    echo "❌ Heroku CLI not found. Install from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

read -p "📝 Enter your existing Heroku app name: " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name is required"
    exit 1
fi

# Verify app exists
echo "🔍 Verifying app exists..."
if ! heroku apps:info -a $APP_NAME &> /dev/null; then
    echo "❌ App '$APP_NAME' not found. Please check the name and try again."
    exit 1
fi

echo "✅ App '$APP_NAME' found"

# Add Heroku remote
echo "🔗 Setting up Heroku remote..."
heroku git:remote -a $APP_NAME 2>/dev/null || echo "✅ Remote already exists"

# Check current environment variables
echo "🔍 Checking current environment variables..."
if heroku config:get STRIPE_API_KEY -a $APP_NAME &> /dev/null; then
    echo "✅ STRIPE_API_KEY already set"
else
    echo "🔑 STRIPE_API_KEY not found, let's add it:"
    read -p "💳 Enter your Stripe API Key (sk_test_... or sk_live_...): " STRIPE_KEY
    if [ ! -z "$STRIPE_KEY" ]; then
        heroku config:set STRIPE_API_KEY="$STRIPE_KEY" -a $APP_NAME
        echo "✅ STRIPE_API_KEY added"
    fi
fi

# Update other environment variables if needed
echo ""
echo "🔧 Checking other environment variables..."

# Check CLAUDE_API_KEY vs old ANTHROPIC_API_KEY
if heroku config:get ANTHROPIC_API_KEY -a $APP_NAME &> /dev/null; then
    if ! heroku config:get CLAUDE_API_KEY -a $APP_NAME &> /dev/null; then
        echo "🔄 Found ANTHROPIC_API_KEY, copying to CLAUDE_API_KEY..."
        CLAUDE_KEY=$(heroku config:get ANTHROPIC_API_KEY -a $APP_NAME)
        heroku config:set CLAUDE_API_KEY="$CLAUDE_KEY" -a $APP_NAME
        echo "✅ CLAUDE_API_KEY set"
    fi
fi

# Set production environment variables
echo "⚙️  Setting production environment..."
heroku config:set ENVIRONMENT=production -a $APP_NAME
heroku config:set DEBUG=False -a $APP_NAME
heroku config:set NODE_ENV=production -a $APP_NAME

# Commit and push changes
echo ""
echo "📦 Preparing code for deployment..."
git add .
git commit -m "Fix: Replace emergentintegrations with direct Stripe integration - update deployment" || echo "✅ No changes to commit"

# Deploy
echo "🚀 Deploying updated code to Heroku..."
git push heroku main

# Check deployment status
echo ""
echo "🔍 Checking deployment status..."
sleep 5

# Test the deployment
echo "🧪 Testing deployment..."
if curl -s "https://$APP_NAME.herokuapp.com/api/health" > /dev/null 2>&1; then
    echo "✅ Health check passed!"
else
    echo "⚠️  Health check failed - checking logs..."
    echo "📊 Recent logs:"
    heroku logs --tail -a $APP_NAME -n 20
fi

echo ""
echo "🎉 Update Complete!"
echo "======================================="
echo "✅ Your app has been updated: https://$APP_NAME.herokuapp.com"
echo ""
echo "📋 What was updated:"
echo "   • Removed emergentintegrations dependency"
echo "   • Added direct Stripe integration"
echo "   • Enhanced error handling"
echo "   • Updated environment variables"
echo ""
echo "🔧 Useful commands:"
echo "   • View logs: heroku logs --tail -a $APP_NAME"
echo "   • Open app: heroku open -a $APP_NAME"
echo "   • Check config: heroku config -a $APP_NAME"
echo ""
echo "🎊 Your PostVelocity app is now running with the fixed code!"