# 🤖 AeroApplied: Automated Job Application Bot (Render Cloud)

An intelligent automation system designed to bridge the gap between aviation security and tech by automating LinkedIn job applications. This bot runs on **Render Cloud** and is triggered via **WhatsApp**, allowing for seamless career transitions while on the go.

## 🚀 Features

* **WhatsApp Integration**: Trigger job searches and receive status updates via Twilio.
* **Headless Automation**: Runs on a Dockerized Chrome environment on Render Cloud, removing local machine dependencies.
* **Intelligent Matching**: Analyzes job descriptions against specific professional criteria, including **M.Sc. Data Science**.
* **Persistent Logging**: Tracks applications in a SQLite database to avoid duplicate entries.
* **Production Ready**: Uses Gunicorn WSGI server for reliable cloud deployment.

## 🛠️ Tech Stack

* **Language**: Python 3.13
* **Automation**: Selenium (Headless Chrome)
* **Server**: Flask + Gunicorn
* **Messaging**: Twilio WhatsApp API
* **Cloud**: Render (Docker Runtime)

## 📂 Project Structure

* `whatsapp_server.py`: Flask entry point for WhatsApp webhooks with health check endpoint.
* `browser_bot.py`: Selenium logic for cloud-based headless browsing and LinkedIn interaction.
* `main_app.py`: Core orchestration logic for job searching and application flow.
* `matcher.py`: Logic to evaluate job descriptions against candidate profile.
* `database.py`: Handles SQLite logging for application history.
* `dockerfile`: Defines the container environment with Chrome dependencies for Render.
* `Procfile`: Specifies production server startup command.

## ⚙️ Setup & Deployment

### 1. Environment Variables

Set these in your Render Dashboard under **Environment** tab (never commit these to GitHub):

```
LINKEDIN_EMAIL=your_actual_email@example.com
LINKEDIN_PASSWORD=your_actual_password
TWILIO_ACCOUNT_SID=your_actual_sid
TWILIO_AUTH_TOKEN=your_actual_token
OPENAI_API_KEY=your_actual_key
```

### 2. Deploy to Render

```bash
git add .
git commit -m "Deploy with health check and gunicorn"
git push origin main
```

### 3. Render Configuration

1. Connect your GitHub repo to a new **Web Service** on Render
2. Select **Docker** as the runtime
3. Add environment variables (see step 1)
4. Deploy!

### 4. Configure Twilio Webhook

In your Twilio Console:
1. Go to your WhatsApp Sandbox settings
2. Set the webhook URL to: `https://job-bot-server.onrender.com/whatsapp`
3. Save configuration

### 5. Test Your Bot

Send a WhatsApp message to your Twilio number:
```
start search
```

You should receive: "🚀 AeroApplied AI: Search started on Render! I will notify you once applications are logged."

## 🔍 Endpoints

* `GET /` - Health check (returns 200 OK)
* `POST /whatsapp` - Twilio webhook for incoming WhatsApp messages

## 🐛 Troubleshooting

**404 Errors**: The root endpoint now returns 200 OK for health checks.

**Server not responding**: Check Render logs to verify gunicorn started successfully.

**WhatsApp not triggering**: Verify your Twilio webhook URL is correct and environment variables are set.

## 📈 About the Developer

**Gopi Borra** is a transition-focused professional with 5 years of experience in aviation security at **Quikjet Cargo Airlines**. Currently pursuing an **M.Sc. in Data Science** at Chandigarh University (9.00 SGPA), Gopi specializes in Python, SQL, and Agentic AI solutions.

---

**Status**: ✅ Production-ready deployment on Render Cloud
