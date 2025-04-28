from playwright.sync_api import sync_playwright

class BookScraper:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()

    def scrape_book(self, url):
        try:
            self.page.goto(url)
        except Exception as e:
            print(f"Помилка при переході на {url}: {e}")
            return None

        try:
            title = self.page.locator("//h1").text_content()
        except AttributeError:
            title = None

        try:
            category = self.page.locator("//ul[@class='breadcrumb']/li[3]/a").text_content()
        except AttributeError:
            category = None

        try:
            price = self.page.locator("//p[@class='price_color']").first.text_content()
        except AttributeError:
            price = None

        try:
            rating = self.page.locator('p.star-rating').first.get_attribute('class').replace('star-rating', '').strip()
        except AttributeError:
            rating = None

        try:
            stock = self.page.locator('.instock.availability').first.text_content().strip()
        except AttributeError:
            stock = None

        try:
            image_url = self.page.locator('.item img').get_attribute('src')
        except AttributeError:
            image_url = None

        if image_url.startswith('../'):
            image_url = "https://books.toscrape.com/" + image_url.replace('../', '')

        try:
            description = self.page.locator('#product_description ~ p').text_content()
        except:
            description = "No description available."

        book_data = {
            "title": title,
            "category": category,
            "price": price,
            "rating": rating,
            "stock": stock,
            "image_url": image_url,
            "description": description,
        }

        return book_data

    def close(self):
        self.browser.close()
        self.playwright.stop()


if __name__ == "__main__":
    scraper.close()
