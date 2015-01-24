
import time
import os
from os.path import dirname, abspath
parentdir = dirname(dirname(abspath(__file__)))
os.sys.path.insert(0,parentdir)

from  Model.HMobileArm import HMobileArm

hMobileArm = HMobileArm()

# time.sleep(1)
# hMobileArm.startLeapController()
hMobileArm.mw.on_newtab_pressed()
hMobileArm.run()
