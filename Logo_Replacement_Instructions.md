# Logo Replacement Instructions 🖼️

## **How to Replace the PostVelocity Logo**

### **Step 1: Prepare Your Logo**
1. **Save your logo** as `logo.png` (or `logo.jpg`, `logo.svg`)
2. **Recommended size**: 32x32 pixels (or any square size)
3. **Format**: PNG with transparent background (recommended)
4. **File size**: Keep under 50KB for fast loading

### **Step 2: Add Logo to Your Project**

#### **Option A: For Local Development**
1. Place your logo file in: `/app/frontend/public/logo.png`
2. The logo will be automatically loaded

#### **Option B: For Heroku Deployment**
1. Add the logo to your project's `public` folder
2. When you deploy, the logo will be included
3. The logo will be available at: `https://your-app-name.herokuapp.com/logo.png`

#### **Option C: Use External URL**
1. Upload your logo to a service like:
   - **Imgur**: [imgur.com](https://imgur.com)
   - **Cloudinary**: [cloudinary.com](https://cloudinary.com)
   - **GitHub**: Put in your repository
2. Update the logo URL in the code (see Step 3)

### **Step 3: Update the Logo URL (If Needed)**

If your logo has a different name or is hosted externally, update this line in `App.js`:

```javascript
// Current code:
<img 
  src="/logo.png" 
  alt="PostVelocity Logo" 
  className="w-8 h-8 object-contain"
/>

// Update to your logo:
<img 
  src="/your-logo-name.png" 
  alt="PostVelocity Logo" 
  className="w-8 h-8 object-contain"
/>

// Or external URL:
<img 
  src="https://your-domain.com/logo.png" 
  alt="PostVelocity Logo" 
  className="w-8 h-8 object-contain"
/>
```

### **Step 4: Test Your Logo**
1. **Local testing**: Run your app and check the header
2. **Production testing**: Deploy and verify the logo appears
3. **Fallback**: If logo fails to load, rocket emoji 🚀 will show

### **Logo Sizing Options**

You can adjust the logo size by changing the CSS classes:

```javascript
// Small logo (24x24):
className="w-6 h-6 object-contain"

// Medium logo (32x32) - Current:
className="w-8 h-8 object-contain"

// Large logo (48x48):
className="w-12 h-12 object-contain"

// Extra large logo (64x64):
className="w-16 h-16 object-contain"
```

### **Current Logo Setup**
- **Location**: Header, left side next to "PostVelocity" title
- **Size**: 32x32 pixels (w-8 h-8)
- **Fallback**: Rocket emoji 🚀 if image fails to load
- **Alt text**: "PostVelocity Logo" for accessibility

### **File Structure**
```
/app/
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── logo.png          ← Your logo goes here
│   │   └── favicon.ico
│   └── src/
│       └── App.js             ← Logo reference is here
└── backend/
```

### **Troubleshooting**

**Issue: Logo not showing**
- Check file path: `/app/frontend/public/logo.png`
- Verify file name matches code: `src="/logo.png"`
- Check browser console for errors

**Issue: Logo too big/small**
- Adjust CSS classes: `w-8 h-8` to `w-6 h-6` (smaller) or `w-12 h-12` (larger)
- Use `object-contain` to maintain aspect ratio

**Issue: Logo quality poor**
- Use PNG format with transparent background
- Provide 2x size for high-DPI displays
- Consider SVG format for scalability

### **Best Practices**
1. **Use PNG or SVG** for best quality
2. **Transparent background** looks most professional
3. **Square aspect ratio** works best in header
4. **Optimize file size** for fast loading
5. **Test on different devices** to ensure it looks good

---

**Note**: I updated the code to expect the logo at `/logo.png`. Simply place your logo file in the `public` folder and it will automatically appear in the header!