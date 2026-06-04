# Complete Mobile App Setup Guide

## Option 3: Quick Phone Access (5 minutes)

### Step 1: Install flask-cors
```bash
cd c:\Users\AJAI MUHAMMED\Desktop\dream\dream
pip install flask-cors
```

### Step 2: Start Flask App
```bash
python app.py
```

### Step 3: Note Your IP Address
The terminal will show something like:
```
✅ Muhfal running on:
   Local: http://localhost:5000
   Network: http://192.168.1.100:5000
   Access from phone: http://192.168.1.100:5000
```

### Step 4: Open on Phone
- Connect phone to SAME WiFi
- Open browser
- Go to the Network URL shown (e.g., http://192.168.1.100:5000)

### Troubleshooting:
If it doesn't work, allow firewall:
```bash
netsh advfirewall firewall add rule name="Flask App" dir=in action=allow protocol=TCP localport=5000
```

---

## Option 2: React Native Mobile App (30 minutes)

### Step 1: Install Node.js
Download from: https://nodejs.org/

### Step 2: Install Expo CLI
```bash
npm install -g expo-cli
```

### Step 3: Install Expo Go on Phone
- iOS: https://apps.apple.com/app/expo-go/id982107779
- Android: https://play.google.com/store/apps/details?id=host.exp.exponent

### Step 4: Setup Mobile App
```bash
cd c:\Users\AJAI MUHAMMED\Desktop\dream\mobile-app
npm install
```

### Step 5: Update API URL in App.js
Open `mobile-app/App.js` and change line 6:
```javascript
const API_URL = 'http://YOUR_COMPUTER_IP:5000';
```
Replace `YOUR_COMPUTER_IP` with the IP shown when you run Flask app.

### Step 6: Start Flask Backend
```bash
cd c:\Users\AJAI MUHAMMED\Desktop\dream\dream
python app.py
```

### Step 7: Start Mobile App
```bash
cd c:\Users\AJAI MUHAMMED\Desktop\dream\mobile-app
npx expo start
```

### Step 8: Scan QR Code
- Open Expo Go app on phone
- Scan the QR code shown in terminal
- App will load on your phone

---

## Which Option to Choose?

**Option 3 (Quick):**
- ✅ Works immediately
- ✅ No installation needed
- ✅ Just open browser on phone
- ❌ Requires same WiFi
- ❌ Browser-based (not native app)

**Option 2 (Better):**
- ✅ Real mobile app experience
- ✅ Better performance
- ✅ Native UI/UX
- ❌ Requires Node.js installation
- ❌ Takes more time to setup

---

## Quick Start (Recommended)

1. Install flask-cors:
   ```bash
   pip install flask-cors
   ```

2. Start Flask:
   ```bash
   cd c:\Users\AJAI MUHAMMED\Desktop\dream\dream
   python app.py
   ```

3. Open on phone browser using the Network URL shown

Done! 🎉
