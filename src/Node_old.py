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

    for index in node_indices:
        encrypted_message, aes_key = encrypt_aes(json.dumps(jsonMsg))
        encrypted_key = encrypt_rsa(index, aes_key)
        next_url = PRE_URL + str(BASE_PORT + index) + POST_URL
        jsonMsg = {'next_url': next_url, 'content': encrypted_message, 'key': encrypted_key}

    res = requests.post(jsonMsg.get('next_url'), json=jsonMsg)

@app.route("/comment", methods=['POST'])
@cross_origin()
def comment():
    comment = request.json
    #if (type(comment) == type("")):
        #comment = json.loads(comment)

    # Putting received message into buffer queue and wati to be process
    buffer_queue.append(comment)

    # decrypt the AES symmetric key using RSA
    aes_key = decrypt_rsa(comment['key']).encode('utf-8')

    # decrypt the message using AES
    decrypted_str = decrypt_aes(comment['content'], aes_key)

    # retrieve the next url to send to from the decrypted json
    decrypted_json = json.loads(decrypted_str)
    next_url = decrypted_json['next_url']

    # Logs
    f = open(args[1]+'.log', 'a')
    f.write('\nReceived message at {}'.format(request.remote_addr, datetime.datetime.now()))
    f.write('\nSent {} to {} at {}'.format(decrypted_json, next_url, datetime.datetime.now()))
    f.close()

    # Random delay 1-7ms
    delay = random.randint(1,7)
    time.sleep(delay/1000)

    res = requests.post(next_url, json=decrypted_json)
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
    app.run(host=HOST, debug=DEBUG, port=PORT) # ssl_context="adhoc" to add TLS

  #with open('private_noshare.pem', 'wb') as f: f.write(serial_private)
  #with open('public_shared.pem', 'wb') as f: f.write(serial_pub)

'''
  for the sake of simplicity we are just assuming the node would only recieve a list of packets from the previous node. We are assuming the packets in the queue are ordered by arrival time.
'''
'''
To make back-tracing harder, we can either:
  1. shuffle the whole list of received packets
  2. retrieve a certain number and shuffle
'''

class Node:

  def __init__(self, id, mixnet, private_key, public_key):
    #keys = getKeys()
    self.id = id
    self.public_key = public_key
    self.private_key = private_key
    # Packets in the queue stays as string
    self.received_queue = list()
    self.awaiting_queue = list()
    # Referance to the mixnet singleton
    self.mixnet = mixnet
  
  # Put the received packet in the received queue
  def receive(self, packet):
    self.received_queue.append(packet)
    print("Received packet!")
    #print("Received payload: {}".format(payload))


  # def convert_to_dict(str: json_object):
  #   return json.loads(json_object)

  # def convert_to_json(dict: dictionary):
  #   return json.dumps(dictionary)

  # def send(self, dest, packet):
  #   self.mixnet.routeTo(dest, packet)

  # def receive_packets(list_of_packets):
  #   self.received_queue = list_of_packets

  def shuffle(list_of_packets):
    random.shuffle(list_of_packets)

  # def decrypt_and_send(self, list_of_packets):
  #   for packet in list_of_packets:
  #     #decryption goes here
  #     container = noise_creator()
  #     container.append(packet)
  #     shuffle(container)
  #     send_packet(container)


  
  def noise_creator():
    list_of_noise = []
    '''
      generating some fake packets here and fill the list up here
    '''
    return list_of_noise

  def send_packet(self, dest, packet):
    self.mixnet.route_to(dest, packet)

  def decode_packet(self, packet):
    packetDic = json.loads(packet)
    
    secret = packetDic.get('secret')
    key = packetDic.get('key')

    # TODO: RSA decyption on key then ASE decryption on secret
    # then load secret (JSON) into dict and return 

    '''
    How do we determine when the packet has reached its final destination? My thoughts: check if 'next' is found in secret? 
    A: that is correct
    '''
    return secret


  def build_new_packet(key):
    pass



  '''
    This is the working cycle of a Node
    1. Check if there is still more packets in the awaiting_queue
      a. if not get 5 more the received_queue, shuffle and store
         in awaiting_queue
    2. Parse the packet (JSON) into dictionary, shoud have this format
        {
          "keys": ["key0", "key1"],
          "secret": "{
            "next": 1,
            "secret": "xxxxxx"
          }"
        }
      Use the first ket to decyrpt secret to see the next destination,
      remove key after used
    3. Form new packet 
      {
        "keys": ["key1"],
        secret: "xxxxx"
      }
    4. Send packet after a random delay (time.sleep)
  '''
  def main(self):
    print("start running node{}".format(self.id))

    while True:
      if len(self.awaiting_queue) != 0:
        packet = self.awaiting_queue.pop()
        # Decode the packet and store 
        decoded_secret = self.decode_packet(self, packet)

        # No more layer, check if there is a post
        if decoded_secret.get("next") == None:
          # Update DB with post
          if decoded_secret.get('isReal') == True:
            self.mixnet.post_to_blog(decoded_secret.get('post'))
          # Do nothing
          else:
            pass
        # More layers
        else: 
          next = decoded_secret.get('next')
          content = decoded_secret.get('content')
          # Put to sleep with random time
          time.sleep(random.randrange(0, 0.087))
          # Send packet
          self.mixnet.route_to(next, content)


        # next_dest = decoded_value['next']
        # new_packet = decoded_value['newPacket']
      else:
        '''
        I am thinking if there would be any race condition here, because what if there are packets being recieved when we try to take packets out of the received_queue?

        A: don't matter cuz queue is FIFO, if there is it will only wait a bit till it gets pull from received_queue
        '''
        # Grab oldest 5 packets from received_queue
        if(len(self.received_queue) < 5):
          temp = random.shuffle(self.received_queue)
          self.awaiting_queue = temp
          self.received_queue.clear()
        else:
          temp = self.received_queue[:5]
          random.shuffle(temp)
          self.awaiting_queue = temp
          self.recieved_queue = self.received_queue[5:]
