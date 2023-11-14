from flask import request, jsonify
from models import db, Book

def postBook():
    try:
        data = request.json

        title = data.get('title')
        author = data.get('author')
        genre = data.get('genre')
        publication_year = data.get('publication_year')

        new_book = Book(title=title, author=author, genre=genre, publication_year=publication_year)

        db.session.add(new_book)
        db.session.commit()

        return jsonify({"message": "Book created successfully", "data": {"title": new_book.title, "author": new_book.author}}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def getBooks():
    all_books = Book.query.all()
    books_list = []
    for book in all_books:
        books_list.append({
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'publication_year': book.publication_year,
        })

    return jsonify({'all_books': books_list})

def getBook(book_id):
    book = Book.query.get(book_id)

    if book is not None:
        book_info = {
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'publication_year': book.publication_year,
        }
        return jsonify({'book': book_info})
    else:
        return jsonify({'error': 'Book not found'}), 500
    
def searchBookByTitle(search_word):
    filtered_books = Book.query.filter(Book.title.like(f"%{search_word}%")).all()
    books_list = []

    for book in filtered_books:
        books_list.append({
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'publication_year': book.publication_year,
        })
    
    return jsonify({'all_books': books_list})

def searchBookByAuthor(search_word):
    filtered_books = Book.query.filter(Book.author.like(f"%{search_word}%")).all()
    books_list = []

    for book in filtered_books:
        books_list.append({
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'publication_year': book.publication_year,
        })
    
    return jsonify({'all_books': books_list})

def searchBookByGenre(search_word):
    filtered_books = Book.query.filter(Book.genre.like(f"%{search_word}%")).all()
    books_list = []

    for book in filtered_books:
        books_list.append({
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'publication_year': book.publication_year,
        })
    
    return jsonify({'all_books': books_list})

    
    