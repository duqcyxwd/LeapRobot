# This is a File Contains all the configuration data and All the Constant

# WIFI Configuration
LOCALHOST = ""
SERVER_PORT = 55555
RECEIVE_TIMEOUT = 0.5



INITSPEED = 0
# Constant for car 
MAX_SPEED_RANGE = 255/2

INITDIR = 1
INISERVOANGLE1 = 15 # 15.0 - 150.0   Left Servo, 
INISERVOANGLE2 = -30 # -30.0 - 90.0  Right Servo
INISERVOANGLE3 = 0 # 16.0 - 60.0	   BASE
INISERVOANGLE4 = 30 # -16.0 - 16.0   GRABBER


DATABUFFERSIZE = 1024

GRAPH_BUTTON_CHANGE_RATE = 10

CLIPPERMAX_HAND_LIMIT = 3
CLIPPERMIN_HAND_LIMIT = 8



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

# ==========  HARM   =============
# Constant for arm
CLIPPERMIN_PWM = 190
CLIPPERMAX_PWM = 140

