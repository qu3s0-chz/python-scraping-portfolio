import requests
from bs4 import BeautifulSoup
import csv

base_url = "http://books.toscrape.com/catalogue/page-{}.html"
all_books = []

for page_num in range(1, 6):
    url = base_url.format(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    for book in soup.select("article.product_pod"):
        title = book.select_one("h3 a")["title"]
        price = book.select_one(".price_color").text
        rating = book.select_one("p.star-rating")["class"][1]
        
        all_books.append({
            "title": title,
            "price": price,
            "rating": rating
        })
    
    print(f"Page {page_num} scraped — {len(all_books)} total so far")

with open("all_books.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
    writer.writeheader()
    writer.writerows(all_books)

print(f"Done. {len(all_books)} books saved.")