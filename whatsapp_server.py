import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import threading
from main_app import run_automation

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    """
    Handles incoming WhatsApp messages from Twilio.
    Triggers Gopi's Data Science job search in the background.
    """
    # 1. Capture and log the incoming message for Render Logs
    incoming_msg = request.values.get('Body', '').lower().strip()
    print(f"📩 DEBUG: Received WhatsApp message: '{incoming_msg}'")
    
    resp = MessagingResponse()
    
    if "start search" in incoming_msg:
        print("🤖 DEBUG: Triggering 'run_automation' thread...")
        try:
            # 2. Start automation in a background thread to prevent timeout
            thread = threading.Thread(target=run_automation)
            thread.start()
            
            # 3. Send confirmation back to Gopi's phone
            resp.message("🚀 AeroApplied AI: Search initiated on Render! I will notify you once applications are processed.")
            print("✅ DEBUG: Twilio response generated.")
        except Exception as e:
            print(f"❌ DEBUG: Thread Error: {e}")
            resp.message(f"⚠️ System Error: {e}")
    else:
        print(f"❓ DEBUG: Unknown command received: {incoming_msg}")
        resp.message("Hi Gopi! Send 'start search' to begin the automated job application process.")

    return str(resp)

if __name__ == "__main__":
    # Render's default port is 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)