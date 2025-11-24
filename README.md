# 🎓 Student Grade Automation Bot

A Python automation script that periodically checks your Student Information System (OIS/OBS) for new exam grades and sends instant notifications via Telegram.

## 🚀 Features

- **Automated Login:** Uses Selenium to log in to the student portal.
- **Smart Monitoring:** Checks for grades every 30 minutes.
- **Instant Notifications:** Sends a Telegram message as soon as a grade is announced.
- **Diff Checking:** Compares old data with new data; only notifies you about *changes*.
- **First Run Silence:** Does not spam you with all existing grades on the first run.

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/Suyumm/Student-Grade-Automation-Bot.git](https://github.com/Suyumm/Student-Grade-Automation-Bot.git)
   cd Student-Grade-Automation-Bot
