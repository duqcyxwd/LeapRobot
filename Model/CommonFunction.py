import math

def converInHex(str):
  return ",".join("{:02x}".format(ord(char)) for char in str)

# Approach num to num2
def approach(num, num2, appoachRate):
    if num != num2:
        dif =  math.fabs(num - num2)
        if dif < appoachRate:
            num = num2
        elif num > num2:
            num -= appoachRate
        elif num < num2:
            num += appoachRate
    return num
