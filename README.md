[README.md](https://github.com/user-attachments/files/25271280/README.md)
# TradingView to Discord Alert Bridge

This service receives webhooks from TradingView and forwards them to your Discord channel.

## Setup Instructions

### 1. Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Sign up/login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Upload these files to a GitHub repository first, OR use "Empty Service"
5. If using Empty Service:
   - Click "New" → "Empty Service"
   - Go to Settings → Connect to GitHub repo (after creating one)

### 2. Configure Environment Variable

In Railway dashboard:
1. Click on your service
2. Go to "Variables" tab
3. Add new variable:
   - Name: `DISCORD_WEBHOOK_URL`
   - Value: Your Discord webhook URL (from Discord channel settings)

### 3. Deploy

Railway will automatically deploy your service. Wait for it to finish.

### 4. Get Your Webhook URL

1. In Railway, go to "Settings" tab
2. Click "Generate Domain" under "Networking"
3. Copy the domain (e.g., `your-app.railway.app`)
4. Your webhook URL will be: `https://your-app.railway.app/webhook`

### 5. Configure TradingView

1. Create an alert in TradingView
2. In alert settings, go to "Notifications" tab
3. Check "Webhook URL"
4. Paste: `https://your-app.railway.app/webhook`
5. In the "Message" field, write whatever you want to see in Discord
6. Save the alert

## Testing

Visit `https://your-app.railway.app/` in your browser - you should see:
"✅ TradingView to Discord Bridge is running!"

## Message Format

The alert message you type in TradingView will appear in Discord as an embedded message with:
- Blue sidebar
- Timestamp
- Your custom message

## Troubleshooting

- **Not receiving alerts**: Check Railway logs for errors
- **Discord webhook error**: Verify your webhook URL in Railway variables
- **Deploy failed**: Check that all files are uploaded correctly
