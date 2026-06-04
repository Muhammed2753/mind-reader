# Access Flask App from Phone

## Steps:

1. **Start the Flask app:**
   ```bash
   cd c:\Users\AJAI MUHAMMED\Desktop\dream\dream
   python app.py
   ```

2. **Find your IP address** (shown in terminal output)

3. **On your phone:**
   - Connect to the SAME WiFi network as your computer
   - Open browser (Chrome/Safari)
   - Enter: `http://YOUR_IP_ADDRESS:5000`
   - Example: `http://192.168.1.100:5000`

4. **Troubleshooting:**
   - Make sure Windows Firewall allows port 5000
   - Both devices must be on same WiFi
   - Use the Network IP shown in terminal, not localhost

## Allow Firewall (if blocked):
```bash
netsh advfirewall firewall add rule name="Flask App" dir=in action=allow protocol=TCP localport=5000
```
