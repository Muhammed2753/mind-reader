# Complete APK Build Guide

## Method 1: EAS Build (Recommended)

### Step 1: Fix the error
```bash
cd c:\Users\AJAI MUHAMMED\Desktop\dream\mobile-app

# Delete and reinstall
rmdir /s /q node_modules
npm install
```

### Step 2: Add to .gitignore
Create/edit `.gitignore`:
```
node_modules/
.expo/
dist/
npm-debug.*
*.jks
*.p8
*.p12
*.key
*.mobileprovision
*.orig.*
web-build/
```

### Step 3: Commit changes
```bash
git add .
git commit -m "Fix build"
```

### Step 4: Build APK
```bash
eas build --platform android --profile preview
```

Wait 10-20 minutes. You'll get a download link!

## Method 2: Local Build (Faster)

```bash
# Install Android Studio first
# Then:
eas build --platform android --profile preview --local
```

## Method 3: Expo Classic Build (Easiest)

```bash
# Update app.json
# Add:
{
  "expo": {
    "android": {
      "package": "com.yourname.footballgame"
    }
  }
}

# Then build
expo build:android
```

## After Build Completes:

1. Download APK from link
2. Send APK file to friends
3. Friends install APK
4. No Expo Go needed!

## Quick Share Method (No Build):

```bash
# Just use tunnel mode
npx expo start --tunnel
```

Share QR code - works instantly!
