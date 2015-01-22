import math

def setValueWithinLimit(value, max, min):
    if value > max:
        return max
    elif value < min:
        return min
    else:
        return value

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

    x1 = z * 1.0
    y1 = y * 1.0
    z1 = x * 1.0

    l = l * 1.0
    k = k * 1.0
    h = h * 1.0

    # print [x, y, z, l, k, h] 
    if x1 == 0 or z > 0:
        return False
    angleBase = math.atan(z1/x1)

    x4 = x1 + h * math.cos(angleBase)
    y4 = y1
    z4 = z1 + h * math.sin(angleBase)
    ps = x4 * x4 + y4 * y4 + z4 * z4
    p = math.sqrt(ps)
    if  p < l - k or p > l + k:
        return False

    alpha1 = math.acos(( k * k + ps - l * l) / 2.0 / k / p)
    alpha2 = math.asin(y4 / p)



    alpha = alpha1 - alpha2
    beta1 = math.acos((k * k + l * l - ps) / 2.0 / k / l)
    beta = beta1 + alpha - math.pi / 2.0


    alpha = alpha/math.pi*180.0
    angleBase = angleBase/math.pi*180.0
    beta = beta/math.pi*180.0

    return [angleBase, alpha, beta]


if __name__ == '__main__':
    # print calculateFromXYZToDegree(-8, 7, 0, 7, 7, 1 )
    print calculateFromXYZToDegree(-2-math.sqrt(3), -1+math.sqrt(3), 0, 2, 2, 1)
