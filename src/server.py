import datetime
from flask import Flask, render_template, url_for, flash, request, redirect
from flask_cors import CORS, cross_origin
import sqlite3 as sql
import json
import sys

app = Flask(__name__)

# enable cross origin ajax requests
CORS(app)

args = sys.argv

if (len(args) != 3):
    print("python3", args[0], "<hostname> <num_nodes>")
    quit()

HOST = args[1]
NUM_NODES = args[2]
DEBUG = True
PORT = 5000

# Default route to get the webpage
@app.route("/", methods=['GET'])
def home():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM messages")

    posts = cur.fetchall()
    node_info = {'host': HOST, 'num_nodes': NUM_NODES}
    return render_template('blog.html', posts=posts, node_info=node_info)

'''
THIS ROUTE IS JUST FOR TESTING
SIMPLY SO I DONT HAVE TO MANUALLY WIPE THE DATABASE EVERY TEST
'''
@app.route("/erase")
def erase():
    con = sql.connect("database.db")
    con.execute("DROP TABLE messages")
    con.execute("CREATE TABLE messages (date_posted TEXT, time_posted TEXT, content TEXT)")
    return redirect("/")

# The route to post a new message
@app.route("/comment", methods=['POST'])
@cross_origin()
def comment():
    comment = request.json

    #comment = json.loads(comment)

    # If the message is a fake one, just return immediately
    if (not comment['is_real']):
        return ('', 204)

    # Otherwise handle the message normally
    # Retrieve all necessary information
    date = datetime.datetime.now()
    date_posted = date.strftime("%x")
    time_posted = date.strftime("%X")

    message = comment['content']

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
    app.run(host=HOST, debug=DEBUG, port=PORT)
