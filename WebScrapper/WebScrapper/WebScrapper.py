import requests
from bs4 import BeautifulSoup

# 1. The URL of the page we want to scrape
url = "https://www.dvusd.org/"

try:
    # 2. Send a GET request to the website
    response = requests.get(url)
    
    # 3. Parse the HTML content of the page
    # 'html.parser' is built into Python
    soup = BeautifulSoup(response.text, 'html.parser')

    # 4. Extract data
    # Get the page title
    print(f"Page Title: {soup.title.string}")
    print("-" * 20)

    # Find all 'a' tags (links) and print their destination
    print("Links found on page:")
    for link in soup.find_all('a'):
        href = link.get('href')
        text = link.text.strip()
        print(f"Text: {text} | URL: {href}")

except Exception as e:
    print(f"An error occurred: {e}")

