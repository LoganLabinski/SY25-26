import requests
from bs4 import BeautifulSoup

# 1. The URL of the page we want to scrape
url = "https://books.toscrape.com/"

def fetch_books(url):
    response = requests.get(url)
    # Explicitly set the encoding to handle non-UTF-8 characters
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    books = []
    for article in soup.select('article.product_pod'):
        title = article.h3.a['title']
        price = article.find('p', class_='price_color').text.strip()
        rating = article.p['class'][1]  # e.g., 'Three'
        # Genre is not directly on the book, so we get it from breadcrumb
        genre = soup.select_one('ul.breadcrumb li:nth-of-type(3) a')
        genre = genre.text.strip() if genre else "All"
        books.append({
            'title': title,
            'price': price,
            'rating': rating,
            'genre': genre
        })
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
        books = fetch_books(url)
        print("Book Search Engine")
        print("Enter search criteria (leave blank to skip):")
        title = input("Title: ")
        price = input("Price (e.g., \u00A353.74): ")  # Unicode escape for £
        rating = input("Rating (e.g., Three, Five): ")
        genre = input("Genre: ")

        # Handle all unicode input
        title = title.strip() if title else None
        price = price.strip() if price else None
        rating = rating.strip() if rating else None
        genre = genre.strip() if genre else None

        results = search_books(books, title, price, rating, genre)
        print(f"\nFound {len(results)} book(s):\n")
        print_books(results)
    except Exception as e:
        print(f"An error occurred: {e}")
