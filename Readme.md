# **README: Simple Share Server PWA**

# 📱 Simple Share Server PWA

**Share files between devices on the same WiFi network instantly!**  
A Progressive Web App (PWA) that works like a native mobile app for seamless file sharing between laptops, phones, and tablets.

![Simple Share Server PWA](https://img.icons8.com/color/96/000000/share.png)

##  Features

### 📱 **PWA Features**
- **Installable** - Add to home screen like a native app
- **Offline Support** - Works without internet connection
- **Push Notifications** - Real-time file share alerts
- **Camera Integration** - Take photos and share instantly
- **Gallery Access** - Upload from phone gallery
- **Dark Mode** - Automatic theme detection
- **Splash Screen** - Professional app-like launch
- **App Shortcuts** - Quick actions from home screen

### 🔄 **Sharing Features**
- 📤 **Drag & Drop** file upload
- 📲 **QR Code Scanner** - Easy connection from phone
- 🔗 **Copy URL** with one click
- 📁 **Multiple File Support** - Upload/download multiple files
- 📊 **Progress Indicators** - Real-time upload progress
- 🔄 **Auto Refresh** - See new files instantly
- 🗑️ **File Management** - Upload/download/delete files

### 🌐 **Cross-Platform**
- **iOS** (iPhone, iPad) - Safari
- **Android** - Chrome, Firefox
- **Windows/Mac/Linux** - All modern browsers
- **Tablets** - Responsive design

## 📋 Requirements

### **Server Requirements:**
- Python 3.6+
- Flask (`pip install flask`)

### **Client Requirements:**
- Modern web browser (Chrome 70+, Safari 12+, Edge 79+)
- Devices must be on **same WiFi network**

## 🛠️ Installation

### **1. Server Setup (Laptop/Desktop)**

```bash
# Clone or download the project
git clone https://github.com/yourusername/simple-share.git
cd simple-share

# Install dependencies
pip install flask

# Run the server
python app.py
```

### **2. Install as PWA on Mobile Devices**

#### **iOS (iPhone/iPad):**
1. Open **Safari**
2. Go to: `http://YOUR-LAPTOP-IP:5000/mobile`
   - Replace with actual IP shown in terminal
3. Tap **Share** button (📤)
4. Tap **"Add to Home Screen"**
5. Name it "Simple Share"
6. Tap **"Add"**

#### **Android:**
1. Open **Chrome**
2. Go to: `http://YOUR-LAPTOP-IP:5000/mobile`
3. Tap **Menu** (3 dots)
4. Tap **"Add to Home Screen"**
5. Tap **"Add"**
6. Or wait for install prompt to appear

#### **Chrome Desktop:**
1. Visit `http://localhost:5000/mobile`
2. Look for install icon in address bar (📥)
3. Click **"Install Simple Share"**

## 📱 How to Use

### **From Laptop to Phone:**
1. Start server on laptop
2. Open installed PWA on phone
3. Scan QR code or type URL
4. Upload files from laptop
5. Download on phone

### **From Phone to Phone:**
1. Start server on laptop
2. Both phones install PWA
3. Phone 1: Upload files via camera/gallery
4. Phone 2: Refresh and download files

### **From Phone to Laptop:**
1. Start server on laptop
2. Phone uploads files via PWA
3. Laptop downloads from browser

## 🌐 Network Configuration

### **Getting Your IP Address:**
```bash
# On Linux/Mac:
ifconfig | grep "inet "

# On Windows:
ipconfig
```

### **Firewall Settings:**
- **Windows:** Allow port 5000 in Windows Defender Firewall
- **Mac:** Allow incoming connections in Security & Privacy
- **Linux:** `sudo ufw allow 5000`

### **Troubleshooting Connection Issues:**
1. ✅ All devices on same WiFi
2. ✅ Firewall allows port 5000
3. ✅ Correct IP address (not localhost)
4. ✅ Mobile data disabled on phones

## 📁 Supported File Types

| Category | File Types | Max Size |
|----------|------------|----------|
| **Images** | PNG, JPG, JPEG, GIF | 100MB |
| **Documents** | PDF, TXT, DOC, DOCX | 100MB |
| **Spreadsheets** | XLS, XLSX | 100MB |
| **Media** | MP3, MP4 | 100MB |
| **Archives** | ZIP | 100MB |

## 🎨 PWA Features in Detail

### **Service Worker:**
- Caches app for offline use
- Background sync for uploads
- Push notification support

### **Web App Manifest:**
- Standalone display mode
- Custom splash screen
- App shortcuts
- Theme colors

### **Mobile Features:**
- Camera access (`capture="environment"`)
- File system access
- Gesture support
- Touch-optimized UI

## 🔧 Advanced Configuration

### **Change Port (if 5000 is busy):**
```python
# In app.py, change:
app.run(host='0.0.0.0', port=5000, ...)
# To:
app.run(host='0.0.0.0', port=8080, ...)
```

### **Change Upload Folder:**
```python
# In app.py, change:
UPLOAD_FOLDER = 'shared_files'
```

### **Add More File Types:**
```python
# In app.py, add to ALLOWED_EXTENSIONS:
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 
                      'mp3', 'mp4', 'zip', 'doc', 'docx', 'xls', 
                      'xlsx', 'ppt', 'pptx'}  # Added PowerPoint
```

### **Increase File Size Limit:**
```python
# In app.py, change (in MB):
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB
```

## 🚀 Quick Start Commands

```bash
# 1. Start server
python app.py

# 2. Access on laptop
#    http://localhost:5000

# 3. Access on mobile
#    http://YOUR-IP:5000/mobile
#    Example: http://192.168.1.100:5000/mobile

# 4. Stop server
#    Press Ctrl+C in terminal
```

## 📊 Performance

- **Initial Load:** ~2 seconds
- **File Upload:** ~10MB/second on WiFi
- **Offline Cache:** ~5MB
- **Memory Usage:** ~50MB

## 🔒 Security Notes

- **Local Network Only:** Works only on same WiFi
- **No Authentication:** Simple sharing (add password if needed)
- **File Type Restrictions:** Prevents malicious uploads
- **Size Limits:** Prevents server overload

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 🐛 Troubleshooting

### **Common Issues:**

#### **"Can't connect from phone"**
```bash
# Check laptop firewall
sudo ufw status  # Linux
# Allow port 5000
sudo ufw allow 5000
```

#### **"Upload fails"**
- Check file size (< 100MB)
- Check file type (allowed extensions)
- Check disk space

#### **"PWA not installing"**
- Use HTTPS in production
- Ensure manifest.json is served correctly
- Clear browser cache

#### **"QR code not working"**
- Ensure camera has permission
- Good lighting conditions
- Center QR code in frame

### **Debug Commands:**
```bash
# Check if server is running
netstat -an | grep 5000

# Check Python version
python --version

# Check Flask installation
python -c "import flask; print(flask.__version__)"
```

## 📱 Mobile-Specific Instructions

### **iOS Specific:**
- Requires iOS 12.2+
- Safari only
- Camera permissions needed
- Can't run in background

### **Android Specific:**
- Chrome 72+ recommended
- Can install from any browser
- Background sync available
- File system access

## 🌟 Pro Tips

1. **Bookmark the URL** for quick access
2. **Use QR codes** for group sharing
3. **Enable Dark Mode** for battery saving
4. **Clear cache** if app acts strange
5. **Restart server** if connections fail

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Icons by [Icons8](https://icons8.com)
- QR Code library by [davidshimjs](https://github.com/davidshimjs/qrcodejs)
- Font Awesome for icons
- Flask team for amazing framework


```
Desktop View:                 Mobile View:
┌─────────────────┐          ┌─────────────────┐
│  Simple Share   │          │  📱 Simple Share│
│  ┌───────────┐  │          │  ┌───────────┐  │
│  │  QR Code  │  │          │  │  Upload   │  │
│  └───────────┘  │          │  │  Options  │  │
│  ┌───────────┐  │          │  └───────────┘  │
│  │ File List │  │          │  ┌───────────┐  │
│  └───────────┘  │          │  │Recent Files│ │
└─────────────────┘          └─────────────────┘
```

---

**Made with ❤️ for easy file sharing between devices**