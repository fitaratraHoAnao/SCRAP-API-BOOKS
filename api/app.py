from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

BASE_URL = "https://books.toscrape.com/"

def scrape_books(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    books = []

    for book in soup.select('article.product_pod'):
        title = book.h3.a['title']
        price = book.select_one('p.price_color').text
        availability = book.select_one('p.instock.availability').text.strip()

        # Définit une catégorie par défaut, car la page principale n'en a pas
        category = 'General'

        books.append({
            'title': title,
            'price': price,
            'availability': availability,
            'category': category
        })

    return books

@app.route('/books')
def get_books():
    page = request.args.get('page', default=1, type=int)
    url = f"{BASE_URL}catalogue/page-{page}.html"
    scraped_books = scrape_books(url)
    return jsonify(scraped_books)

@app.route('/books/search')
def search_books():
    query = request.args.get('q', default='', type=str)
    books = scrape_books(BASE_URL)
    filtered_books = [book for book in books if query.lower() in book['title'].lower()]
    return jsonify(filtered_books)

@app.route('/books/category/<category>')
def books_by_category(category):
    url = f"{BASE_URL}catalogue/category/books/{category}/index.html"
    books = scrape_books(url)
    return jsonify(books)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
