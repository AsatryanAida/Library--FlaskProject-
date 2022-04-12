import sqlite3
from flask import Flask, render_template, url_for, request, redirect, flash
from werkzeug.exceptions import abort


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT title, about FROM library WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


def get_post_title(post_title):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM library WHERE title = ?', (post_title,)).fetchall()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY']='jnjkniljmvyusnfcovnfgdmdkdn'


@app.route('/posts')
def posts():
    q = request.args.get('q')

    if q:
        library = get_post_title(q)
    else:
        conn = get_db_connection()
        library = conn.execute('SELECT id, UDK, author, title, year FROM library').fetchall()
        conn.close()
    return render_template('posts.html', library=library)


@app.route('/posts/<int:post_id>')
def about(post_id):
    post = get_post(post_id)
    return render_template('post_detailed.html', post=post)


@app.route('/')
def index():
    return render_template("main.html")


if __name__ == '__main__':
    app.run()


@app.route('/new-book', methods=["POST", "GET"])
def new_book():
    if request.method == "POST":
        UDK = request.form['UDK']
        author = request.form['author']
        title = request.form['title']
        year = request.form['year']
        about = request.form['about']



        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO library (UDK, author, title, year, about) VALUES(?,?,?,?,?)", (UDK, author, title, year, about))
            conn.commit()
            conn.close()
            return redirect('/posts')
        except:
            return "При добавлении книги произошла ошибка"

    else:
        return render_template("new-book.html")


@app.route('/posts/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    library = get_post(id)

    if request.method == 'POST':
        UDK = request.form['UDK']
        author = request.form['author']
        title = request.form['title']
        year = request.form['year']
        about = request.form['about']

        if not UDK:
            flash('Введите УДК')
        elif not author:
            flash('Введите имя автора')
        elif not title:
            flash('Введите название')
        elif not year:
            flash('Введите год издания')
        elif not about:
            flash('Введите описание')
        else:

            try:
                conn = get_db_connection()
                conn.execute('UPDATE library SET UDK = ?, author = ?, title = ?, year = ?, about = ?''WHERE id = ?',
                             (UDK, author, title, year, about, id))
                conn.commit()
                conn.close()
                return redirect('/posts')
            except:
                return "При изменении информации произошла ошибка"

    return render_template('edit.html', library=library)







