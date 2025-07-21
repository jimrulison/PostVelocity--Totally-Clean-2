# PostVelocity Quick Setup Guide ⚡

## **15-Minute Production Setup**

This is the condensed version for experienced developers who want to get PostVelocity running quickly.

---

## **🚀 Quick Start Commands**

### **Step 1: System Setup (3 minutes)**
```bash
# Update system and install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git nginx certbot python3-certbot-nginx nodejs npm python3.9 python3.9-venv python3-pip

# Install PM2
sudo npm install -g pm2

# Create user and directories
sudo useradd -m -s /bin/bash postvelocity
sudo mkdir -p /home/postvelocity/postvelocity/{backend,frontend,logs}
sudo chown -R postvelocity:postvelocity /home/postvelocity/postvelocity
```

### **Step 2: Backend Setup (5 minutes)**
```bash
# Switch to app user
sudo su - postvelocity
cd /home/postvelocity/postvelocity/backend

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn motor pydantic anthropic aiofiles python-multipart python-jose[cryptography] passlib[bcrypt] python-dotenv Pillow beautifulsoup4 textstat nltk pymongo dnspython

# Create server.py (copy from your development environment)
# Create security.py (copy from your development environment)

# Create .env file
cat > .env << 'EOF'
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/postvelocity
CLAUDE_API_KEY=your_anthropic_api_key
SECRET_KEY=your_secret_key_32_characters_minimum
CORS_ORIGINS=https://yourdomain.com
ENVIRONMENT=production
EOF

# Test backend
python server.py &
curl http://localhost:8001/api/health
```

### **Step 3: Frontend Setup (4 minutes)**
```bash
# Setup frontend
cd /home/postvelocity/postvelocity/frontend

# Create package.json and install dependencies
npm init -y
npm install react react-dom react-scripts @tailwindcss/forms autoprefixer postcss tailwindcss

# Create directory structure
mkdir -p src public

# Create React files (copy from your development environment)
# - public/index.html
# - src/index.js
# - src/App.js
# - src/App.css
# - src/index.css

# Create .env file
cat > .env << 'EOF'
REACT_APP_BACKEND_URL=https://yourdomain.com
REACT_APP_ENVIRONMENT=production
GENERATE_SOURCEMAP=false
EOF

# Build frontend
npm run build
```

### **Step 4: Web Server Setup (2 minutes)**
```bash
# Create Nginx config
sudo tee /etc/nginx/sites-available/postvelocity << 'EOF'
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    location / {
        root /home/postvelocity/postvelocity/frontend/build;
        index index.html;
        try_files $uri $uri/ /index.html;
    }
    
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/postvelocity /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Get SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### **Step 5: Process Management (1 minute)**
```bash
# Create PM2 config
cat > /home/postvelocity/postvelocity/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'postvelocity-backend',
    script: '/home/postvelocity/postvelocity/backend/server.py',
    interpreter: '/home/postvelocity/postvelocity/backend/venv/bin/python',
    cwd: '/home/postvelocity/postvelocity/backend',
    instances: 2,
    exec_mode: 'cluster',
    env: { NODE_ENV: 'production', PORT: 8001 }
  }]
};
EOF

# Start services
pm2 start ecosystem.config.js
pm2 save
pm2 startup
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## **🔧 Essential Configuration Files**

### **Backend .env**
```bash
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/postvelocity
CLAUDE_API_KEY=YOUR_CLAUDE_API_KEY_HERE
SECRET_KEY=your-super-secret-key-32-characters-minimum
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
ENVIRONMENT=production
DEBUG=False
```

### **Frontend .env**
```bash
REACT_APP_BACKEND_URL=https://yourdomain.com
REACT_APP_ENVIRONMENT=production
GENERATE_SOURCEMAP=false
```

### **MongoDB Atlas Setup**
1. Create account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create cluster (free tier available)
3. Add IP address to whitelist (0.0.0.0/0 for all IPs)
4. Create database user
5. Get connection string

### **API Keys Required**
1. **Anthropic Claude API**: Get from [console.anthropic.com](https://console.anthropic.com)
2. **MongoDB Atlas**: Connection string from cluster
3. **Domain SSL**: Free with Let's Encrypt

---

## **✅ Quick Verification**

```bash
# Check all services
sudo systemctl status nginx
pm2 status
curl https://yourdomain.com/health
curl https://yourdomain.com/api/health

# Check logs if issues
pm2 logs postvelocity-backend
sudo tail -f /var/log/nginx/error.log
```

---

## **🚨 Common Quick Fixes**

### **Backend Not Starting**
```bash
cd /home/postvelocity/postvelocity/backend
source venv/bin/activate
python server.py
# Check error messages
```

### **Frontend Not Loading**
```bash
cd /home/postvelocity/postvelocity/frontend
npm run build
sudo systemctl restart nginx
```

### **Database Connection Failed**
```bash
# Check MongoDB Atlas IP whitelist
# Verify connection string in .env
# Test connection:
python3 -c "
import motor.motor_asyncio
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_URL'))
async def test(): 
    await client.admin.command('ping')
    print('Connected!')
asyncio.run(test())
"
```

---

## **🎯 Production Essentials**

### **Security Basics**
```bash
# Firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# SSL Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### **Basic Monitoring**
```bash
# Create simple health check
cat > /home/postvelocity/postvelocity/health-check.sh << 'EOF'
#!/bin/bash
curl -f https://yourdomain.com/api/health || pm2 restart postvelocity-backend
EOF
chmod +x /home/postvelocity/postvelocity/health-check.sh

# Schedule every 5 minutes
crontab -e
# Add: */5 * * * * /home/postvelocity/postvelocity/health-check.sh
```

---

## **🚀 You're Live!**

Your PostVelocity platform should now be running at `https://yourdomain.com` with:

- ✅ AI-powered content generation
- ✅ Multi-platform social media management  
- ✅ Beta feedback system
- ✅ SEO monitoring add-on
- ✅ Payment and trial system
- ✅ Secure HTTPS connections
- ✅ Automatic SSL renewal
- ✅ Process management with PM2
- ✅ Basic monitoring and restart

**Next Steps:**
1. Test all features thoroughly
2. Set up proper monitoring (see full deployment guide)
3. Configure backups
4. Add your API keys
5. Invite beta testers

**For advanced configuration, monitoring, and troubleshooting, refer to the complete PostVelocity Production Deployment Guide.**

---

## **📞 Quick Support**

**Common URLs to test:**
- Main site: `https://yourdomain.com`
- API health: `https://yourdomain.com/api/health`
- Backend direct: `http://localhost:8001/api/health`

**Common commands:**
- Restart backend: `pm2 restart postvelocity-backend`
- Restart web server: `sudo systemctl restart nginx`
- Check logs: `pm2 logs postvelocity-backend`
- Check SSL: `sudo certbot certificates`

**That's it! Your PostVelocity platform is now live and ready for users! 🎉**