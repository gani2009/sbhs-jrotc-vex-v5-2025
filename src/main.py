# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       pctom                                                        #
# 	Created:      8/18/2025, 3:30:38 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Brain should be defined by default
brain = Brain()

# The controller
controller = Controller()

cylinder_left = DigitalOut(brain.three_wire_port.g)
cylinder_right = DigitalOut(brain.three_wire_port.h)


# Arm motors
conveyor_belt_1 = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)


# Drive motors
left_drive_1 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_drive_1 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
drive_motor_group = MotorGroup(left_drive_1, right_drive_1)

# Max motor speed (percent) for motors controlled by buttons
MAX_SPEED = 100

#
# All motors are controlled from this function which is run as a separate thread
#
def drive_task():
    drive_left = 0
    drive_right = 0
    
    cylinder_left.set(False)
    cylinder_right.set(False)

    # loop forever
    while True:
        brain.screen.clear_screen()
        brain.screen.set_cursor(1,1)
        

        # joystick tank control
        try:
            drive_left = (controller.axis3.position() / 21.5)*(controller.axis3.position() / 21.5)*(controller.axis3.position() / 21.5)*((controller.axis3.position()*controller.axis3.position())/abs(controller.axis3.position()*controller.axis3.position()))
        except ZeroDivisionError:
            drive_left = 0
        try:
            drive_right = (controller.axis2.position() / 21.5)*(controller.axis2.position() / 21.5)*(controller.axis2.position() / 21.5)*((controller.axis2.position()*controller.axis2.position())/abs(controller.axis2.position()*controller.axis2.position()))
        except ZeroDivisionError:
            drive_right = 0
        brain.screen.print(drive_left)
        brain.screen.new_line()
        brain.screen.print(drive_right)
        # button control
        # lower conveyor belt
        if (controller.buttonR1.pressing()):
            conveyor_belt_1.spin(FORWARD, 100, PERCENT)
        elif (controller.buttonR2.pressing()):
            conveyor_belt_1.spin(REVERSE, 100, PERCENT)
        else:
            conveyor_belt_1.stop()
            
        if (controller.buttonL2.pressing()):
            cylinder_left.set(True)
            cylinder_right.set(True)
        elif (controller.buttonL1.pressing()):
            cylinder_left.set(False)
            cylinder_right.set(False)

        # threshold the variable channels so the drive does not
        # move if the joystick axis does not return exactly to 0
        deadband = 5
        if abs(drive_left) < deadband:
            drive_left = 0
        if abs(drive_right) < deadband:
            drive_right = 0

        # Now send all drive values to motors

        # The drivetrain
        left_drive_1.spin(FORWARD, drive_left, PERCENT)
        right_drive_1.spin(FORWARD, drive_right, PERCENT)
        # No need to run too fast
        sleep(20)

def autonomous():
    cylinder_left.set(True)
    cylinder_right.set(True)
    drive_motor_group.spin_for(FORWARD, 540)
    right_drive_1.spin_for(FORWARD, 1240)
    drive_motor_group.spin(FORWARD, 50, PERCENT)
    wait(1000)
    drive_motor_group.stop()
    conveyor_belt_1.spin_for(FORWARD, 1000)
    
    drive_motor_group.spin_for(FORWARD, -400)
    right_drive_1.spin_for(FORWARD, 650, wait=False)
    left_drive_1.spin_for(REVERSE, 650, wait=True)
    drive_motor_group.spin_for(FORWARD, 90)
    
    cylinder_left.set(False)
    cylinder_right.set(False)
    
    conveyor_belt_1.spin_for(REVERSE, 1000)

# Run the drive code
drive = Thread(autonomous)

# Python now drops into REPL
