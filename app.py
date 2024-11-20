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

@app.route('/')
def hello_world():  # put application's code here
    return '<p>This is a test project</p>'
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        with DB_local('db.db') as db_cur:
            db_cur.execute('SELECT * FROM user WHERE login = ? AND password = ? ', (request.form.get('login'),request.form.get('password')))
            user_id = db_cur.fetchall()[0]
        #if user_id: # do something
        #else:
        #    return render_template('/login')
        session['username'] = request.form['login']
        return 'Login: POST'
    if request.method == 'GET':
        return render_template('login.html')

@app.route('/register', methods =  ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    if request.method == 'POST':
        with DB_local('db.db') as db_cur:
            form_data = request.form
            db_cur.execute('''INSERT INTO user 
                            (login, password, ipn, full_name, contacts, photo, passport)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (
                               form_data['login'], form_data['password'], form_data['ipn'], form_data['full_name'],
                           form_data['contacts'], form_data['photo'], form_data['passport']
                                    )
                           )
        return redirect('/login')

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
    #if session.get('user_id') is None:
    #    return f'You're logged-in as {session["user_id"]}'
    #return 'You are not logged in'

    if request.method == 'PUT':
        with DB_local('db.db') as db_cur:
            pass
        return "PUT"
    if request.method == 'GET':
        with DB_local('db.db') as db_cur:
            db_cur.execute('SELECT * FROM users WHERE login = ? AND password = ?',)
        return 'GET'
#@app.route('/profile/<user_id>', methods = ['GET', 'PUT', 'PATCH', 'DELETE'])
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
        with DB_local('db.db') as db_cur:
            exec_param = '' # put here current user_id later
            db_cur.execute('''SELECT * FROM favourites JOIN item ON favourites.item = item.id 
                                WHERE favourites.user = ?''',
                           exec_param)
            items = db_cur.fetchall()
        return render_template('items.html', items=items)

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
        with DB_local('db.db') as db_cur:
            exec_param = '' # put some 'current user' id here later
            db_cur.execute('''SELECT * FROM search_history WHERE favourites.user = ?''',
                           exec_param)
            search_hist = db_cur.fetchall()
        return render_template('user.html', lines=search_hist)
    if request.method == "DELETE":
        return 'DELETE'

@app.route('/items', methods = ['GET', 'POST'])
def items():
    if request.method == 'POST':
        with DB_local('db.db') as db_cur:
            db_cur.execute('''INSERT INTO item 
            (photo, name, description, price_hour, price_day, price_week, price_month, owner)
            VALUES(:photo, :name, :description, :price_hour, :price_day, :price_week, :price_month, :owner )''', request.form)
        return redirect('/items')
    if request.method == 'GET':
        with DB_local('db.db') as db_cur:
            db_cur.execute('SELECT * FROM item')
            items = db_cur.fetchall()
        return render_template('items.html', items=items)


@app.route('/items/<item_id>', methods = ['GET', 'PUT', 'DELETE'])
def item(item_id):
    if request.method == 'GET':
        with DB_local('db.db') as db_cur:
            db_cur.execute('SELECT * FROM item WHERE id = ?', (item_id,))
            our_item = db_cur.fetchone()
        return render_template('items.html', items=our_item)
    if request.method == 'PUT':
        return 'PUT'
    if request.method == 'DELETE':
        return 'DELETE'


@app.route('/leasers', methods = ['GET'])
def leasers():
    if request.method == 'GET':
        with DB_local('db.db') as db_cur:
            db_cur.execute('''SELECT user.full_name, user.contacts, user.photo
                            FROM contract JOIN user ON contract.leaser = user.id
                            ''')
            leasers_list = db_cur.fetchall()
        return render_template('leasers.html', params=leasers_list)


@app.route('/leasers/<leaser_id>', methods = ['GET'])
def leaser(leaser_id):
    if request.method == 'GET':
        return 'GET'

@app.route('/contracts', methods = ['GET', 'POST'])
def contracts():
    if request.method == 'POST':
        return 'POST'
    if request.method == 'GET':
        with DB_local('db.db') as db_cur:
            db_cur.execute('''SELECT * FROM contract ''')
            contracts_list = db_cur.fetchall()
        return render_template('contracts.html', params=contracts_list)


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
