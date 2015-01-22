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

def calculateFromXYZToDegree(x, y, z, l, k, h):

    z =-z

    angleBase = math.atan(z/x)

    x4 = x + h * math.cos(angleBase)
    y4 = y
    z4 = z + h * math.sin(angleBase)
    ps = x4 * x4 + y4 * y4 + z4 * z4
    p = math.sqrt(ps)
    alpha1 = math.acos(( k * k + ps - l * l) / 2.0 / k / p)
    alpha2 = math.asin(z4 / p)
    alpha = alpha1 - alpha2
    beta1 = math.acos((k * k + l * l - ps) / 2.0 / k / l)
    beta = beta1 + alpha - math.pi / 2.0


    alpha = alpha/math.pi*180.0
    print alpha

    return [angleBase/math.pi*180.0, alpha, beta/math.pi*180.0]


if __name__ == '__main__':
    print calculateFromXYZToDegree(-8, 7, 0, 7, 7, 1 )
