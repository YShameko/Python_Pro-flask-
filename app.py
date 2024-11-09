from flask import Flask, request, render_template, redirect, session
import sqlite3
app = Flask(__name__)
app.secret_key = 'sdhhjdsfjjihuyug87487bsdjb7843'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DB_local(object):
    def __init__(self, file_name):
        self.con = sqlite3.connect(file_name)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()
    def __enter__(self):
        return self.cur
    def __exit__(self, type, value, traceback):
        self.con.commit()
        self.con.close()

def open_DB(db_name):
    return DB_local(db_name)
@app.route('/')
def hello_world():  # put application's code here
    return '<p>This is a test project</p>'
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        with DB_local('db.db') as db_cur:
            db_cur.execute('SELECT * FROM users WHERE login = ? AND password = ?',
                           (request.form.get('login'),))
            user_id = db_cur.fetchall()[0][0]
        if user: # do something
        else:
            return render_template('/login')
        session['username'] = request.form['username']
        return 'POST'
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/register', methods =  ['GET', 'POST'])
def register():
    if request.method == 'POST':
        with DB_local('db.db') as db_cur:
            form_data = request.form
            db_cur.execute('''INSERT into user 
                            (login, password, ipn, full_name, contacts, photo, passport)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           form_data['login'], form_data['password'], form_data['ipn'], form_data['full_name'],
                           form_data['contacts'], form_data['photo'], form_data['passport'])
        return redirect('/login')
    if request.method == 'GET':
        return render_template("register.html")
@app.route('/logout', methods = ['GET', 'POST', 'DELETE'])
def logout():
    session.pop('user_id', None)
    return redirect('/')
    if request.method == 'POST':
        return 'POST'
    if request.method == 'GET':
        return '<p>You have been logged out</p>'
    if request.method == "DELETE":
        return 'DELETE'

@app.route('/profile', methods = ['GET', 'PUT'])
def profile():
    if session.get('user_id') is None:
        return f'Logged in as {session["user_id"]}'
    return 'You are not logged in'

    if request.method == 'PUT':
        with DB_local('db.db') as db_cur:
        return "PUT"
    if request.method == 'GET':
        with DB_local('db.db') as db_cur:
            db_cur.execute('SELECT * FROM users WHERE login = ? AND password = ?',)
        return 'GET'
@app.route('/profile/<user_id>', methods = ['GET', 'PUT', 'PATCH', 'DELETE'])
# /profile (/user, /me) [GET, PUT(PATCH), DELETE]
#      what shall we do with /me ?
def profile(user_id):
    if request.method == 'GET':
        return 'GET'
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == "DELETE":
        return 'DELETE'

@app.route('/profile/favourites', methods = ['GET', 'PUT', 'PATCH', 'DELETE'])
def favourites():
    if request.method == 'GET':
        return 'GET'
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == "DELETE":
        return 'DELETE'

@app.route('/profile/favourites/<favourite_id>', methods = ['DELETE'])
def favourite(favourite_id):
    if request.method == "DELETE":
        return 'DELETE'

@app.route('/profile/search_history', methods=['GET', 'DELETE'])
def search_history():
    if request.method == 'GET':
        return 'GET'
    if request.method == "DELETE":
        return 'DELETE'

@app.route('/items', methods = ['GET', 'POST'])
def items():
    if request.method == 'POST':
        return 'POST'
    if request.method == 'GET':
        with DB_local('db.db') as db_cur:
            db_cur.execute('SELECT * FROM item')
            items = db_cur.fetchall()
            render_template('items.html', items=items)
        return 'GET'

@app.route('/items/<item_id>', methods = ['GET', 'PUT', 'DELETE'])
def item(item_id):
    if request.method == 'GET':
        return 'GET'
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'DELETE':
        return 'DELETE'

@app.route('/leasers', methods = ['GET'])
def leasers():
    if request.method == 'GET':
        return 'GET'
@app.route('/leasers/<leaser_id>', methods = ['GET'])
def leaser(leaser_id):
    if request.method == 'GET':
        return 'GET'

@app.route('/contracts', methods = ['GET', 'POST'])
def contracts():
    if request.method == 'POST':
        return 'POST'
    if request.method == 'GET':
        return 'GET'
@app.route('/contracts/<contract_id>', methods = ['GET', 'PUT', 'PATCH'])
def contract(contract_id):
    if request.method == 'GET':
        return 'GET'
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'PATCH':
        return 'PATCH'

@app.route('/search', methods = ['GET', 'POST'])
def search():
    if request.method == 'POST':
        return 'POST'
    if request.method == 'GET':
        return 'GET'

@app.route('/complain', methods = ['POST'])
def complain():
    if request.method == 'POST':
        return 'POST'

@app.route('/compare', methods = ['GET', 'PUT', 'PATCH'])
def compare():
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'PATCH':
        return 'PATCH'
    if request.method == "GET":
        return 'GET'

if __name__ == '__main__':
    app.run()

