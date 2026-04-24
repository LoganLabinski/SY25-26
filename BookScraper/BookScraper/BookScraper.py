import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

BASE_URL = "https://books.toscrape.com/"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = response.apparent_encoding
    return BeautifulSoup(response.text, 'html.parser')

def fetch_books(start_url):
    books = []
    url = start_url

    while url:
        print(f"Scraping page: {url}")
        soup = get_soup(url)

        for article in soup.select('article.product_pod'):
            title = article.h3.a['title']
            price = article.find('p', class_='price_color').text.strip()
            rating = article.p['class'][1]

            # Get book detail URL
            relative_link = article.h3.a['href']
            book_url = urljoin(url, relative_link)

            # Fetch detail page with SAME encoding handling
            book_soup = get_soup(book_url)

            genre_tag = book_soup.select_one('ul.breadcrumb li:nth-of-type(3) a')
            genre = genre_tag.text.strip() if genre_tag else "Unknown"

            books.append({
                'title': title,
                'price': price,
                'rating': rating,
                'genre': genre
            })

            time.sleep(0.2)  # polite delay

        # Handle pagination
        next_button = soup.select_one('li.next a')
        if next_button:
            url = urljoin(url, next_button['href'])
        else:
            url = None

    return books


def search_books(books, title=None, price=None, rating=None, genre=None):
    results = []
    for book in books:
        if title and title.lower() not in book['title'].lower():
            continue
        if price and price != book['price']:
            continue
        if rating and rating.lower() != book['rating'].lower():
            continue
        if genre and genre.lower() not in book['genre'].lower():
            continue
        results.append(book)
    return results


def print_books(books):
    for book in books:
        print(f"Title: {book['title']}")
        print(f"Price: {book['price']}")
        print(f"Rating: {book['rating']}")
        print(f"Genre: {book['genre']}")
        print("-" * 40)


if __name__ == "__main__":
    try:
        books = fetch_books(BASE_URL)

        print("\nBook Search Engine")
        print("Enter search criteria (leave blank to skip):")

        title = input("Title: ")
        price = input("Price (e.g., \u00A353.74): ")
        rating = input("Rating (e.g., Three, Five): ")
        genre = input("Genre: ")

        title = title.strip() if title else None
        price = price.strip() if price else None
        rating = rating.strip() if rating else None
        genre = genre.strip() if genre else None

        results = search_books(books, title, price, rating, genre)

        print(f"\nFound {len(results)} book(s):\n")
        print_books(results)

    except Exception as e:
        print(f"An error occurred: {e}")