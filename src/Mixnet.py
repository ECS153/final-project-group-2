import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


import multiprocessing

from Node import Node
import json

'''
Mixnet wil be init once when te server is created. Then init the nodes and store them in a list. 

API:
  route_yo(destination, packet) -> send the packet to the 'destination' node
  post_to_blog(post) -> update datebase with new "post"
'''

class Mixnet:

  __instance = None

  def getInstance():
    if Mixnet.__instance != None:
      raise Exception("Mixnet has not been created yet!")
    return Mixnet.__instance

  def __init__(self, number_of_nodes):
    if Mixnet.__instance != None:
        raise Exception("There can only be one Mixnet. This class is a singleton!")
    else:
        Mixnet.__instance = self

    self.nodes = list()
    self.public_keys = list()
    self.node_process = list()

    # Populate list
    for i in range(number_of_nodes):
      keys = getKeys(i)
      # print(keys)
      self.nodes.append(Node(i, Mixnet.__instance, keys.get('private'), keys.get('public')))
      self.public_keys.append(self.nodes[i].public_key)
      self.node_process.append(multiprocessing.Process(target=self.nodes[i].main))

    # Start the processes
    for element in self.node_process:
      element.start()

    print("Create mixnet with {} nodes".format(number_of_nodes))
  
  # Method to send a payload to a node
  def route_to(self, dest, payload):
    self.nodes[dest].receive(payload)
    print("Sent payload to node{}".format(payload, dest))

  # Method to update database with new post
  def post_to_blog(self, post):
    # TODO: update DB
    print("Post {}".format(post))

  # Method to handle fisrt arrival
  def mixnet_gateway(self, packet):
    packetObj = json.loads(packet)
    next_nodeID = packetObj.get('next_url')
    content = packetObj.get("content")
    self.route_to(next_nodeID, content)


  '''
  Here is what I think:
  1. Post data being onion encrypted and sent off from server to first node
  2. Then the first node checks the packet and use to key to peel off the first layer of packet to find destination. This can be done by calling package[secret][dest]. 
  3. But since we don't need previous dest and key we can remove them and let package be only "secret:" to be sent off. It is like peeling of an onion as the packet traverse through the mixnet. 
  4. Perform this recursively and when we see secret[dest] == Not found, we know that it has reached its final destination 
  '''


# Function to generate asymmentric keys
def getKeys(id):
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

  # private key
  serial_private = private_key.private_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PrivateFormat.PKCS8,
      encryption_algorithm=serialization.NoEncryption()
  )
  with open('private_node{}.pem'.format(id), 'wb') as f: f.write(serial_private)
      
  # public key
  serial_pub = public_key.public_bytes(
      encoding=serialization.Encoding.PEM,
      format=serialization.PublicFormat.SubjectPublicKeyInfo
  )
  with open('public_node{}.pem'.format(id), 'wb') as f: f.write(serial_pub)

  return {'public':public_key, 'private':private_key}

#########      Private device only    ##########
def read_private (filename = 'private_noshare.pem'):
  with open(filename, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
      key_file.read(),
      password=None,
      backend=default_backend()
    )
  return private_key
                  
######### Public (shared) device only ##########
def read_public (filename = "public_shared.pem"):
  with open("public_shared.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
      key_file.read(),
      backend=default_backend()
    )
  return public_key