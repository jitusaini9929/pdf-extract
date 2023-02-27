import winsound
import requests
from bs4 import BeautifulSoup
import time
import os
import telegram

# Set up Telegram bot
bot = telegram.Bot(token='6110984921:AAFoWvkX7avuoCTAYK1sDDtzAreXcTUwPGs')
chat_id = '505635797'

# Set up user-agent string
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/'
}


# Set up list of URLs to track
urls = ['https://rsmssb.rajasthan.gov.in/page?menuName=ApBuI6wdvnNKC6MoOgFsfXwFRsE7cKLr']

# Set up list of known PDF links
known_pdf_links = []

# Get list of already sent PDF links from file, if it exists
if os.path.isfile('known_pdf_links.txt'):
    with open('known_pdf_links.txt', 'r') as f:
        known_pdf_links = f.read().splitlines()

while True:
    try:
        for url in urls:
            # Send GET request to URL
            response = requests.get(url, headers=headers, timeout=5)

            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all <a> tags with href attribute
            links = soup.find_all('a', href=True)

            # Loop through links and check if they end in .pdf
            for link in links:
                href = link['href']
                if href.endswith('.pdf') and href not in known_pdf_links:
                    # Send Telegram notification with new PDF link
                    bot.send_message(chat_id=chat_id, text=f'New PDF link found: https://rsmssb.rajasthan.gov.in//{href}')

                    # Add new PDF link to list of known links
                    known_pdf_links.append(href)

            print(f'Successfully scraped {url}')
        
        # Save list of known PDF links to file
        with open('known_pdf_links.txt', 'w') as f:
            f.write('\n'.join(known_pdf_links))

    except requests.exceptions.RequestException as e:
         print(f'Getting Error {url}')

    time.sleep(120)  # Wait for 5 minutes before scraping again
