import sqlite3

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, jsonify


# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'my_precious'
USERNAME = 'admin'
PASSWORD = 'admin'

# create and initialize app
app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def index():
    """Searches the db for entries, then displays them"""
    db = get_db()
    cur = db.execute('SELECT * FROM entries ORDER BY id DESC')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login/authentication/session management"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    """User logout/authentiation/session management."""
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


# connect to db
def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


# create db
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


# open db connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


# close db connection
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


if __name__ == '__main__':
    init_db()
    app.run()
