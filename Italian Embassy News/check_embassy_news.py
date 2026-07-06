import requests
from bs4 import BeautifulSoup
import schedule
import time
from datetime import datetime

# The URL of the news section
NEWS_URL = "https://ambbuenosaires.esteri.it/es/news/"

def get_news_titles():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Checking for news updates...")
    
    # Use a standard User-Agent so the website doesn't block the request as a basic bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        # Fetch the webpage
        response = requests.get(NEWS_URL, headers=headers, timeout=10)
        response.raise_for_status()  # Check if the request was successful
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # On this specific site, news titles are inside <h5> tags, wrapped in an <a> tag.
        # We will find all <h5> tags and extract the text from the links inside them.
        title_elements = soup.find_all('h5')
        
        if not title_elements:
            print("No titles found. The webpage structure might have changed.")
            return

        print("\n--- LATEST NEWS TITLES ---")
        for i, element in enumerate(title_elements, start=1):
            link = element.find('a')
            if link:
                # Extract the text and remove leading/trailing whitespace
                title = link.get_text(strip=True)
                print(f"{i}. {title}")
        print("--------------------------\n")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")

# --- Scheduling ---

# Run the function once immediately
get_news_titles()
# Schedule the script to run regularly
# Run it at a specific time every day:
schedule.every().day.at("10:00").do(get_news_titles)

print("Scheduler is running. Press Ctrl+C to stop.")

