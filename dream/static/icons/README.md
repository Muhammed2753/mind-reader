# 🎨 App Icons for Muhfal

## Required Icons:
- icon-192.png (192x192 pixels)
- icon-512.png (512x512 pixels)

## Quick Icon Creation:

### Option 1: Online Generator
1. Go to: https://favicon.io/favicon-generator/
2. Text: "⚽"
3. Background: #5bc0be (teal)
4. Font: Bold
5. Download and rename files

### Option 2: Canva
1. Go to: https://canva.com/
2. Create 512x512 design
3. Add football emoji ⚽
4. Background: gradient blue to teal
5. Export as PNG
6. Resize to 192x192 for smaller version

### Option 3: Use Emoji
Create simple HTML file and screenshot:

```html
<!DOCTYPE html>
<html>
<head>
<style>
body {
  width: 512px;
  height: 512px;
  background: linear-gradient(135deg, #5bc0be, #3a506b);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 300px;
  margin: 0;
}
</style>
</head>
<body>⚽</body>
</html>
```

Save as icon.html, open in browser, screenshot, and crop to 512x512.

## Placement:
Put icons in: `dream/static/icons/`
- icon-192.png
- icon-512.png

## Alternative:
If you don't have icons, the APK will use default browser icon. The app will still work perfectly!