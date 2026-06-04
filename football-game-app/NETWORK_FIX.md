# Network Connection Fix

## Problem: Second phone can't connect

## Solutions (try in order):

### 1. Use Tunnel Mode (BEST FIX)
```bash
cd c:\Users\AJAI MUHAMMED\Desktop\dream\football-game-app
npx expo start --tunnel
```
This works even if phones are on different networks!

### 2. Check Same WiFi
- Both phones MUST be on the exact same WiFi network
- Not one on WiFi and one on mobile data
- Not different WiFi networks

### 3. Disable Windows Firewall temporarily
- Windows Security → Firewall → Turn off for Private networks
- Try connecting
- Turn back on after testing

### 4. Use LAN mode
```bash
npx expo start --lan
```

### 5. Install Expo Go on both phones
- Make sure both have latest Expo Go app
- Android: Play Store
- iOS: App Store

## Recommended: Always use tunnel mode
```bash
npx expo start --tunnel
```
Slower but works everywhere!
