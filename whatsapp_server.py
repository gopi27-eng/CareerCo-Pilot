import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import threading
from main_app import run_automation

app = Flask(__name__)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if "start search" in incoming_msg:
        # Trigger automation in background
        thread = threading.Thread(target=run_automation)
        thread.start()
        msg.body("🚀 Render Cloud: Job search initiated! I will update you via WhatsApp once applications are processed.")
    else:
        msg.body("Hi Gopi! Send 'start search' to begin the automated application process on Render.")

    return str(resp)

if __name__ == "__main__":
    # Render provides the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)