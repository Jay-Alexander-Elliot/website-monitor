import requests
from bs4 import BeautifulSoup
import difflib
import os
from twilio.rest import Client
import hashlib

# Twilio configuration
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
DESTINATION_PHONE_NUMBER = 'your_phone_number'

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_sms(message):
    client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=DESTINATION_PHONE_NUMBER)

def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.get_text()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def load_previous_content(url):
    filename = hashlib.md5(url.encode()).hexdigest()
    try:
        with open(f'previous_content/{filename}', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return None

def save_current_content(url, content):
    filename = hashlib.md5(url.encode()).hexdigest()
    with open(f'previous_content/{filename}', 'w') as file:
        file.write(content)

def compare_contents(old_content, new_content):
    return difflib.unified_diff(old_content.splitlines(), new_content.splitlines(), lineterm='')

# Load URLs from URLs.txt
with open('URLs.txt', 'r') as file:
    urls = [url.strip() for url in file.readlines()]

# Ensure previous_content directory exists
os.makedirs('previous_content', exist_ok=True)

# Main monitoring logic
for url in urls:
    print(f"Checking {url}")
    new_content = fetch_website_content(url)
    if new_content:
        old_content = load_previous_content(url)
        if old_content:
            differences = compare_contents(old_content, new_content)
            if sum(1 for _ in differences) > 0:  # Change detected
                print(f"Change detected in {url}")
                send_sms(f"Website changed: {url}")
        save_current_content(url, new_content)
    else:
        print(f"Unable to fetch content for {url}")

print("Monitoring complete.")
