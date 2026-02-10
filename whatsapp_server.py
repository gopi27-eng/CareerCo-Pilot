import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import threading
from main_app import run_automation

app = Flask(__name__)

# Health check endpoint for Render
@app.route("/", methods=['GET', 'HEAD'])
def health_check():
    """Render pings this endpoint to verify the service is running"""
    return "🤖 AeroApplied Job Bot - Status: Online", 200

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower().strip()
    print(f"📩 DEBUG: Received from WhatsApp: '{incoming_msg}'")
    
    resp = MessagingResponse()
    
    if "start search" in incoming_msg:
        try:
            # Threading ensures Gopi gets an instant reply while bot works in background
            thread = threading.Thread(target=run_automation)
            thread.daemon = True # Allows server to shut down properly
            thread.start()
            
            resp.message("🚀 AeroApplied AI: Search started on Render! I will notify you once applications are logged.")
            print("✅ DEBUG: Confirmation sent to Twilio.")
        except Exception as e:
            print(f"❌ DEBUG: Thread Error: {e}")
            resp.message(f"⚠️ System Error: {e}")
    else:
        resp.message("Hi Gopi! Send 'start search' to begin the job hunt.")

    return str(resp)

if __name__ == "__main__":
    # Render uses port 10000 by default
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)