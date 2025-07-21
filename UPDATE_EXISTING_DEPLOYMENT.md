# 🔄 PostVelocity - Update Existing Heroku Deployment

## 🎯 **YOU ALREADY DEPLOYED - LET'S UPDATE IT!**

Since you already have a Heroku app deployed, here's how to update it with the fixed code:

---

## 🚀 **OPTION 1: Update via GitHub (Easiest)**

### If you connected GitHub to your Heroku app:

1. **Push the fixed code to GitHub:**
   ```bash
   git add .
   git commit -m "Fix: Replace emergentintegrations with direct Stripe integration"
   git push origin main
   ```

2. **Go to your Heroku app dashboard**
3. **Navigate to the "Deploy" tab**
4. **Scroll to "Manual deploy" section**
5. **Click "Deploy Branch"**

**That's it!** Your app will rebuild with the fixed code.

---

## 🚀 **OPTION 2: Update via Heroku CLI**

### If you have Heroku CLI installed:

```bash
# Navigate to your project directory
cd /path/to/postvelocity

# Add your existing Heroku app as a remote (replace YOUR_APP_NAME)
heroku git:remote -a YOUR_APP_NAME

# Push the updated code
git push heroku main
```

**Replace `YOUR_APP_NAME` with your actual Heroku app name.**

---

## 🚀 **OPTION 3: Force Update (If needed)**

### If you get conflicts or issues:

```bash
# Force push the changes (use with caution)
git push heroku main --force
```

---

## 🔧 **UPDATE YOUR ENVIRONMENT VARIABLES**

### Add the new Stripe variable to your existing app:

1. **Go to your Heroku app dashboard**
2. **Settings tab → Config Vars → Reveal Config Vars**
3. **Add this new variable:**
   ```
   Key: STRIPE_API_KEY
   Value: STRIPE_TEST_KEY_PLACEHOLDER
   ```
4. **Update existing variables if needed:**
   - Change `ANTHROPIC_API_KEY` to `CLAUDE_API_KEY` (if you have the old name)

---

## 📋 **QUICK UPDATE SCRIPT**

### Save this as `update_deployment.sh` and run it:

```bash
#!/bin/bash

echo "🔄 Updating PostVelocity Heroku deployment..."

# Get your app name
read -p "📝 Enter your Heroku app name: " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name is required"
    exit 1
fi

# Add Heroku remote if not exists
heroku git:remote -a $APP_NAME 2>/dev/null || echo "Remote already exists"

# Add the new Stripe environment variable
echo "🔑 Adding STRIPE_API_KEY..."
read -p "💳 Enter your Stripe API Key: " STRIPE_KEY
heroku config:set STRIPE_API_KEY="$STRIPE_KEY" -a $APP_NAME

# Push the updated code
echo "🚀 Deploying updated code..."
git add .
git commit -m "Fix: Direct Stripe integration - deployment ready" || true
git push heroku main

echo ""
echo "✅ Update complete!"
echo "🌐 Your app: https://$APP_NAME.herokuapp.com"
echo "📊 Check logs: heroku logs --tail -a $APP_NAME"
```

---

## 🔍 **VERIFY YOUR UPDATE WORKED**

### After updating, check these:

1. **Visit your Heroku app URL**
2. **Check the logs for any errors:**
   ```bash
   heroku logs --tail -a YOUR_APP_NAME
   ```
3. **Look for success messages:**
   - ✅ "Advanced Social Media Management Platform Started!"
   - ✅ No "ModuleNotFoundError" messages
   - ✅ No "emergentintegrations" errors

---

## 🆘 **IF YOU GET DEPLOYMENT ERRORS**

### Common issues when updating:

**1. If you see build errors:**
- Check that you pushed the latest fixed code
- Verify your `requirements.txt` doesn't have `emergentintegrations`
- Ensure `stripe==8.10.0` is in requirements.txt

**2. If the app won't start:**
- Check logs: `heroku logs --tail -a YOUR_APP_NAME`
- Verify environment variables are set correctly
- Make sure `STRIPE_API_KEY` is added

**3. If you get "No such app" error:**
- List your apps: `heroku apps`
- Use the exact app name from the list

---

## 🎯 **WHAT TO EXPECT AFTER UPDATE**

### Your deployment should now:
- ✅ **Start without import errors**
- ✅ **Use direct Stripe integration** 
- ✅ **Process payments correctly**
- ✅ **Handle all API calls properly**
- ✅ **Show improved error handling**

---

## 📞 **NEED YOUR APP NAME?**

### Find your existing Heroku app name:

```bash
# List all your Heroku apps
heroku apps

# Or check your current git remotes
git remote -v
```

The app name will be in the format: `https://YOUR_APP_NAME.herokuapp.com`

---

## 🎉 **UPDATE CHECKLIST**

After updating your deployment:

- [ ] Code pushed to GitHub/Heroku
- [ ] `STRIPE_API_KEY` environment variable added
- [ ] App builds successfully (check build logs)
- [ ] App starts without errors (check application logs)
- [ ] Homepage loads correctly
- [ ] Payment system works (if testing)
- [ ] No "emergentintegrations" errors in logs

---

## 🚀 **QUICK COMMANDS SUMMARY**

```bash
# If using GitHub integration:
git push origin main  # Then deploy via Heroku dashboard

# If using Heroku CLI:
heroku git:remote -a YOUR_APP_NAME
git push heroku main

# Check logs:
heroku logs --tail -a YOUR_APP_NAME

# View app:
heroku open -a YOUR_APP_NAME
```

---

**Your existing deployment can be easily updated with the fixed code! Choose the method that works best for you.** 🔄