from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

URL = "https://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []

    for book in soup.select('article.product_pod'):
        title = book.h3.a['title']
        price = book.select_one('p.price_color').text
        availability = book.select_one('p.instock.availability').text.strip()
        
        books.append({
            'title': title,
            'price': price,
            'availability': availability
        })

    return books

@app.route('/')
def get_books():
    scraped_books = scrape_books(URL)
    return jsonify(scraped_books)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
