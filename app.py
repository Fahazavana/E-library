from flask import Flask, request, render_template, url_for, redirect, send_file
from flask_sqlalchemy import SQLAlchemy  # Database
from flask_migrate import Migrate  # handle migration
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask_wtf import CSRFProtect
from io import BytesIO


app = Flask(__name__)
# Database setting /// for relative path
app.config['UPLOAD_FOLDER'] = "./media"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
db = SQLAlchemy(app)
app.secret_key = b'_53oi3uriq9pifpff;apl'
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# A model


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary)
    year = db.Column(db.String(4))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Book %r>' % self.id


# @app.route('/')
# def index():
#     return "<h1>Hello world</h1>"

@app.route('/')
def index():
    return render_template('index.html', books=Book.query.all())

# CREATE


@app.route('/addbook', methods=['GET', 'POST'])
def addBook():
    if request.method == "POST":
        title = request.form['title']
        file = request.files['file']
        year = request.form['year']
        author = request.form['author']
        book = Book(title=title, filename='',
                    data=file.read(), author=author, year=year)
        db.session.add(book)
        db.session.commit()
        id = book.id
        filename = secure_filename(str(id)+file.filename)
        book.filename = filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        db.session.commit()
    return redirect(url_for('index'))

# DOWNLOAD
@app.route('/delete/<int:pk>')
def delete(pk):
    book = Book.query.filter_by(id=pk).first()
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], book.filename))
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:pk>', methods=['GET','POST'])
def updateBook(pk):
    book = Book.query.get_or_404(pk)
    if book:
        if request.method == "POST":
            book.title = request.form['title']
            book.year = request.form['year']
            book.author = request.form['author']
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return render_template('update.html', book=book)
    else:
        return "Book not found"
    
@app.route('/<int:pk>')
def download(pk):
    print(pk)
    book = Book.query.filter_by(id=pk).first()
    print(book)
    return send_file(BytesIO(book.data),
                     download_name=book.filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
