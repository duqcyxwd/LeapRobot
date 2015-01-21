def converInHex(str):
  return ",".join("{:02x}".format(ord(char)) for char in str)
