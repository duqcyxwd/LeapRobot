# This is a File Contains all the configuration data and All the Constant

LOCALHOST=""
SERVER_PORT=55555

INITSPEED = 0
INITDIR = 1

INISERVOANGLE1 = 15.0 # 15.0 - 150.0   Left Servo, 
INISERVOANGLE2 = -30.0 # -30.0 - 90.0  Right Servo
INISERVOANGLE3 = 16.0 # 16.0 - 60.0	   Grabber
INISERVOANGLE4 = 10.0 # -16.0 - 16.0   Base

DATABUFFERSIZE = 1024

GRAPH_BUTTON_CHANGE_RATE = 10


# Constant for car 
# 
MAX_SPEED_RANGE = 255


# ==========  LEAP  =============
# Constant for leap celebration 
# Speed constant : change degree to speed.
LEFT_HAND_PITCH_RANGE = 30
LEFT_HAND_SPEED_CONSTANT = -1.0 * MAX_SPEED_RANGE / LEFT_HAND_PITCH_RANGE
LEFT_HAND_ROLL_RANGE = 30
LEFT_HAND_DIRECTION_CONSTANT = 20

LEFT_GRABLIMIT = 0.9
RIGHTHAND_SCALE = 1.0
RIGHTHAND_INITPOINT = [80 * RIGHTHAND_SCALE, 160 * RIGHTHAND_SCALE, 40 * RIGHTHAND_SCALE]
RIGHTHAND_SHIFT = [0, -20, 0]

# ==========  OpenGl  =============
FPS = 60
SMOOTH_UPDATE_MODEL = True
ARM_MOVE_SPEED = 6.0					# This only works if Smooth update model is true
ARM_MOVE_RATE = ARM_MOVE_SPEED/FPS		# This only works if Smooth update model is true

