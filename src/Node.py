# Module from encryption
import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

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


class Node:

  def __init__(self):
    keys = getKeys()
    self.public_key = keys[0]
    self.private_key = keys[1]