# This is a File Contains all the configuration data and All the Constant

# WIFI Configuration
LOCALHOST = ""
SERVER_PORT = 55555
RECEIVE_TIMEOUT = 0.2




# ==========  Car  =============
INITSPEED = 0
MAX_SPEED_RANGE = 255/3
MINIMOVESPEED = 30

INITDIR = 1
INISERVOANGLE1 = 15 # 15.0 - 150.0   Left Servo, 
INISERVOANGLE2 = -30 # -30.0 - 90.0  Right Servo
INISERVOANGLE3 = 0 # 16.0 - 60.0	   BASE
INISERVOANGLE4 = 50 # -16.0 - 16.0   GRABBER
CYLINDERDENSITY = 50 # Density of rectangles surrording cylinder


DATABUFFERSIZE = 1024

GRAPH_BUTTON_CHANGE_RATE = 10

CLIPPERMAX_HAND_LIMIT = 3
CLIPPERMIN_HAND_LIMIT = 7



# ==========  LEAP  =============
# Constant for leap celebration 
# Speed constant : change degree to speed.
# Set Pitch from -30 to 30
GESTUREENABLE = False
LEFT_HAND_PITCH_RANGE = 30
LEFT_HAND_SPEED_CONSTANT = -1.0 * MAX_SPEED_RANGE / LEFT_HAND_PITCH_RANGE

# Set Pitch from -30 to 30
LEFT_HAND_ROLL_RANGE = 30
LEFT_HAND_DIRECTION_CONSTANT = 10

LEFT_GRABLIMIT = 0.9
RIGHTHAND_SCALE = 1.0

R1 = 80
R2 = 160
R3 = 120
RIGHTHAND_INITPOINT = [R1 * RIGHTHAND_SCALE, R2 * RIGHTHAND_SCALE, R3 * RIGHTHAND_SCALE]
RIGHTHAND_SHIFT = [0, -20, 0]

# ==========  OpenGl  =============
CLIPPERMIN = 16
CLIPPERMAX = 86
FPS = 60
SMOOTH_UPDATE_MODEL = True
ARM_MOVE_SPEED = 6.0					# This only works if Smooth update model is true
ARM_MOVE_RATE = ARM_MOVE_SPEED/FPS		# This only works if Smooth update model is true

ARM_HORIZONTAL_W = 3.0    # length of horizontal arm
ARM_VERTICAL_L = 7.0    # length of vertical arm
ARM_HORIZONTAL_K = 6.0    # length of horizontal extension
HAND_LENGTH_H = 2.0    # hand length
BASE_CONNECTION_B = 4.0    # base connection length
GRABBER_LENGTH_P = 2.0    # piter length

LEFTSERVOMIN = -10
LEFTSERVOMAX = 90

RIGHTSERVOMIN = -60
RIGHTSERVOMAX = 90

BOTSERVOMIN = -90
BOTSERVOMAX = 90


# ==========  HARM   =============
# Constant for arm

LEFTSERVOMIN_PWN = 390
LEFTSERVOMAX_PWN = 620

RIGHTSERVOMIN_PWN = 140
RIGHTSERVOMAX_PWN = 340

BOTSERVOMIN_PWN = 160
BOTSERVOMAX_PWN = 560

CLIPPERMIN_PWM = 190
CLIPPERMAX_PWM = 140

LEFTMIFPOINT = 497
RIGHTMIDPOINT = 284
BOTMIDPOINT = 369

MINANGLEDIF = 20

