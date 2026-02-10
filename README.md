# 🤖 Agentic AI: Automated Job Application Bot (Render Cloud)

An intelligent automation system designed to bridge the gap between aviation security and tech by automating LinkedIn job applications. This bot runs on **Render Cloud** and is triggered via **WhatsApp**, allowing for seamless career transitions while on the go.

## 🚀 Features

* **WhatsApp Integration**: Trigger job searches and receive status updates via Twilio.
* **Headless Automation**: Runs on a Dockerized Chrome environment on Render Cloud, removing local machine dependencies.
* **Intelligent Matching**: Analyzes job descriptions against specific professional criteria, including **M.Sc. Data Science**.
* **Persistent Logging**: Tracks applications in a SQLite database to avoid duplicate entries.

## 🛠️ Tech Stack

* **Language**: Python 3.13
* **Automation**: Selenium (Headless Chrome)
* **Server**: Flask
* **Messaging**: Twilio WhatsApp API
* **Cloud**: Render (Docker Runtime)

## 📂 Project Structure

* `whatsapp_server.py`: Flask entry point for WhatsApp webhooks.
* `browser_bot.py`: Selenium logic for cloud-based headless browsing and LinkedIn interaction.
* `main_app.py`: Core orchestration logic for job searching and application flow.
* `matcher.py`: Logic to evaluate job descriptions against candidate profile.
* `database.py`: Handles SQLite logging for application history.
* `dockerfile`: Defines the container environment with Chrome dependencies for Render.

## ⚙️ Setup & Deployment

### 1. Environment Variables

To run this project, you must set the following variables in your Render Dashboard (or local `.env`):

```text
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
OPENAI_API_KEY=your_key

```

### 2. GitHub Push

```bash
git add .
git commit -m "Deploying to Render Cloud"
git push origin main

```

### 3. Render Configuration

* Connect your GitHub repo to a new **Web Service**.
* Select **Docker** as the runtime.
* Add your secret environment variables under the **Environment** tab.

## 📈 About the Developer

**Gopi Borra** is a transition-focused professional with 5 years of experience in aviation security at **Quikjet Cargo Airlines**. Currently pursuing an **M.Sc. in Data Science** at Chandigarh University (9.00 SGPA), Gopi specializes in Python, SQL, and Agentic AI solutions.

---

