# Share Your Game with Anyone

## Method 1: Tunnel Mode (Instant)
```bash
cd c:\Users\AJAI MUHAMMED\Desktop\dream\football-game-app
npx expo start --tunnel
```
- Share QR code screenshot
- Friend scans with Expo Go
- Works worldwide!

## Method 2: Expo Publish (Permanent Link)
```bash
# 1. Create Expo account at expo.dev
# 2. Login
npx expo login

# 3. Publish
npx expo publish

# You'll get a link like:
# exp://exp.host/@yourname/football-game-app
```
Share this link with anyone!

## Method 3: Build APK (Android Only)
```bash
# 1. Install EAS CLI
npm install -g eas-cli

# 2. Login
eas login

# 3. Configure
eas build:configure

# 4. Build APK
eas build --platform android --profile preview
```
Download APK and share the file!

## Method 4: Web Version (Browser)
```bash
# 1. Build for web
npx expo export:web

# 2. Deploy to Netlify
# - Go to netlify.com
# - Drag & drop the 'web-build' folder
# - Get shareable link!
```

## Recommended: Use Tunnel Mode
Fastest and easiest for testing with friends!

```bash
npx expo start --tunnel
```

Then send them:
1. QR code screenshot
2. Tell them to download "Expo Go" app
3. Scan QR code
4. Play!
