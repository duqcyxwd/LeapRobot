from  main_run import LeapArm
import time


leapArm = LeapArm()

# time.sleep(1)
# leapArm.startLeapController()
leapArm.mw.on_newtab_pressed()
leapArm.run()
