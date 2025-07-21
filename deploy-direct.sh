#!/bin/bash
echo "🚀 PostVelocity Heroku Direct Deployment"
echo "========================================"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   Visit: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Login check
echo "🔐 Checking Heroku login..."
if ! heroku auth:whoami &> /dev/null; then
    echo "📝 Please login to Heroku first:"
    heroku login
fi

# Set app name
APP_NAME="postvelocity-live-1a79e85352b7"

echo "📦 Setting up Heroku git remote..."
heroku git:remote -a $APP_NAME

echo "🔧 Setting buildpacks..."
heroku buildpacks:clear -a $APP_NAME
heroku buildpacks:add heroku/nodejs -a $APP_NAME
heroku buildpacks:add heroku/python -a $APP_NAME

echo "🚀 Deploying to Heroku..."
git push heroku main --force

echo "✅ Deployment complete!"
echo "🌐 Your app: https://$APP_NAME.herokuapp.com/"
echo "📊 View logs: heroku logs --tail -a $APP_NAME"