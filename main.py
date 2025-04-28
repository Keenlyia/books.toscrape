from manager import ProcessManager
from playwright.sync_api import sync_playwright
from scraper import BookScraper
import json

def collect_book_links():
    links = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://books.toscrape.com/catalogue/page-1.html')

        while True:
            book_elements = page.locator('h3 a')
            count = book_elements.count()
            print(f"Знайдено {count} книжок на сторінці")
            for i in range(count):
                link = book_elements.nth(i).get_attribute('href')
                print(link)
                if link.startswith('../'):
                    link = "https://books.toscrape.com/catalogue/" + link.replace('../', '')
                elif not link.startswith('http'):
                    link = "https://books.toscrape.com/catalogue/" + link
                links.append(link)

            next_button = page.locator('li.next a')
            if next_button.count() == 0:
                break
            next_page = next_button.get_attribute('href')
            page.goto("https://books.toscrape.com/catalogue/" + next_page)

        browser.close()
    return links

if __name__ == "__main__":
    urls = collect_book_links()
    scraper = BookScraper()
    books_data = []
    for url in urls:
        book_data = scraper.scrape_book(url)  # збираємо дані для кожного посилання
        if book_data:
            books_data.append(book_data)
            print(f"Назва книги: {book_data['title']}")
            print(f"Категорія: {book_data['category']}")
            print(f"Ціна: {book_data['price']}")
            print(f"Рейтинг: {book_data['rating']}")
            print(f"Наявність: {book_data['stock']}")
            print(f"URL зображення: {book_data['image_url']}")
            print(f"Опис: {book_data['description']}")
            print("\n" + "-"*50 + "\n")

    with open("./results/books_data.json", "w",
              encoding="utf-8") as f:
        json.dump(books_data, f,
                  ensure_ascii=False, indent=4)

    scraper.close()
    print("Всі дані успішно збережено в books_data.json")
