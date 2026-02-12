from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# Discord webhook URL from environment variable
DISCORD_WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

@app.route('/')
def home():
    return "✅ TradingView to Discord Bridge is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Check if Discord webhook is configured
        if not DISCORD_WEBHOOK_URL:
            return jsonify({"error": "Discord webhook URL not configured"}), 500
        
        # Get data from TradingView
        if request.is_json:
            alert_message = request.get_json()
        else:
            alert_message = request.data.decode('utf-8')
        
        # Create Discord message
        discord_data = {
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
        
        if response.status_code == 204:
            return jsonify({"status": "success", "message": "Alert sent to Discord"}), 200
        else:
            return jsonify({"error": f"Discord returned status {response.status_code}"}), 500
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
