import requests
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_apscheduler import APScheduler
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5, AES, PKCS1_OAEP
from base64 import b64decode, b64encode
import json
import sys
import random
import os
import string
import datetime
import time
import multiprocessing

app = Flask(__name__)

# enable cross origin ajax requests
CORS(app)

args = sys.argv

if (len(args) != 4):
    print("python3", args[0], "<node number> <hostname> <total number of nodes>")
    quit()

HOST = args[2]
DEBUG = True
PORT = 10000 + int(args[1])

PRE_URL = 'http://' + HOST + ':'
POST_URL = '/comment'
BASE_PORT = 10000
SERVER_URL = PRE_URL + '5000/comment'

# Message queues
buffer_queue = list()
outbound_queue = list()
BATCH_SIZE = 5

def pad(msg):
    block_size = 16
    return msg + (block_size - len(msg) % block_size) * chr(block_size - len(msg) % block_size)


def unpad(msg):
    return msg[:-msg[-1]]

def generate_key_iv():
    key = "".join(random.choice(string.ascii_letters) for i in range(16)).encode('utf-8')
    iv = "".join(random.choice(string.ascii_letters) for i in range(16)).encode('utf-8')
    return key, iv

def encrypt_aes(message):
    key, iv = generate_key_iv()
    aes = AES.new(key, AES.MODE_CBC, iv)
    message = pad(message)
    encrypted = aes.encrypt(message)
    encrypted = b64encode(iv + encrypted).decode('utf-8')
    return encrypted, key

def encrypt_rsa(node_index, message):
    public_key = open(str(node_index) + '.pub', "rb").read()
    keyPub = RSA.importKey(public_key)
    cipher = PKCS1_v1_5.new(keyPub)
    ciphertext = cipher.encrypt(message)
    encrypted = b64encode(ciphertext).decode('utf-8')
    return encrypted

def decrypt_aes(encryptedMessage, key):
    block_size = 16
    decoded = b64decode(encryptedMessage)
    iv = decoded[:block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(decoded[block_size:])).decode('utf-8')

def decrypt_rsa(encryptedMessage):
    private_key = RSA.importKey(open(args[1] + '.pem', "rb").read(), passphrase='password')
    decoded = b64decode(encryptedMessage)
    cipher = PKCS1_v1_5.new(private_key)
    message = cipher.decrypt(decoded, None)
    message = message.decode()
    return message

def generate_noise():
    length_of_string = random.choice(range(5, 250))
    message = "".join(random.choice(string.ascii_letters) for i in range(length_of_string))

    node_indices = list(range(0, int(args[3])))
    node_indices.remove(int(args[1]))
    random.shuffle(node_indices, random.SystemRandom().random)

    jsonMsg = {'next_url': SERVER_URL, 'is_real': False, 'content': message}

    # for index in node_indices:
    #     encrypted_message, aes_key = encrypt_aes(json.dumps(jsonMsg))
    #     encrypted_key = encrypt_rsa(index, aes_key)
    #     next_url = PRE_URL + str(BASE_PORT + index) + POST_URL
    #     jsonMsg = {'next_url': next_url, 'content': encrypted_message, 'key': encrypted_key}

    # res = requests.post(jsonMsg.get('next_url'), json=jsonMsg)

    # json_str = json.dumps(jsonMsg)

    return jsonMsg

def work_cycle():
    global buffer_queue
    global outbound_queue

    # Unload the outboud queue
    while len(outbound_queue) != 0:
        decrypted_str = outbound_queue.pop(0)

        # retrieve the next url to send to from the decrypted json
        decrypted_json = json.loads(decrypted_str)
        next_url = decrypted_json['next_url']

        # Log
        f = open(args[1]+'.log', 'a')
        f.write('\nSent {} to {} at {}'.format(decrypted_json, next_url, datetime.datetime.now()))
        f.close()

        # Random delay 1-7ms
        delay = random.randint(1,7)
        time.sleep(delay/1000)

        # Send
        res = requests.post(next_url, json=decrypted_json)
    
    # Get a batch from buffer queue, shuffle and load into outbound queue
    if len(buffer_queue) >= BATCH_SIZE:
        temp = buffer_queue[:BATCH_SIZE]
        random.shuffle(temp)

        # Load shuffled messages into outbound_queue
        outbound_queue = temp

        # Removed processed messages from buffer
        temp = buffer_queue[BATCH_SIZE:]
        buffer_queue = temp
    else:
        queue_size = len(buffer_queue)
        temp = buffer_queue[:queue_size]

        # Load noise
        # for i in range(BATCH_SIZE-queue_size):
        #     jsonMsg = generate_noise()
        #     json_str = json.dumps(jsonMsg)
        #     temp.append(json_str)

        random.shuffle(temp)

        # Load shuffled messages into outbound_queue
        outbound_queue = temp

        # Removed processed messages from buffer
        temp = buffer_queue[queue_size:]
        buffer_queue = temp


@app.route("/comment", methods=['POST'])
@cross_origin()
def comment():
    global buffer_queue

    comment = request.json
    #if (type(comment) == type("")):
        #comment = json.loads(comment)

    # decrypt the AES symmetric key using RSA
    aes_key = decrypt_rsa(comment['key']).encode('utf-8')

    # decrypt the message using AES
    decrypted_str = decrypt_aes(comment['content'], aes_key)

    # Putting received decrypted message into buffer queue and wati to be process
    buffer_queue.append(decrypted_str)

    # # retrieve the next url to send to from the decrypted json
    # decrypted_json = json.loads(decrypted_str)
    # next_url = decrypted_json['next_url']

    # Logs
    f = open(args[1]+'.log', 'a')
    f.write('\nReceived message at {}'.format(datetime.datetime.now()))
    # f.write('\nSent {} to {} at {}'.format(decrypted_json, next_url, datetime.datetime.now()))
    f.close()

    # # Random delay 1-7ms
    # delay = random.randint(1,7)
    # time.sleep(delay/1000)

    # res = requests.post(next_url, json=decrypted_json)
    return ('', 204)


@app.route("/getkeys", methods=['GET'])
@cross_origin()
def getkeys():
    public_key = open(args[1] + '.pub', "rb").read()
    public_key = public_key.decode().replace('\n', '')
    return {'url': 'http://' + HOST + ':' + str(PORT) + '/comment', 'key': public_key}

if (__name__ == "__main__"):
    # noise_scheduler = APScheduler()
    # noise_scheduler.add_job(func=generate_noise, args=[], trigger='interval', id='noise', seconds=0.5)
    # noise_scheduler.start()

    work_cycle_scheduler = APScheduler()
    work_cycle_scheduler.add_job(func=work_cycle, args=[], trigger='interval', id='work_cycle', seconds=1)
    work_cycle_scheduler.start()

    app.run(host=HOST, debug=DEBUG, port=PORT) # ssl_context="adhoc" to add TLS


