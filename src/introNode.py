import requests
from flask import Flask, request
from flask_cors import CORS, cross_origin
app = Flask(__name__)

# enable cross origin ajax requests
CORS(app)


@app.route("/intro", methods=['POST'])
@cross_origin()
def comment():
    comment = request.json
    res = requests.post('http://localhost:5000/comment', json=comment)
    return ('', 204)


if (__name__ == "__main__"):
    app.run(debug=True, port=10000) # ssl_context="adhoc" to add TLS
