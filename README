# Myslytsia ChatBot

Telegram bot developed for **Myslytsia**, a Ukrainian volunteering organization that promotes critical thinking among youth.

---

## Project Overview

* **Project Name:** Myslytsia ChatBot
* **Organization:** Myslytsia
* **Role:** Developer
* **Period:** July 8, 2025 – Present

This bot automates application collection and delivers interactive critical thinking tests via Telegram.

---

## Features

### Application System

* Interactive multi-step application form
* Collects:

  * Name
  * Contact (phone/email)
  * Comment/message
* Stores data directly in **Google Sheets**
* Uses secure Google Service Account authentication

### Testing System

#### 1. Basic Test (`/test`)

* 3-question quiz
* Yes/No format via inline buttons
* Instant feedback with correctness indicators (✅ / ❌)

#### 2. Critical Thinking Test (`/critical`)

* 5-question quiz
* “Fake or True” evaluation
* Score-based results
* Detailed feedback:

  * User answer
  * Correct answer
  * Explanation-style output

### Interactive UX

* Inline keyboard buttons (Telegram UI)
* Step-by-step conversations using `ConversationHandler`
* Clean and intuitive chat flow

---

## Tech Stack

* **Language:** Python
* **Frameworks/Libraries:**

  * `python-telegram-bot` (async)
  * `gspread` (Google Sheets integration)
  * `google-auth` (service account authentication)

---

## Architecture

* Conversation-based state management
* User session data stored in `context.user_data`
* Google Sheets used as a lightweight database
* Environment-based configuration for credentials

---

## Project Structure

```id="qf8p9z"
.
├── bot.py               # Main bot logic
├── creds.json           # Generated from env (DO NOT COMMIT)
├── requirements.txt     # Dependencies
├── Dockerfile           # Container setup (optional)
└── README.md            # Documentation
```

---

## Setup & Installation

### 1. Clone the repository

```bash id="j2l4dp"
git clone https://github.com/your-username/myslytsia-chatbot.git
cd myslytsia-chatbot
```

### 2. Install dependencies

```bash id="z4x9qs"
pip install -r requirements.txt
```

### 3. Configure environment variables

#### Telegram Bot Token

```bash id="c2a7w1"
export TOKEN=your_telegram_bot_token
```

#### Google Credentials

Store your **Google Service Account JSON** as a string:

```bash id="0m3lqk"
export GOOGLE_CREDS_JSON='{"type": "...", "project_id": "...", ...}'
```

---

## Running the Bot

```bash id="a91dke"
python bot.py
```

---

## Google Sheets Integration

* Uses `gspread` to connect to Google Sheets
* Data is appended using:

```python
sheet.append_row([...])
```

### Requirements:

* Enable Google Sheets API
* Share the spreadsheet with your service account email
* Use the spreadsheet key:

```
1EQq7u8BaqboIdgS7E5c0vj0fLQLO-UtbPpdESF9ojyY
```

---

## 💬 Bot Commands

| Command     | Description                   |
| ----------- | ----------------------------- |
| `/start`    | Start the bot                 |
| `/apply`    | Submit an application         |
| `/test`     | Take a basic test             |
| `/critical` | Take a critical thinking test |
| `/cancel`   | Cancel current process        |

---

## Environment Variables

| Variable            | Description                        |
| ------------------- | ---------------------------------- |
| `TOKEN`             | Telegram Bot API token             |
| `GOOGLE_CREDS_JSON` | Google service account credentials |

---

## Future Improvements

* Admin panel for reviewing applications
* Persistent database (PostgreSQL / Firebase)
* Advanced scoring analytics
* Multi-language support (UA / EN)
* Export results dashboard

---

## Security Notes

* Never commit `creds.json` to GitHub
* Store credentials only in environment variables
* Restrict access to your Google Sheet


---

## License

MIT License

---

## Acknowledgments

Special thanks to the Myslytsia team for their mission to empower youth through critical thinking.
