import datetime
from flask import Flask, render_template, url_for, flash, request, redirect
from flask_cors import CORS, cross_origin
import sqlite3 as sql
app = Flask(__name__)

# enable cross origin ajax requests
CORS(app)


@app.route("/", methods=['GET'])
def home():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM messages")

    posts = cur.fetchall()
    return render_template('blog.html', posts=posts)

# THIS ROUTE IS JUST FOR TESTING
# SIMPLY SO I DONT HAVE TO MANUALLY WIPE THE DATABASE EVERY TEST
@app.route("/erase")
def erase():
    con = sql.connect("database.db")
    con.execute("DROP TABLE messages")
    con.execute("CREATE TABLE messages (date_posted TEXT, time_posted TEXT, content TEXT)")
    return redirect("/")

@app.route("/comment", methods=['POST'])
@cross_origin()
def comment():
    comment = request.json

    # If the message is a fake one, just return immediately
    if (comment['Onion']):
        return ('', 204)

    # Otherwise handle the message normally
    # Retrieve all necessary information
    date = datetime.datetime.now()
    date_posted = date.strftime("%x")
    time_posted = date.strftime("%X")
    message = comment['Content']

    # Insert the message to the database
    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO messages (date_posted, time_posted, content) VALUES (?, ?, ?)", (date_posted, time_posted, message))
            con.commit()
    except:
        con.rollback()
    finally:
        con.close()
        return ('', 204)

if (__name__ == "__main__"):
    app.run(debug=True)
