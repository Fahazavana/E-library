from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy  # Database
from datetime import datetime

app = Flask(__name__)
# Database setting /// for relative path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
db = SQLAlchemy(app)

# A model


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    data = db.Column(db.LargeBinary)
    year = db.Column(db.DateTime, default=datetime.today().strftime('%Y'))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Book %r>' % self.id


# @app.route('/')
# def index():
#     return "<h1>Hello world</h1>"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addbook', methods=['GET', 'POST'])
def addBook():
    if request.method == "POST":
        title = request.form['title']
        file = request.files['file']
        year = request.form['year']
        book = Book(title=title, filename=year +"_" +
                    title, data=file.read(), year=year)
        db.session(book)
        db.session.commit()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
