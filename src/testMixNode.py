import requests
from flask import Flask, request
from flask_cors import CORS, cross_origin
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5, AES
from base64 import b64decode
import json
app = Flask(__name__)

# enable cross origin ajax requests
CORS(app)

HOST = 'localhost'
DEBUG = True
PORT = 10000


def unpad(msg):
    return msg[:-msg[-1]]

def DecryptAES(encryptedMessage, key):
    block_size = 16
    decoded = b64decode(encryptedMessage)
    iv = decoded[:block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(decoded[block_size:])).decode('utf-8')

def DecryptRSA(encryptedMessage):
    private_key = RSA.importKey(open('key.pem', "rb").read(), passphrase='password')
    decoded = b64decode(encryptedMessage)
    cipher = PKCS1_v1_5.new(private_key)
    message = cipher.decrypt(decoded, None).decode()
    return message


@app.route("/comment", methods=['POST'])
@cross_origin()
def comment():
    comment = request.json

    # decrypt the AES symmetric key using RSA
    aes_key = DecryptRSA(comment['key']).encode('utf-8')

    # decrypt the message using AES
    decrypted_str = DecryptAES(comment['content'], aes_key)

    # retrieve the next url to send to from the decrypted json
    decrypted_json = json.loads(decrypted_str)
    next_url = decrypted_json['next_url']

    res = requests.post(next_url, json=decrypted_str)
    return ('', 204)

@app.route("/getkeys", methods=['GET'])
@cross_origin()
def getkeys():
    public_key = open('key.pub', "rb").read()
    public_key = public_key.decode().replace('\n', '')
    return json.dumps({'key': public_key})

if (__name__ == "__main__"):
    app.run(host=HOST, debug=DEBUG, port=PORT) # ssl_context="adhoc" to add TLS
