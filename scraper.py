import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

books = []

for book in soup.select("article.product_pod"):
    title = book.select_one("h3 a")["title"]
    price = book.select_one(".price_color").text
    rating = book.select_one("p.star-rating")["class"][1]
    
    books.append({
        "title": title,
        "price": price,
        "rating": rating
    })

with open("books.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "rating"])
    writer.writeheader()
    writer.writerows(books)

print(f"Scraped {len(books)} books and saved to CSV")