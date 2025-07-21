# PostVelocity Production Deployment Guide 🚀

## **Complete Setup Instructions for Website Deployment**

This comprehensive guide will walk you through setting up PostVelocity on your production website, ensuring all components work perfectly together.

**🎯 What You'll Achieve:**
- Fully functional PostVelocity platform on your domain
- All API endpoints working correctly
- Secure HTTPS connections
- Database properly configured
- All features operational (Beta Feedback, SEO Monitoring, Payment System)

---

## **📋 Prerequisites & Requirements**

### **Server Requirements**
- **VPS/Dedicated Server** with root access
- **Operating System**: Ubuntu 20.04 LTS or later (recommended)
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: Minimum 20GB SSD
- **CPU**: 2 cores minimum (4 cores recommended)
- **Network**: Stable internet connection with public IP

### **Domain & SSL**
- **Domain Name**: Your website domain (e.g., yoursite.com)
- **DNS Access**: Ability to configure DNS records
- **SSL Certificate**: Let's Encrypt (free) or commercial SSL

### **Required Services**
- **MongoDB Atlas** (cloud database) or self-hosted MongoDB
- **Anthropic Claude API** key for content generation
- **Email Service** (optional, for notifications)
- **CDN Service** (optional, for performance)

---

## **🛠️ Phase 1: Server Setup & Configuration**

### **Step 1: Initial Server Setup**

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install essential packages
sudo apt install -y curl wget git vim nginx certbot python3-certbot-nginx

# Install Node.js (for React frontend)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python 3.9+ (for FastAPI backend)
sudo apt install -y python3.9 python3.9-venv python3.9-dev python3-pip

# Install PM2 for process management
sudo npm install -g pm2

# Create application user
sudo useradd -m -s /bin/bash postvelocity
sudo usermod -aG sudo postvelocity
```

### **Step 2: Create Directory Structure**

```bash
# Switch to application user
sudo su - postvelocity

# Create application directories
mkdir -p /home/postvelocity/postvelocity
mkdir -p /home/postvelocity/postvelocity/backend
mkdir -p /home/postvelocity/postvelocity/frontend
mkdir -p /home/postvelocity/postvelocity/logs
mkdir -p /home/postvelocity/postvelocity/backups

# Set proper permissions
sudo chown -R postvelocity:postvelocity /home/postvelocity/postvelocity
chmod -R 755 /home/postvelocity/postvelocity
```

---

## **🗄️ Phase 2: Database Setup (MongoDB)**

### **Option A: MongoDB Atlas (Recommended)**

1. **Create MongoDB Atlas Account**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Sign up for free account
   - Create new cluster (free tier available)

2. **Configure Database**
   ```bash
   # Database name: postvelocity
   # Collections will be created automatically:
   # - companies
   # - content_generations
   # - beta_users
   # - beta_feedback
   # - seo_addons
   # - seo_parameters
   # - website_audits
   ```

3. **Get Connection String**
   - Click "Connect" → "Connect your application"
   - Copy connection string (format: `mongodb+srv://username:password@cluster.mongodb.net/postvelocity`)

### **Option B: Self-Hosted MongoDB**

```bash
# Install MongoDB
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Create database and user
mongosh
use postvelocity
db.createUser({
  user: "postvelocity",
  pwd: "your_secure_password",
  roles: [{role: "readWrite", db: "postvelocity"}]
})
exit
```

---

## **🔧 Phase 3: Backend Deployment (FastAPI)**

### **Step 1: Deploy Backend Code**

```bash
# Navigate to backend directory
cd /home/postvelocity/postvelocity/backend

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
motor==3.3.2
pydantic==2.5.0
anthropic==0.7.8
aiofiles==23.2.1
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
Pillow==10.1.0
beautifulsoup4==4.12.2
textstat==0.7.3
nltk==3.8.1
pymongo==4.6.0
dnspython==2.4.2
EOF

# Install dependencies
pip install -r requirements.txt

# Create main application file
cat > server.py << 'EOF'
[COPY THE COMPLETE server.py FILE FROM /app/backend/server.py]
EOF

# Create security file
cat > security.py << 'EOF'
[COPY THE COMPLETE security.py FILE FROM /app/backend/security.py]
EOF
```

### **Step 2: Create Backend Environment File**

```bash
# Create .env file
cat > .env << 'EOF'
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/postvelocity
CLAUDE_API_KEY=your_anthropic_api_key_here
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=your_secret_key_here_minimum_32_characters
CORS_ORIGINS=https://yourdomain.com
EOF

# Secure the environment file
chmod 600 .env
```

### **Step 3: Test Backend**

```bash
# Test backend locally
source venv/bin/activate
python server.py

# Test API endpoints
curl http://localhost:8001/api/health
curl http://localhost:8001/api/companies
```

---

## **⚛️ Phase 4: Frontend Deployment (React)**

### **Step 1: Deploy Frontend Code**

```bash
# Navigate to frontend directory
cd /home/postvelocity/postvelocity/frontend

# Create package.json
cat > package.json << 'EOF'
{
  "name": "postvelocity-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1",
    "@tailwindcss/forms": "^0.5.7"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "eslintConfig": {
    "extends": [
      "react-app"
    ]
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6"
  }
}
EOF

# Install dependencies
npm install

# Create directory structure
mkdir -p src public
```

### **Step 2: Create Frontend Files**

```bash
# Create public/index.html
cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta name="description" content="PostVelocity - AI-Powered Social Media Management Platform" />
    <title>PostVelocity - AI Social Media Management</title>
</head>
<body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
</body>
</html>
EOF

# Create src/index.js
cat > src/index.js << 'EOF'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
EOF

# Create src/App.js
cat > src/App.js << 'EOF'
[COPY THE COMPLETE App.js FILE FROM /app/frontend/src/App.js]
EOF

# Create src/App.css
cat > src/App.css << 'EOF'
[COPY THE COMPLETE App.css FILE FROM /app/frontend/src/App.css]
EOF

# Create src/index.css
cat > src/index.css << 'EOF'
[COPY THE COMPLETE index.css FILE FROM /app/frontend/src/index.css]
EOF
```

### **Step 3: Create Frontend Environment File**

```bash
# Create .env file
cat > .env << 'EOF'
REACT_APP_BACKEND_URL=https://yourdomain.com
REACT_APP_ENVIRONMENT=production
GENERATE_SOURCEMAP=false
EOF
```

### **Step 4: Configure Tailwind CSS**

```bash
# Create tailwind.config.js
cat > tailwind.config.js << 'EOF'
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}
EOF

# Create postcss.config.js
cat > postcss.config.js << 'EOF'
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
EOF
```

### **Step 5: Build Frontend**

```bash
# Build production version
npm run build

# Test build
npm install -g serve
serve -s build -l 3000
```

---

## **🌐 Phase 5: Web Server Configuration (Nginx)**

### **Step 1: Configure Nginx**

```bash
# Create Nginx configuration
sudo tee /etc/nginx/sites-available/postvelocity << 'EOF'
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # Frontend (React)
    location / {
        root /home/postvelocity/postvelocity/frontend/build;
        index index.html;
        try_files $uri $uri/ /index.html;
        
        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, no-transform";
        }
    }

    # Backend API (FastAPI)
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:8001/api/health;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Error pages
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
    
    # Logs
    access_log /var/log/nginx/postvelocity_access.log;
    error_log /var/log/nginx/postvelocity_error.log;
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/postvelocity /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t
```

### **Step 2: SSL Certificate Setup**

```bash
# Install SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Test automatic renewal
sudo certbot renew --dry-run

# Create auto-renewal cron job
sudo crontab -e
# Add this line:
0 12 * * * /usr/bin/certbot renew --quiet
```

---

## **🔄 Phase 6: Process Management (PM2)**

### **Step 1: Create PM2 Configuration**

```bash
# Create PM2 ecosystem file
cat > /home/postvelocity/postvelocity/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'postvelocity-backend',
      script: '/home/postvelocity/postvelocity/backend/server.py',
      interpreter: '/home/postvelocity/postvelocity/backend/venv/bin/python',
      cwd: '/home/postvelocity/postvelocity/backend',
      instances: 2,
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
        PORT: 8001
      },
      error_file: '/home/postvelocity/postvelocity/logs/backend-error.log',
      out_file: '/home/postvelocity/postvelocity/logs/backend-out.log',
      log_file: '/home/postvelocity/postvelocity/logs/backend-combined.log',
      time: true,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      max_memory_restart: '1G'
    }
  ]
};
EOF
```

### **Step 2: Start Services**

```bash
# Start backend with PM2
cd /home/postvelocity/postvelocity
pm2 start ecosystem.config.js

# Save PM2 configuration
pm2 save

# Setup PM2 startup script
pm2 startup
# Follow the instructions provided by PM2

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## **🔧 Phase 7: Environment Configuration**

### **Step 1: API Keys Setup**

```bash
# Edit backend .env file
cd /home/postvelocity/postvelocity/backend
nano .env
```

**Required API Keys:**
```bash
# Anthropic Claude API Key
CLAUDE_API_KEY=YOUR_CLAUDE_API_KEY_HERE

# MongoDB Connection
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/postvelocity

# Application Security
SECRET_KEY=your-super-secret-key-32-characters-minimum

# CORS Settings
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### **Step 2: Frontend Environment**

```bash
# Edit frontend .env file
cd /home/postvelocity/postvelocity/frontend
nano .env
```

**Frontend Configuration:**
```bash
# Backend API URL
REACT_APP_BACKEND_URL=https://yourdomain.com

# Environment
REACT_APP_ENVIRONMENT=production

# Disable source maps in production
GENERATE_SOURCEMAP=false
```

### **Step 3: Rebuild Frontend**

```bash
# Rebuild frontend with production settings
cd /home/postvelocity/postvelocity/frontend
npm run build

# Update Nginx to serve new build
sudo systemctl reload nginx
```

---

## **🔍 Phase 8: Testing & Verification**

### **Step 1: Backend API Testing**

```bash
# Test health endpoint
curl https://yourdomain.com/health

# Test API endpoints
curl https://yourdomain.com/api/companies
curl https://yourdomain.com/api/platforms

# Test with authentication
curl -X POST https://yourdomain.com/api/companies \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Company","industry":"Technology"}'
```

### **Step 2: Frontend Testing**

```bash
# Test main page
curl -I https://yourdomain.com

# Test static assets
curl -I https://yourdomain.com/static/css/main.css
curl -I https://yourdomain.com/static/js/main.js

# Test API integration
# Open browser and navigate to https://yourdomain.com
# Check browser console for any errors
```

### **Step 3: Feature Testing Checklist**

**✅ Core Features:**
- [ ] User registration and login
- [ ] Company creation and management
- [ ] Content generation with Claude API
- [ ] Platform selection and content optimization
- [ ] Media upload and management
- [ ] Analytics dashboard

**✅ Advanced Features:**
- [ ] Beta feedback system
- [ ] SEO monitoring add-on
- [ ] Payment and trial system
- [ ] Training materials access
- [ ] Calendar and scheduling
- [ ] Automation features

**✅ Technical Features:**
- [ ] HTTPS encryption working
- [ ] API endpoints responding correctly
- [ ] Database connections stable
- [ ] File uploads working
- [ ] Email notifications (if configured)
- [ ] Error handling and logging

---

## **🔐 Phase 9: Security Configuration**

### **Step 1: Firewall Setup**

```bash
# Configure UFW firewall
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw --force enable

# Check firewall status
sudo ufw status verbose
```

### **Step 2: Security Hardening**

```bash
# Disable root login
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Set up fail2ban
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Configure automatic security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### **Step 3: Backup Configuration**

```bash
# Create backup script
sudo tee /home/postvelocity/postvelocity/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/home/postvelocity/postvelocity/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database (if using local MongoDB)
# mongodump --out $BACKUP_DIR/mongodb_$DATE

# Backup application files
tar -czf $BACKUP_DIR/postvelocity_$DATE.tar.gz \
  /home/postvelocity/postvelocity/backend \
  /home/postvelocity/postvelocity/frontend \
  /etc/nginx/sites-available/postvelocity

# Keep only last 7 days of backups
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
EOF

# Make backup script executable
chmod +x /home/postvelocity/postvelocity/backup.sh

# Add to crontab
crontab -e
# Add this line for daily backup at 2 AM:
0 2 * * * /home/postvelocity/postvelocity/backup.sh
```

---

## **📊 Phase 10: Monitoring & Logging**

### **Step 1: Log Management**

```bash
# Configure log rotation
sudo tee /etc/logrotate.d/postvelocity << 'EOF'
/home/postvelocity/postvelocity/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 postvelocity postvelocity
    postrotate
        pm2 reload postvelocity-backend
    endscript
}
EOF

# Configure Nginx log rotation
sudo tee /etc/logrotate.d/nginx-postvelocity << 'EOF'
/var/log/nginx/postvelocity_*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 0644 www-data www-data
    postrotate
        nginx -s reload
    endscript
}
EOF
```

### **Step 2: Monitoring Setup**

```bash
# Create monitoring script
sudo tee /home/postvelocity/postvelocity/monitor.sh << 'EOF'
#!/bin/bash
LOG_FILE="/home/postvelocity/postvelocity/logs/monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Check backend health
BACKEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/api/health)

# Check frontend
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://yourdomain.com)

# Check database connection
DB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/api/companies)

# Log status
echo "[$DATE] Backend: $BACKEND_STATUS, Frontend: $FRONTEND_STATUS, DB: $DB_STATUS" >> $LOG_FILE

# Send alert if any service is down
if [ "$BACKEND_STATUS" != "200" ] || [ "$FRONTEND_STATUS" != "200" ] || [ "$DB_STATUS" != "200" ]; then
    echo "[$DATE] ALERT: Service down - Backend: $BACKEND_STATUS, Frontend: $FRONTEND_STATUS, DB: $DB_STATUS" >> $LOG_FILE
    # Add email notification here if needed
fi
EOF

# Make monitoring script executable
chmod +x /home/postvelocity/postvelocity/monitor.sh

# Add to crontab for every 5 minutes
crontab -e
# Add this line:
*/5 * * * * /home/postvelocity/postvelocity/monitor.sh
```

---

## **🚀 Phase 11: Performance Optimization**

### **Step 1: Database Optimization**

```bash
# MongoDB optimization (if self-hosted)
# Add to MongoDB configuration
sudo tee -a /etc/mongod.conf << 'EOF'
# Performance settings
operationProfiling:
  slowOpThresholdMs: 100
  mode: slowOp

# Index optimization
setParameter:
  internalQueryExecMaxBlockingSortBytes: 167772160
EOF

# Restart MongoDB
sudo systemctl restart mongod
```

### **Step 2: Nginx Optimization**

```bash
# Update Nginx configuration for better performance
sudo tee -a /etc/nginx/nginx.conf << 'EOF'
# Worker processes
worker_processes auto;
worker_connections 1024;

# Buffer sizes
client_body_buffer_size 128k;
client_max_body_size 100m;
client_header_buffer_size 1k;
large_client_header_buffers 4 4k;

# Timeout settings
client_body_timeout 12;
client_header_timeout 12;
keepalive_timeout 15;
send_timeout 10;

# Gzip compression
gzip on;
gzip_comp_level 6;
gzip_min_length 1000;
gzip_proxied any;
gzip_vary on;
gzip_types
    application/atom+xml
    application/javascript
    application/json
    application/rss+xml
    application/vnd.ms-fontobject
    application/x-font-ttf
    application/x-web-app-manifest+json
    application/xhtml+xml
    application/xml
    font/opentype
    image/svg+xml
    image/x-icon
    text/css
    text/plain
    text/x-component;
EOF

# Reload Nginx
sudo systemctl reload nginx
```

### **Step 3: Backend Optimization**

```bash
# Update PM2 configuration for better performance
cat > /home/postvelocity/postvelocity/ecosystem.config.js << 'EOF'
module.exports = {
  apps: [
    {
      name: 'postvelocity-backend',
      script: '/home/postvelocity/postvelocity/backend/server.py',
      interpreter: '/home/postvelocity/postvelocity/backend/venv/bin/python',
      cwd: '/home/postvelocity/postvelocity/backend',
      instances: 'max',
      exec_mode: 'cluster',
      env: {
        NODE_ENV: 'production',
        PORT: 8001,
        UVICORN_WORKERS: 4
      },
      error_file: '/home/postvelocity/postvelocity/logs/backend-error.log',
      out_file: '/home/postvelocity/postvelocity/logs/backend-out.log',
      log_file: '/home/postvelocity/postvelocity/logs/backend-combined.log',
      time: true,
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s',
      max_memory_restart: '1G',
      watch: false,
      ignore_watch: ["node_modules", "logs"]
    }
  ]
};
EOF

# Restart PM2
pm2 restart ecosystem.config.js
```

---

## **🔧 Phase 12: Troubleshooting Guide**

### **Common Issues & Solutions**

#### **1. Backend API Not Responding**

**Symptoms:**
- 502 Bad Gateway errors
- API endpoints returning 500 errors
- Backend not starting

**Diagnosis:**
```bash
# Check backend logs
pm2 logs postvelocity-backend

# Check if backend is running
pm2 status

# Check port 8001
netstat -tlnp | grep 8001

# Test backend directly
curl http://localhost:8001/api/health
```

**Solutions:**
```bash
# Restart backend
pm2 restart postvelocity-backend

# Check environment variables
cd /home/postvelocity/postvelocity/backend
cat .env

# Check Python dependencies
source venv/bin/activate
pip list

# Reinstall dependencies if needed
pip install -r requirements.txt
```

#### **2. Frontend Not Loading**

**Symptoms:**
- White screen on website
- 404 errors for static assets
- JavaScript errors in browser console

**Diagnosis:**
```bash
# Check Nginx logs
sudo tail -f /var/log/nginx/postvelocity_error.log

# Check if build exists
ls -la /home/postvelocity/postvelocity/frontend/build/

# Test frontend build
cd /home/postvelocity/postvelocity/frontend
npm run build
```

**Solutions:**
```bash
# Rebuild frontend
cd /home/postvelocity/postvelocity/frontend
npm run build

# Check environment variables
cat .env

# Restart Nginx
sudo systemctl restart nginx

# Check Nginx configuration
sudo nginx -t
```

#### **3. Database Connection Issues**

**Symptoms:**
- Database connection timeout errors
- 500 errors on API endpoints that use database
- MongoDB connection refused

**Diagnosis:**
```bash
# Check MongoDB Atlas connection string
cd /home/postvelocity/postvelocity/backend
grep MONGO_URL .env

# Test database connection
python3 -c "
import motor.motor_asyncio
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGO_URL'))

async def test_connection():
    try:
        await client.admin.command('ping')
        print('Database connection successful')
    except Exception as e:
        print(f'Database connection failed: {e}')

asyncio.run(test_connection())
"
```

**Solutions:**
```bash
# Update MongoDB Atlas IP whitelist
# Go to MongoDB Atlas → Network Access → Add IP Address → Add Current IP

# Check connection string format
# Should be: mongodb+srv://username:password@cluster.mongodb.net/postvelocity

# Test with different connection method
# Try adding ?retryWrites=true&w=majority to connection string
```

#### **4. SSL Certificate Issues**

**Symptoms:**
- SSL certificate expired warnings
- "Not secure" in browser
- Certificate chain issues

**Diagnosis:**
```bash
# Check certificate expiry
sudo certbot certificates

# Check certificate chain
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com
```

**Solutions:**
```bash
# Renew certificate
sudo certbot renew

# Force renewal
sudo certbot renew --force-renewal

# Update Nginx configuration
sudo nginx -t
sudo systemctl reload nginx
```

#### **5. Permission Issues**

**Symptoms:**
- Cannot write to log files
- File upload errors
- PM2 permission denied

**Diagnosis:**
```bash
# Check file permissions
ls -la /home/postvelocity/postvelocity/
ls -la /home/postvelocity/postvelocity/logs/

# Check user ownership
ps aux | grep postvelocity
```

**Solutions:**
```bash
# Fix ownership
sudo chown -R postvelocity:postvelocity /home/postvelocity/postvelocity/

# Fix permissions
chmod -R 755 /home/postvelocity/postvelocity/
chmod -R 644 /home/postvelocity/postvelocity/backend/.env
chmod -R 644 /home/postvelocity/postvelocity/frontend/.env
```

---

## **📈 Phase 13: Performance Monitoring**

### **Step 1: System Monitoring**

```bash
# Install system monitoring tools
sudo apt install -y htop iotop nethogs

# Create system monitoring script
sudo tee /home/postvelocity/postvelocity/system-monitor.sh << 'EOF'
#!/bin/bash
LOG_FILE="/home/postvelocity/postvelocity/logs/system-monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# CPU usage
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')

# Memory usage
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.1f", $3/$2 * 100.0}')

# Disk usage
DISK_USAGE=$(df -h / | awk 'NR==2{printf "%s", $5}')

# Network connections
CONNECTIONS=$(netstat -an | grep ESTABLISHED | wc -l)

# Log metrics
echo "[$DATE] CPU: ${CPU_USAGE}%, Memory: ${MEMORY_USAGE}%, Disk: ${DISK_USAGE}, Connections: ${CONNECTIONS}" >> $LOG_FILE

# Alert if usage is too high
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "[$DATE] ALERT: High CPU usage: ${CPU_USAGE}%" >> $LOG_FILE
fi

if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "[$DATE] ALERT: High memory usage: ${MEMORY_USAGE}%" >> $LOG_FILE
fi
EOF

# Make script executable
chmod +x /home/postvelocity/postvelocity/system-monitor.sh

# Add to crontab
crontab -e
# Add this line for every 10 minutes:
*/10 * * * * /home/postvelocity/postvelocity/system-monitor.sh
```

### **Step 2: Application Monitoring**

```bash
# Create application monitoring script
sudo tee /home/postvelocity/postvelocity/app-monitor.sh << 'EOF'
#!/bin/bash
LOG_FILE="/home/postvelocity/postvelocity/logs/app-monitor.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Check PM2 processes
PM2_STATUS=$(pm2 jlist | jq -r '.[] | select(.name=="postvelocity-backend") | .pm2_env.status')

# Check backend response time
BACKEND_RESPONSE_TIME=$(curl -o /dev/null -s -w "%{time_total}" http://localhost:8001/api/health)

# Check frontend response time
FRONTEND_RESPONSE_TIME=$(curl -o /dev/null -s -w "%{time_total}" https://yourdomain.com)

# Check database response time
DB_RESPONSE_TIME=$(curl -o /dev/null -s -w "%{time_total}" http://localhost:8001/api/companies)

# Log metrics
echo "[$DATE] PM2: $PM2_STATUS, Backend: ${BACKEND_RESPONSE_TIME}s, Frontend: ${FRONTEND_RESPONSE_TIME}s, DB: ${DB_RESPONSE_TIME}s" >> $LOG_FILE

# Alert if response times are too slow
if (( $(echo "$BACKEND_RESPONSE_TIME > 5" | bc -l) )); then
    echo "[$DATE] ALERT: Slow backend response: ${BACKEND_RESPONSE_TIME}s" >> $LOG_FILE
fi

if (( $(echo "$FRONTEND_RESPONSE_TIME > 3" | bc -l) )); then
    echo "[$DATE] ALERT: Slow frontend response: ${FRONTEND_RESPONSE_TIME}s" >> $LOG_FILE
fi
EOF

# Make script executable
chmod +x /home/postvelocity/postvelocity/app-monitor.sh

# Add to crontab
crontab -e
# Add this line for every 5 minutes:
*/5 * * * * /home/postvelocity/postvelocity/app-monitor.sh
```

---

## **🔄 Phase 14: Maintenance & Updates**

### **Step 1: Update Procedures**

```bash
# Create update script
sudo tee /home/postvelocity/postvelocity/update.sh << 'EOF'
#!/bin/bash
echo "Starting PostVelocity update..."

# Backup current version
./backup.sh

# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Node.js packages
cd /home/postvelocity/postvelocity/frontend
npm update

# Update Python packages
cd /home/postvelocity/postvelocity/backend
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Rebuild frontend
cd /home/postvelocity/postvelocity/frontend
npm run build

# Restart services
pm2 restart postvelocity-backend
sudo systemctl reload nginx

# Run health check
sleep 10
curl -f http://localhost:8001/api/health && echo "Backend healthy"
curl -f https://yourdomain.com && echo "Frontend healthy"

echo "Update completed successfully"
EOF

# Make script executable
chmod +x /home/postvelocity/postvelocity/update.sh
```

### **Step 2: Scheduled Maintenance**

```bash
# Create maintenance window script
sudo tee /home/postvelocity/postvelocity/maintenance.sh << 'EOF'
#!/bin/bash
MAINTENANCE_FILE="/home/postvelocity/postvelocity/frontend/build/maintenance.html"

# Create maintenance page
cat > $MAINTENANCE_FILE << 'MAINT_EOF'
<!DOCTYPE html>
<html>
<head>
    <title>PostVelocity - Maintenance</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .container { max-width: 600px; margin: 0 auto; }
        h1 { color: #333; }
        p { color: #666; font-size: 18px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔧 Maintenance Mode</h1>
        <p>PostVelocity is currently undergoing scheduled maintenance.</p>
        <p>We'll be back online shortly. Thank you for your patience!</p>
    </div>
</body>
</html>
MAINT_EOF

# Update Nginx to show maintenance page
sudo sed -i 's/try_files \$uri \$uri\/ \/index.html;/try_files \$uri \$uri\/ \/maintenance.html;/' /etc/nginx/sites-available/postvelocity
sudo systemctl reload nginx

echo "Maintenance mode enabled"
EOF

# Create script to exit maintenance mode
sudo tee /home/postvelocity/postvelocity/exit-maintenance.sh << 'EOF'
#!/bin/bash
# Restore normal operation
sudo sed -i 's/try_files \$uri \$uri\/ \/maintenance.html;/try_files \$uri \$uri\/ \/index.html;/' /etc/nginx/sites-available/postvelocity
sudo systemctl reload nginx

# Remove maintenance page
rm -f /home/postvelocity/postvelocity/frontend/build/maintenance.html

echo "Maintenance mode disabled"
EOF

# Make scripts executable
chmod +x /home/postvelocity/postvelocity/maintenance.sh
chmod +x /home/postvelocity/postvelocity/exit-maintenance.sh
```

---

## **📝 Phase 15: Documentation & Final Checklist**

### **Step 1: Create Operations Manual**

```bash
# Create operations manual
sudo tee /home/postvelocity/postvelocity/OPERATIONS.md << 'EOF'
# PostVelocity Operations Manual

## Daily Operations
- Check monitoring logs: `tail -f /home/postvelocity/postvelocity/logs/monitor.log`
- Check system status: `pm2 status`
- Check disk space: `df -h`

## Weekly Operations
- Review error logs: `sudo tail -f /var/log/nginx/postvelocity_error.log`
- Check SSL certificate: `sudo certbot certificates`
- Review performance metrics: `cat /home/postvelocity/postvelocity/logs/system-monitor.log`

## Monthly Operations
- Update system: `sudo apt update && sudo apt upgrade`
- Backup database: Run backup script
- Review security logs: `sudo tail -f /var/log/auth.log`

## Emergency Procedures
- Restart all services: `pm2 restart all && sudo systemctl restart nginx`
- Enable maintenance mode: `./maintenance.sh`
- Disable maintenance mode: `./exit-maintenance.sh`
- Restore from backup: See backup documentation

## Important File Locations
- Backend: `/home/postvelocity/postvelocity/backend/`
- Frontend: `/home/postvelocity/postvelocity/frontend/`
- Logs: `/home/postvelocity/postvelocity/logs/`
- Nginx config: `/etc/nginx/sites-available/postvelocity`
- SSL certs: `/etc/letsencrypt/live/yourdomain.com/`

## Emergency Contacts
- System Administrator: [Your contact information]
- Developer: [Developer contact information]
- Hosting Provider: [Hosting provider support]
EOF
```

### **Step 2: Final Verification Checklist**

```bash
# Create verification script
sudo tee /home/postvelocity/postvelocity/verify-deployment.sh << 'EOF'
#!/bin/bash
echo "PostVelocity Deployment Verification"
echo "===================================="

# Check system services
echo "1. System Services:"
systemctl is-active nginx && echo "  ✅ Nginx running" || echo "  ❌ Nginx not running"
systemctl is-active mongod && echo "  ✅ MongoDB running" || echo "  ⚠️ MongoDB not running (may be using Atlas)"

# Check PM2 processes
echo "2. Application Processes:"
pm2 list | grep -q "postvelocity-backend" && echo "  ✅ Backend running" || echo "  ❌ Backend not running"

# Check ports
echo "3. Network Ports:"
netstat -tlnp | grep -q ":80" && echo "  ✅ HTTP port 80 open" || echo "  ❌ HTTP port 80 not open"
netstat -tlnp | grep -q ":443" && echo "  ✅ HTTPS port 443 open" || echo "  ❌ HTTPS port 443 not open"
netstat -tlnp | grep -q ":8001" && echo "  ✅ Backend port 8001 open" || echo "  ❌ Backend port 8001 not open"

# Check API endpoints
echo "4. API Endpoints:"
curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/api/health | grep -q "200" && echo "  ✅ Backend health check OK" || echo "  ❌ Backend health check failed"
curl -s -o /dev/null -w "%{http_code}" https://yourdomain.com | grep -q "200" && echo "  ✅ Frontend accessible" || echo "  ❌ Frontend not accessible"

# Check SSL certificate
echo "5. SSL Certificate:"
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com </dev/null 2>/dev/null | grep -q "Verify return code: 0" && echo "  ✅ SSL certificate valid" || echo "  ❌ SSL certificate issue"

# Check file permissions
echo "6. File Permissions:"
[ -r /home/postvelocity/postvelocity/backend/.env ] && echo "  ✅ Backend environment file readable" || echo "  ❌ Backend environment file not readable"
[ -r /home/postvelocity/postvelocity/frontend/.env ] && echo "  ✅ Frontend environment file readable" || echo "  ❌ Frontend environment file not readable"

# Check logs
echo "7. Logging:"
[ -f /home/postvelocity/postvelocity/logs/monitor.log ] && echo "  ✅ Monitor log exists" || echo "  ❌ Monitor log missing"
[ -f /var/log/nginx/postvelocity_access.log ] && echo "  ✅ Nginx access log exists" || echo "  ❌ Nginx access log missing"

echo "===================================="
echo "Verification complete!"
EOF

# Make script executable
chmod +x /home/postvelocity/postvelocity/verify-deployment.sh

# Run verification
./verify-deployment.sh
```

---

## **🚀 Final Production Checklist**

### **✅ Pre-Launch Checklist**

**System Requirements:**
- [ ] Server meets minimum requirements (4GB RAM, 2 CPU cores, 20GB storage)
- [ ] Ubuntu 20.04 LTS or later installed
- [ ] Root access available
- [ ] Domain name configured with DNS pointing to server

**Software Installation:**
- [ ] Node.js 18.x installed
- [ ] Python 3.9+ installed
- [ ] Nginx installed and configured
- [ ] PM2 process manager installed
- [ ] MongoDB Atlas account created (or local MongoDB installed)

**Application Deployment:**
- [ ] Backend code deployed to `/home/postvelocity/postvelocity/backend/`
- [ ] Frontend code deployed to `/home/postvelocity/postvelocity/frontend/`
- [ ] Python virtual environment created and dependencies installed
- [ ] Node.js dependencies installed
- [ ] Frontend built for production (`npm run build`)

**Configuration:**
- [ ] Backend `.env` file configured with MongoDB URL and API keys
- [ ] Frontend `.env` file configured with backend URL
- [ ] Nginx virtual host configured
- [ ] SSL certificate installed and configured
- [ ] PM2 ecosystem file configured

**Database Setup:**
- [ ] MongoDB database created (postvelocity)
- [ ] Database user created with appropriate permissions
- [ ] Connection string tested and working

**Security:**
- [ ] Firewall configured (UFW)
- [ ] SSH hardened (disable root login)
- [ ] SSL certificate installed and auto-renewal configured
- [ ] Fail2ban installed and configured
- [ ] File permissions properly set

**Monitoring & Backup:**
- [ ] Monitoring scripts installed and configured
- [ ] Log rotation configured
- [ ] Backup script created and scheduled
- [ ] System monitoring scheduled (crontab)

**Testing:**
- [ ] Backend health check responds (200 OK)
- [ ] Frontend loads correctly
- [ ] All API endpoints tested
- [ ] SSL certificate verified
- [ ] Database connection tested
- [ ] File uploads working
- [ ] Authentication working

**Performance:**
- [ ] Nginx compression enabled
- [ ] PM2 clustering configured
- [ ] Database indexes created
- [ ] Static file caching configured
- [ ] CDN configured (optional)

**Go-Live:**
- [ ] DNS propagation complete
- [ ] All services running
- [ ] Monitoring active
- [ ] Backup scheduled
- [ ] Operations manual created
- [ ] Emergency procedures documented

---

## **🎯 Success Metrics**

After completing this deployment, you should achieve:

**Performance Metrics:**
- **Frontend Load Time**: < 3 seconds
- **Backend API Response**: < 1 second
- **Database Query Time**: < 500ms
- **SSL Certificate Score**: A+ rating

**Availability Metrics:**
- **Uptime**: 99.9% or higher
- **Error Rate**: < 1%
- **Response Success Rate**: 99%+

**Security Metrics:**
- **SSL Certificate**: Valid and auto-renewing
- **Security Headers**: All implemented
- **Firewall**: Properly configured
- **Access Control**: Restricted and monitored

**Monitoring Metrics:**
- **System Monitoring**: Every 10 minutes
- **Application Monitoring**: Every 5 minutes
- **Health Checks**: Every 5 minutes
- **Backup**: Daily automated backups

---

## **📞 Support & Maintenance**

### **Regular Maintenance Schedule**

**Daily (Automated):**
- System monitoring
- Application health checks
- Log rotation
- Backup execution

**Weekly (Manual):**
- Review error logs
- Check SSL certificate status
- Monitor performance metrics
- Review security logs

**Monthly (Manual):**
- System updates
- Security patches
- Performance optimization
- Backup testing

**Quarterly (Manual):**
- Full security audit
- Performance review
- Capacity planning
- Documentation updates

### **Emergency Support**

**Critical Issues (Immediate Response):**
- Site completely down
- Database corruption
- Security breach
- SSL certificate expired

**High Priority (4-hour Response):**
- Performance degradation
- API endpoints failing
- Authentication issues
- Payment system problems

**Medium Priority (24-hour Response):**
- Minor UI issues
- Non-critical feature bugs
- Monitoring alerts
- Log analysis

**Low Priority (72-hour Response):**
- Feature requests
- UI improvements
- Documentation updates
- Optimization suggestions

---

## **🎉 Congratulations!**

You have successfully deployed PostVelocity to production! Your AI-powered social media management platform is now live and ready to help businesses create engaging content across multiple platforms.

**Key Features Now Live:**
- ✅ AI-powered content generation with Claude
- ✅ Multi-platform social media management
- ✅ Beta feedback system for continuous improvement
- ✅ SEO monitoring add-on for website optimization
- ✅ Advanced analytics and ROI tracking
- ✅ Secure payment and trial system
- ✅ Comprehensive training materials

**Next Steps:**
1. Share your platform URL with beta testers
2. Monitor performance and user feedback
3. Collect analytics and optimize based on usage
4. Scale infrastructure as your user base grows
5. Implement additional features based on user requests

**Remember:** This deployment guide ensures your PostVelocity platform is production-ready, secure, and optimized for performance. Follow the maintenance procedures to keep your platform running smoothly and your users happy!

🚀 **Your PostVelocity platform is now live and ready to revolutionize social media management!**