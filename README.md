<img width="1833" height="972" alt="image" src="https://github.com/user-attachments/assets/2a8e89f4-8533-4ce2-a0ac-db45188d2045" />

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-4.0-green?style=for-the-badge&logo=selenium&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blue?style=for-the-badge&logo=telegram&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

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
   git clone https://github.com/Suyumm/Student-Grade-Automation-Bot.git cd Student-Grade-Automation-Bot
