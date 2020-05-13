import datetime
from flask import Flask, render_template, url_for, flash, request, jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# enable cross origin ajax requests
CORS(app)

# using a simple list until we have a database
posts = []

@app.route("/", methods=['GET'])
def home():
    return render_template('blog.html', posts=posts)


@app.route("/comment", methods=['POST'])
@cross_origin()
def comment():
    comment = request.json
    date = datetime.datetime.now()
    newComment = { 'date_posted' : date.strftime("%x"),
                'time_posted' : date.strftime("%X"),
                'content' : comment['Content']}
    posts.append(newComment)
    return ('', 204)

if (__name__ == "__main__"):
    app.run(debug=True)
