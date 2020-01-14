from flask_mysqldb import MySQL
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from flask import flash, request
from flask import jsonify
import pymysql
import yaml

app = Flask(__name__)
app.secret_key = 'my secret key'

db = yaml.load(open('config.yaml'))
app.config['MYSQL_HOST'] = db['mysql']['host']
app.config['MYSQL_USER'] = db['mysql']['user']
app.config['MYSQL_PASSWORD'] = db['mysql']['pass']
app.config['MYSQL_DB'] = db['mysql']['db']

mysql = MySQL(app)
print(mysql)

class User(object):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def __str__(self):
        return "User(id='%s')" % self.id

@app.route('/whoami')
@jwt_required()
def me():
    resp = jsonify("ID:" + str(current_identity[0]) + ", User:" + str(current_identity[1]))
    resp.status_code = 200
    return resp


def authenticate(username, password):
    if username and password:
        conn = None;
        cursor = None;
    try:
        curs = mysql.connection.cursor()
        curs.execute('SELECT id, user, password FROM myusers where user = %s', [username])
        row = curs.fetchone()
        if row:
            if row[2] == password:
                return User(row[0], row[1])
        else:
            return None
    except Exception as e:
        print(e)
        return not_found()
    finally:
        curs.close()

def identity(payload):
    if payload['identity']:
        conn = None;
        cursor = None;
        try:
            curs = mysql.connection.cursor()
            curs.execute("SELECT id, user, password FROM myusers WHERE id=%s", [payload['identity']])
            row = curs.fetchone()
            if row:
                return (row[0], row[1])
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            curs.close()
    else:
        return None

jwt = JWT(app, authenticate, identity)

@app.route('/posts')
@jwt_required()
def posts():
    try:
        curs = mysql.connection.cursor()
        curs.execute('SELECT type FROM myusers where id = %s', [current_identity[0]])
        row = curs.fetchone()
        if row[0] == 'admin':
            curs.execute('SELECT * FROM posts')
        else:
            curs.execute('SELECT id, user, title, content, tags, likes FROM posts')
        rows = curs.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        return not_found()
    finally:
        curs.close()


@app.route('/users')
@jwt_required()
def users():
    try:
        curs = mysql.connection.cursor()
        curs.execute('SELECT * FROM myusers')
        rows = curs.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
        return not_found()
    finally:
        curs.close()


@app.route('/register', methods = ['POST'])
@jwt_required()
def register():
    try:
        _json = request.json
        _user = _json['user']
        _password = _json['password']
        _type = _json['type']
        if _user and _password and _type and request.method == 'POST':
            curs = mysql.connection.cursor()
            curs.execute('INSERT INTO myusers(user, password, type) VALUES(%s, %s, %s)', (_user, _password, _type))
            mysql.connection.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
        return not_found()
    finally:
        curs.close()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found!',
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

@app.errorhandler(403)
def forbidden(error=None):
    message = {
        'status': 403,
        'message': 'You are Unauthorized!',
    }
    resp = jsonify(message)
    resp.status_code = 403
    return resp


@app.route('/create', methods = ['POST'])
@jwt_required()
def create():
    curs = mysql.connection.cursor()
    curs.execute('SELECT type FROM myusers where id = %s', [current_identity[0]])
    row = curs.fetchone()
    if row[0] != 'admin':
        return forbidden()

    _json = request.json
    _title = _json['title']
    _content = _json['content']
    _admin_content = _json['admin_content']
    _tags = _json['tags']

    if _title and _content and request.method == 'POST':
        curs = mysql.connection.cursor()
        curs.execute('INSERT INTO posts (user, title, content, admin_content, tags) values (%s, %s, %s, %s, %s)', ([current_identity[1]], _title, _content, _admin_content, _tags))
        mysql.connection.commit()
        resp = jsonify('Post inserted to DB')
        resp.status_code = 200
        return resp
    return not_found()

@app.route('/search', methods = ['POST'])
@jwt_required()
def search():
    _json = request.json
    _id = _json['id']

    curs = mysql.connection.cursor()
    if _id and request.method == 'POST':
        curs.execute('SELECT * FROM posts WHERE id = %s', _id)
        post = curs.fetchall()
        resp = jsonify(post)
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.route('/delete', methods = ['POST'])
@jwt_required()
def delete():
    _json = request.json
    _id = _json['id']

    curs = mysql.connection.cursor()
    curs.execute('DELETE FROM posts where id = %s', (_id))
    mysql.connection.commit()
    curs.execute('DELETE FROM comments where id = %s', (_id))
    mysql.connection.commit()
    curs.execute('DELETE FROM likes where id = %s', (_id))
    mysql.connection.commit()
    resp = jsonify("post deleted!")
    resp.status_code = 200
    return resp

if __name__=='__main__':
    app.run(host='0.0.0.0', port=9000, debug='True')
