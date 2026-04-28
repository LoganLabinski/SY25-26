import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

BASE_URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Reuse connections for speed
session = requests.Session()
session.headers.update(HEADERS)


def get_soup(url):
    response = session.get(url)
    response.raise_for_status()

    # Use raw bytes for best Unicode handling
    return BeautifulSoup(response.content, "html.parser")


def get_book_details(book_url):
    try:
        soup = get_soup(book_url)
        genre_tag = soup.select_one('ul.breadcrumb li:nth-of-type(3) a')
        return genre_tag.text.strip() if genre_tag else "Unknown"
    except:
        return "Unknown"


def fetch_books(start_url):
    books = []
    url = start_url
    page_num = 1

    while url:
        print(f"\nScraping page {page_num}: {url}")
        soup = get_soup(url)

        articles = soup.select('article.product_pod')

        with ThreadPoolExecutor(max_workers=10) as executor:
            tasks = []

            for article in articles:
                title = article.h3.a['title']
                price = article.select_one('.price_color').text.strip()
                rating = article.p['class'][1]

                relative_link = article.h3.a['href']
                book_url = urljoin(url, relative_link)

                future = executor.submit(get_book_details, book_url)

                tasks.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "future": future
                })

            # Progress bar per page
            for task in tqdm(tasks, desc=f"Processing page {page_num}", leave=False):
                genre = task["future"].result()

                books.append({
                    "title": task["title"],
                    "price": task["price"],
                    "rating": task["rating"],
                    "genre": genre
                })

        # Handle pagination
        next_button = soup.select_one('li.next a')
        url = urljoin(url, next_button['href']) if next_button else None
        page_num += 1

    return books


def search_books(books, title=None, price=None, rating=None, genre=None):
    return [
        book for book in books
        if (not title or title.lower() in book['title'].lower())
        and (not price or price == book['price'])
        and (not rating or rating.lower() == book['rating'].lower())
        and (not genre or genre.lower() in book['genre'].lower())
    ]


def print_books(books):
    if not books:
        print("\nNo results found.")
        return

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

        title = input("Title: ").strip() or None
        price = input("Price (e.g., £53.74): ").strip() or None
        rating = input("Rating (e.g., Three, Five): ").strip() or None
        genre = input("Genre: ").strip() or None

        results = search_books(books, title, price, rating, genre)
        print_books(results)

    except Exception as e:
        print(f"Error: {e}")