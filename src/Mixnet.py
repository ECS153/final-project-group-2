from Node import Node

'''
Mixnet wil be init once when te server is created. Then init the nodes and store them in a list. 

API:
  routeTo(destination, payload) -> send the payload to the 'destination' node
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

    # Create empty list to store Nodes
    self.nodes = list()
    # Create list to store public keys
    self.public_keys = list()

    # Populate list
    for i in range(number_of_nodes):
      self.nodes.append(Node(i, Mixnet.__instance))
      self.public_keys.append(self.nodes[i].public_key)

    print("Create mixnet with {} nodes".format(number_of_nodes))

  # Method to send a payload to a node
  def routeTo(self, dest, payload):
    self.nodes[dest].receive(payload)
    print("Sent {} to node{}".format(payload, dest))