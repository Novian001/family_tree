from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import json

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_javan'

mysql = MySQL()
mysql.init_app(app)

# fetch data from database


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_member/<id>', methods=['GET'])
def get_member(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM family_tree WHERE id = {}".format(id))
    data = cur.fetchone()
    cur.close()
    return json.dumps(data)

# update member


@app.route('/update_member/<id>', methods=['POST'])
def update_member(id):
    cur = mysql.connection.cursor()
    name = request.form['editName']
    gender = request.form['editGender']
    parent_id = request.form['editParent']
    grand_id = request.form['editGrand']
    cur.execute("UPDATE family_tree SET name = %s, gender = %s, parent_id = %s, grand_id WHERE id = %s",
                (name, gender, parent_id, grand_id, id))
    mysql.connection.commit()
    cur.close()
    members = cur.fetchall()
    return redirect(url_for('view', members=members))

# toggle modal


@app.route('/toggle_modal/<id>', methods=['GET'])
def toggle_modal(id):
    # fetch data from database
    member = json.loads(get_member(id))
    # fill the form with data
    return render_template('edit_member.html', member=member)

# view member


@app.route('/view')
def view():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM family_tree")
    members = cur.fetchall()
    cur.close()
    return render_template('view_member.html', members=members)

# delete member


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM family_tree WHERE id = {}".format(id))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('view'))

# create member


@app.route('/create', methods=['POST'])
def create():
    cur = mysql.connection.cursor()
    name = request.form['addName']
    gender = request.form['addGender']
    parent_id = request.form['addParent']
    grand_id = request.form['addGrand']
    cur.execute("INSERT INTO family_tree (id, name, gender, parent_id, grandparent_id) VALUES (%s, %s, %s)",
                (name, gender, parent_id, grand_id))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('view'))


if __name__ == '__main__':
    app.run(debug=True)
