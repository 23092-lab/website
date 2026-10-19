from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "rankings.db"


def create_connection(db_file):  # database connection function
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:  # error catcher
        print(e)
    return None


@app.route('/')  # home renderer using index.html for the root document of the website
def render_home():
    return render_template("index.html")


@app.route(
    '/ranking')  # rankings renderer, for a no filters ranking of all the players, accessed through the purple link
def render_webpages():
    query = "SELECT name,ranking,aura,active,country from ranks"  # query selects all entries in ranks table
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    ranking_list = cur.fetchall()
    con.close()
    print(ranking_list)  # debug uses for checking what entries
    return render_template("ranking.html", ranks=ranking_list)


@app.route('/search', methods=['GET', 'POST'])  # uses get and post methods to transfer data from the static html
# page to python file to parse
def render_search():
    search = request.form.get('search', '')  # search text box
    country = request.form.get('country', '')  # option from country drop down
    sort = request.form.get('sort', '')  # option from the sort order drop down

    search = "%" + search + "%"  # wildcard search
    query = ("SELECT name, ranking, aura, active, country FROM ranks "
             "WHERE (name LIKE ? OR ranking LIKE ? OR active LIKE ? OR aura LIKE ?)")

    params = [search, search, search, search]  # lets the database search all 4 individual tags at the same time
    if country:  # if there is a country selected, appends AND country to the end of the query so only countries
        # selected will be filtered in
        query += " AND country = ?"
        params.append(country)

    if sort == 'desc':  # if drop down menu is either desc or asc, then append following in order to organize data
        # entries through backend
        query += " ORDER BY CAST(ranking AS INTEGER) DESC"
    else:
        query += " ORDER BY CAST(ranking AS INTEGER) ASC"

    con = create_connection(DATABASE)  # code to connect to the database and fetch query
    cur = con.cursor()
    cur.execute(query, tuple(params))  # pass tuple(params) in order to allow searching on every single column specified
    ranking_list = cur.fetchall()
    con.close()
    return render_template("ranking.html", ranks=ranking_list)


if __name__ == '__main__':
    app.run()
