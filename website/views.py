from os import link
from flask import Blueprint, render_template, request
from flask.helpers import url_for
from flask_login import login_required, current_user
import requests
from requests.api import get
from werkzeug.utils import redirect
from .book_scraping import get_books, categories
from . import db
from .models import Book

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('views.top_books', categorie='Alle Kategorien'))

    return render_template("home.html", user=current_user)



@views.route('/top-books/<categorie>', methods=['GET', 'POST'])
@login_required
def top_books(categorie='Alle Kategorien'):
    if request.method == 'POST':
        if request.form.get('add'):
            book = request.form.get('add')
            title, author, link, image = book.split('\n')
            if not Book.query.filter_by(user_id=current_user.get_id(), title=title).first():
                new_book = Book(title=title,author=author,link=link,image=image,user_id=current_user.get_id())
                db.session.add(new_book)
                db.session.commit()

            return redirect(url_for('views.top_books', categorie=categorie))
    else:
        if request.args.get('categorie'):
            categorie = request.args.get('categorie')
            return redirect(url_for('views.top_books', categorie=categorie))
    
        return render_template("top_books.html", user=current_user, books=get_books(categories[categorie]), categories=categories.keys(), categorie=categorie)
    
            
        



@views.route('/my-books', methods=['GET', 'POST'])
@login_required
def my_books():
    books = Book.query.filter_by(user_id=current_user.get_id())

    if request.method == 'POST':
        id = request.form.get('del')
        Book.query.filter_by(id=id).delete()
        db.session.commit()

        return redirect(url_for('views.my_books'))

    return render_template("my_books.html", user=current_user, books=books)
