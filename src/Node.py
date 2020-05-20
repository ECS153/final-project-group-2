# Module from encryption
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

import random

def getKeys():
  private_key = rsa.generate_private_key(
      public_exponent=65537,
      key_size=2048,
      backend=default_backend()
  )

  public_key = private_key.public_key()

  serial_private = private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
  )

  serial_pub = public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
  )

  return [serial_pub, serial_private]
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

  def __init__(self, id):
    keys = getKeys()
    self.id = id
    self.public_key = keys[0]
    self.private_key = keys[1]
    self.received_queue = []
    self.awaiting_queue = []
  
  

  def receive_packets(list_of_packets):
    self.received_queue = list_of_packets

  def shuffle(list_of_packets):
    random.shuffle(list_of_packets)

  def decrypt_and_send(list_of_packets):
    for packet in list_of_packets:
      #decryption goes here
      container = noise_creator()
      container.append(packet)
      shuffle(container)
      send_packet(container)


  
  def noise_creator():
    list_of_noise = []
    '''
      generating some fake packets here and fill the list up here
    '''
    return list_of_noise

  def send_packet(list):
    pass; 