import random
import json
import time


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

