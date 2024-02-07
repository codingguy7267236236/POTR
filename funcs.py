import json
from datetime import datetime, timedelta
import bcrypt

class JSON():

  def __init__(self, path):
    self.path = path
    with open(self.path, "r") as f:
      self.data = json.load(f)
      f.close()

  def save(self):
    with open(self.path, 'w') as file:
      json.dump(self.data, file)
      file.truncate()
      file.close()



#function to hash encrypt passwords.
def hashPassword(pw,salt=None):
  bytes = pw.encode('utf-8')
  #if no salt passed then generate one
  if salt == None:
    salt = bcrypt.gensalt()
  #if salt provided (string format)
  else:
    salt = salt.encode("utf-8")
  
  #hasing with salt
  hash = bcrypt.hashpw(bytes,salt)
  return hash,salt


#checking hashed passwords match
def checkEncryption(pw,stored,salt):
  #stored
  #hash = hashPassword(stored)
  #hash = stored.encode("utf-8")

  #entered password
  userBytes,salt = hashPassword(pw,salt)
  userBytes = userBytes.decode("utf-8")
  #userBytes = pw

  #checking
  result = False
  if stored == userBytes:
    result = True
  #result = bcrypt.checkpw(userBytes,hash)
  return result