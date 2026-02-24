from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime
import logging
import pytz

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Discord webhook URL from environment variable
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

# Log configuration on startup
logger.info(f"Starting app...")
logger.info(f"PORT environment variable: {os.environ.get('PORT', 'NOT SET')}")
logger.info(f"Discord webhook configured: {'Yes' if DISCORD_WEBHOOK_URL else 'No'}")

def is_market_hours():
    """Check if current time is during market hours (6:30 AM - 1:00 PM PT, weekdays)"""
    pacific = pytz.timezone('America/Los_Angeles')
    now = datetime.now(pacific)
    
    # Check if it's a weekday (Monday=0, Sunday=6)
    if now.weekday() >= 5:  # Saturday or Sunday
        return False
    
    # Check if time is between 6:30 AM and 1:00 PM
    market_start = now.replace(hour=6, minute=30, second=0, microsecond=0)
    market_end = now.replace(hour=13, minute=0, second=0, microsecond=0)
    
    return market_start <= now <= market_end

@app.route('/')
def home():
    logger.info("Home route accessed")
    return "✅ TradingView to Discord Bridge is running!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    logger.info(f"Webhook accessed with method: {request.method}")
    
    # Handle GET requests (for testing in browser)
    if request.method == 'GET':
        return jsonify({
            "status": "webhook endpoint is active",
            "message": "Send POST request with alert data",
            "discord_configured": bool(DISCORD_WEBHOOK_URL)
        }), 200
    
    # Handle POST requests from TradingView
    logger.info("Webhook received")
    try:
        # Check if Discord webhook is configured
        if not DISCORD_WEBHOOK_URL:
            logger.error("Discord webhook URL not configured")
            return jsonify({"error": "Discord webhook URL not configured"}), 500
        
        # Get data from TradingView
        if request.is_json:
            alert_message = request.get_json()
        else:
            alert_message = request.data.decode('utf-8')
        
        logger.info(f"Received alert: {alert_message}")
        
        # Check if we're in market hours
        is_market_open = is_market_hours()
        logger.info(f"Market hours active: {is_market_open}")
        
        # Block alerts outside market hours
        if not is_market_open:
            logger.info("Alert blocked - outside market hours")
            return jsonify({"status": "blocked", "message": "Alert blocked - outside market hours (6:30 AM - 1:00 PM PT, weekdays only)"}), 200
        
        # Create Discord message with role ping (only runs during market hours now)
        discord_data = {
            "content": "<@&1460609951021007008>",  # Always ping during market hours
            "embeds": [{
                "title": "📊 TradingView Alert",
                "description": str(alert_message),
                "color": 3447003,  # Blue color
                "timestamp": datetime.utcnow().isoformat(),
                "footer": {
                    "text": "TradingView Alert"
                }
            }]
        }
        
        # Send to Discord
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=discord_data,
            headers={'Content-Type': 'application/json'}
        )
        
        logger.info(f"Discord response status: {response.status_code}")
        
        if response.status_code == 204:
            return jsonify({"status": "success", "message": "Alert sent to Discord"}), 200
        else:
            return jsonify({"error": f"Discord returned status {response.status_code}"}), 500
            
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500

# This is critical for Railway
if __name__ != '__main__':
    # Running under gunicorn
    logger.info("Running under gunicorn")
