#We shoudl probably call the received data packets instead of payload
#payload refers to the actual post message that the user sent

class Payload:
  def __init__(self, dest, content):
    self.dest = dest
    self.content = content