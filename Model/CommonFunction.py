import math
# Convert number x in range x1 to x2 to range y1 to y2.
# If x is not in range [x1, x2], make it within range
# x1 could small than x2
def convertRatio(number, x1, x2, y1, y2):
    number = setValueWithinLimit(number, x1, x2)
    if y1 == y2:
        return y2
    res = (number - x1) * (x2 - x1) / (y2 - y1) + y1
    return res

def setValueWithinLimit(value, number1, number2):

    if number1 < number2:
        maxNum = number2
        minNum = number1
    else:
        maxNum = number1
        minNum = number2

    if value > maxNum:
        return maxNum
    elif value < minNum:
        return minNum
    else:
        return value

def setValueWithRange(value, range_value):
    return setValueWithinLimit(value, range_value, -range_value)

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


    alpha = round(alpha/math.pi*180.0, 3)
    angleBase = round(angleBase/math.pi*180.0, 3)
    beta = round(beta/math.pi*180.0, 3)

    return [alpha, beta, angleBase]


if __name__ == '__main__':
    # print calculateFromXYZToDegree(-8, 7, 0, 7, 7, 1 )
    print calculateFromXYZToDegree(-2-math.sqrt(3), -1+math.sqrt(3), 0, 2, 2, 1)
