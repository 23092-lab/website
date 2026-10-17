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
    query = "SELECT name,ranking,aura,active,country from ranks"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    ranking_list = cur.fetchall()
    con.close()
    print(ranking_list)
    return render_template("ranking.html", ranks=ranking_list)


@app.route('/search',methods=['GET','POST'])
def render_search():
    search = request.form.get('search','')
    country = request.form.get('country','')
    sort = request.form.get('sort','')

    search = "%" + search + "%"
    query = ("SELECT name, ranking, aura, active, country FROM ranks "
             "WHERE (name LIKE ? OR ranking LIKE ? OR active LIKE ? OR aura LIKE ?)")

    params = [search,search,search,search]
    if country:
        query += " AND country = ?"
        params.append(country)
    
    if sort == 'desc':
        query += " ORDER BY CAST(ranking AS INTEGER) DESC"
    else:
        query += " ORDER BY CAST(ranking AS INTEGER) ASC"

    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, tuple(params))
    ranking_list = cur.fetchall()
    con.close()
    return render_template("ranking.html", ranks=ranking_list)


if __name__ == '__main__':
    app.run()
