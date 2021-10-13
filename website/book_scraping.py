from bs4 import BeautifulSoup
from selenium import webdriver
import requests

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.37'}


def get_categories():
    while 1:
        try:
            html_text = requests.get('https://www.amazon.de/gp/bestsellers/books/', headers=headers).content
            souper = BeautifulSoup(html_text, 'lxml')
            categories_text = souper.find(id='zg_browseRoot').find('ul').find_all('a')
        except:
            pass
        else:
            break
    categories = dict()

    categories['Alle Kategorien'] = 'https://www.amazon.de/gp/bestsellers/books/'

    for categorie_text in categories_text:
        categories[' '.join(categorie_text.text.split())] = categorie_text.get('href')

    return categories

def get_books(url):
    while 1:
        try:
            books_text = requests.get(url, headers=headers).content
            soup = BeautifulSoup(books_text, 'lxml')
            books = soup.find(id='zg-ordered-list').find_all('li', limit=30)
        except:
            pass
        else:
            break
    
    book_item_list = []

    for book in books:
        book = book.find('a')
        
        title = book.contents[2].text.strip()
        
        author = book.find_next_sibling('div').contents[0]
        if(author != '\n'):
            author = author.text.strip()
        else: 
            author = 'No Author'
            
        image = book.find('img').get('src')
        
        link = 'https://www.amazon.de' + book.get('href')
        
        book_item = {'title': title, 'author': author, 'image': image, 'link': link}
        book_item_list.append(book_item)
        
    return book_item_list


categories = get_categories()