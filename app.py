from functools import wraps

from flask import Flask, request, render_template, redirect, session
import sqlite3
app = Flask(__name__)
app.secret_key = 'sdhhjdsfjjihuyug87487bsdjb7843'

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DbLocal(object):
    def __init__(self, file_name):
        self.con = sqlite3.connect(file_name)
        self.con.row_factory = dict_factory
        self.cur = self.con.cursor()
    def __enter__(self):
        return self.cur
    def __exit__(self, type, value, traceback):
        self.con.commit()
        self.con.close()

class DbHandler(object):
    db_file = 'db.db'
    def select(self, table_name, filter_dict=None, join_table=None, join_conditions=None):
        if filter_dict is None:
            filter_dict = {}
        with DbLocal(self.db_file) as db_cur:
            query = f'SELECT * FROM {table_name} '

            if join_table is not None:
                query += f'JOIN {join_table} as right_table ON '
                join_conditions_list = []
                for left_field, right_field in join_conditions.items():
                    join_conditions_list.append(f'{table_name}.{left_field}=right_table.{right_field}')
                query += ' AND '.join(join_conditions_list)

            if filter_dict:
                query += f' WHERE '
                join_items = []
                for key, value in filter_dict.items():
                    join_items.append(f' {key} = ?')
                query += ' AND '.join(join_items)

            db_cur.execute(query, tuple(value for value in filter_dict.values()))
            return db_cur.fetchall()

    def insert(self, table_name, data_dict):
        with (DbLocal(self.db_file) as db_cur):
            query = f'INSERT INTO {table_name} ('
            query += ','.join(data_dict.keys())
            query += ') VALUES ('
            query += ','.join([f':{itm}' for itm in data_dict.keys()])
            query += ')'
            db_cur.execute(query, tuple(data_dict.values()))

db_connector = DbHandler()

def login_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapped

@app.route('/')
def hello_world():  # put application's code here
    return '<p>This is a test project</p>'
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = db_connector.select('user', {'login':request.form.get('login'),
                                                                    'password':request.form.get('password')})
        if user_id:
            session['user_id'] = user_id[0]['id']
            session['user_login'] = user_id[0]['login']
            session['user_name'] = user_id[0]['full_name']
        else:
            return redirect('/login')
        return 'You are logged in as: <b>' + session['user_login']+'</b>'

    if request.method == 'GET':
        return render_template('login.html')

@app.route('/register', methods =  ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")

    if request.method == 'POST':
        form_data = request.form
        db_connector.insert('user', form_data)
        return redirect('/login')

@app.route('/logout', methods = ['GET', 'POST', 'DELETE'])
@login_required
def logout():
    session.pop('user_id', None)
    session.pop('user_login', None)
    session.pop('user_name', None)
    return redirect('/login')

@app.route('/profile', methods = ['GET', 'PUT'])
@login_required
def profile():
    if request.method == 'PUT':
        with DbLocal('db.db') as db_cur:
            pass
        return "PUT"

    if request.method == 'GET':
        full_name = db_connector.select('user', {'id':session["user_id"]})[0]['full_name']
        return render_template('user.html', full_name=full_name)

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
@login_required
def favourites():
    if request.method == 'GET':
        items = db_connector.select('favourites', {'user':session["user_id"]},
                                    'item', {'item':'id'})
        # with DbLocal('db.db') as db_cur:
        #      db_cur.execute('''SELECT * FROM favourites JOIN item ON favourites.item = item.id
        #                         WHERE favourites.user = ?''',
        #                    (session["user_id"],)
        #                     )
        #      items = db_cur.fetchall()
        return render_template('items.html', items=items)

    if request.method == 'PUT':
        return 'PUT'

    if request.method == 'PATCH':
        return 'PATCH'

    if request.method == "DELETE":
        return 'DELETE'

@app.route('/profile/favourites/<favourite_id>', methods = ['DELETE'])
@login_required
def favourite(favourite_id):
    if request.method == "DELETE":
        return 'DELETE'

@app.route('/profile/search_history', methods=['GET', 'DELETE'])
@login_required
def search_history():
    if request.method == 'GET':
        search_list = db_connector.select('search_history', {'user':session["user_id"]})
        return render_template('user.html', lines=search_list)
    if request.method == "DELETE":
        return 'DELETE'

@app.route('/items', methods = ['GET', 'POST'])
def items():
    if request.method == 'POST':
        if session.get('user_id') is None:
            return redirect('/login')

        query_args = dict(request.form)
        query_args["owner"] = session["user_id"]
        db_connector.insert('item', query_args)
        return redirect('/items')

    if request.method == 'GET':
        items_to_show = db_connector.select('item')
        return render_template('items.html', items=items_to_show)


@app.route('/items/<item_id>', methods = ['GET', 'PUT', 'DELETE'])
def item(item_id):
    if request.method == 'GET':
        our_item = db_connector.select('item', {'id':item_id})[0]
        return render_template('items.html', items=our_item)

    if request.method == 'PUT':
        return 'PUT'

    if request.method == 'DELETE':
        if session.get('user_id') is None:
            return redirect('/login')
        return 'DELETE'


@app.route('/leasers', methods = ['GET'])
@login_required
def leasers():
    if request.method == 'GET':
        leasers_list = db_connector.select('contract', None, 'user', {'leaser':'id'})
        return render_template('leasers.html', params=leasers_list)


@app.route('/leasers/<leaser_id>', methods = ['GET'])
@login_required
def leaser(leaser_id):
    if request.method == 'GET':
        return 'GET'

@app.route('/contracts', methods = ['GET', 'POST'])
@login_required
def contracts():
    if request.method == 'POST':
        item = request.form['item']
        leaser = db_connector.select('item', {'id':item})[0]['owner']
        taker = session['user_id']
        status = 'pending'
        contract_num = request.form['contract_num']
        query_args = {'text':request.form['text'], 'start_date':request.form['start_date'], 'end_date':request.form['end_date'],
                            'status':status, 'taker':taker, 'leaser':leaser, 'item':item, 'contract_num':contract_num}

        db_connector.insert('contract', query_args)
        return 'POST'

    if request.method == 'GET':
        contract_list = db_connector.select('contract')
        return render_template('contracts.html', params=contract_list)


@app.route('/contracts/<contract_id>', methods = ['GET', 'PUT', 'PATCH'])
@login_required
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
@login_required
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
