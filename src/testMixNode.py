import requests
from flask import Flask, request
from flask_cors import CORS, cross_origin
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5, AES, PKCS1_OAEP
from base64 import b64decode
import json
import sys
app = Flask(__name__)

# enable cross origin ajax requests
CORS(app)

args = sys.argv

if (len(args) != 3):
    print("python3", args[0], "<node number> <hostname>")
    quit()

HOST = args[2]
DEBUG = True
PORT = 10000 + int(args[1])


def unpad(msg):
    return msg[:-msg[-1]]

def DecryptAES(encryptedMessage, key):
    block_size = 16
    decoded = b64decode(encryptedMessage)
    iv = decoded[:block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(decoded[block_size:])).decode('utf-8')

def DecryptRSA(encryptedMessage):
    private_key = RSA.importKey(open(args[1] + '.pem', "rb").read(), passphrase='password')
    decoded = b64decode(encryptedMessage)
    cipher = PKCS1_v1_5.new(private_key)
    message = cipher.decrypt(decoded, None)
    message = message.decode()
    return message


@app.route("/comment", methods=['POST'])
@cross_origin()
def comment():
    comment = request.json
    #if (type(comment) == type("")):
        #comment = json.loads(comment)

    # decrypt the AES symmetric key using RSA
    aes_key = DecryptRSA(comment['key']).encode('utf-8')

    # decrypt the message using AES
    decrypted_str = DecryptAES(comment['content'], aes_key)

    # retrieve the next url to send to from the decrypted json
    decrypted_json = json.loads(decrypted_str)
    next_url = decrypted_json['next_url']

    res = requests.post(next_url, json=decrypted_json)
    return ('', 204)

@app.route("/getkeys", methods=['GET'])
@cross_origin()
def getkeys():
    public_key = open(args[1] + '.pub', "rb").read()
    public_key = public_key.decode().replace('\n', '')
    return {'url': 'http://' + HOST + ':' + str(PORT) + '/comment', 'key': public_key}

if (__name__ == "__main__"):
    app.run(host=HOST, debug=DEBUG, port=PORT) # ssl_context="adhoc" to add TLS
