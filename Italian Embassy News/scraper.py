# Script used to scrape news from the Italian Embassy in Buenos Aires and send an email with the latest news titles. The script uses BeautifulSoup for web scraping and smtplib for sending emails. Make sure to set your email password in the environment variable "EMAIL_PASSWORD" before running the script.
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

NEWS_URL = "https://ambbuenosaires.esteri.it/es/news/"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
# Tell Python to pull the password securely from GitHub's secret vault
SENDER_PASSWORD = os.environ.get("EMAIL_PASSWORD") 
RECEIVER_EMAIL = "your_email@gmail.com"

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def check_news():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(NEWS_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        title_elements = soup.find_all('h5')
        
        if not title_elements:
            return

        email_body = f"Latest news from the Italian Embassy in Buenos Aires ({datetime.now().strftime('%Y-%m-%d')}):\n\n"
        for i, element in enumerate(title_elements, start=1):
            link = element.find('a')
            if link:
                email_body += f"{i}. {link.get_text(strip=True)}\n"
        
        send_email(f"Embassy News Update - {datetime.now().strftime('%d/%m/%Y')}", email_body)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_news()