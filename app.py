from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "rankings.db"


def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


@app.route('/')
def render_home():
    return render_template("index.html")


@app.route('/ranking')
def render_webpages():
    query = "SELECT id,name,ranking,aura,active from ranks"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    ranking_list = cur.fetchall()
    con.close()
    print(ranking_list)
    return render_template("ranking.html", ranks=ranking_list)


@app.route('/search',methods=['GET','POST'])
def render_search():
    search = request.form['search']
    search = "%" + search + "%"
    query = "SELECT name, ranking, aura, active FROM ranks WHERE name like ? OR ranking like ? OR active like ? OR " \
            "aura like ?"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search,search,search,search))
    ranking_list = cur.fetchall()
    con.close()
    return render_template("ranking.html", ranks=ranking_list)


if __name__ == '__main__':
    app.run()
