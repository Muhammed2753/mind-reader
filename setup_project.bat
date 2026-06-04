@echo off
echo Creating Football Game Project Structure...

cd /d c:\Users\AJAI MUHAMMED\Desktop\dream

echo Creating main directories...
mkdir football-game-app 2>nul
cd football-game-app

mkdir src 2>nul
mkdir src\components 2>nul
mkdir src\screens 2>nul
mkdir src\services 2>nul
mkdir src\utils 2>nul
mkdir src\data 2>nul
mkdir src\assets 2>nul
mkdir src\assets\sounds 2>nul
mkdir src\assets\images 2>nul

echo Project structure created successfully!
echo.
echo Next steps:
echo 1. Run: npx create-expo-app . --template blank
echo 2. Install dependencies: npm install
echo.
pause
