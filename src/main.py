# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       pctom                                                        #
# 	Created:      8/18/2025, 3:30:38 PM                                        #
# 	Description:  Code For Team 33020B Vex V5 Competition Bot                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Brain should be defined by default
brain = Brain()
brain.screen.print("Good Luck Autodogs!! You got this!")

# The controller
controller = Controller()
controller.screen.print("Good Luck Autodogs!! You got this!")

cylinder_left = DigitalOut(brain.three_wire_port.g)
cylinder_right = DigitalOut(brain.three_wire_port.h)


# Arm motors
conveyor_belt_R = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
# One motor in the group is mounted opposite; keep this one non-reversed
conveyor_belt_L = Motor(Ports.PORT20, GearSetting.RATIO_18_1, True)
conveyor_belt_1 = MotorGroup(conveyor_belt_R, conveyor_belt_L)

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
    
    wait(5000)
    
    #Set motor Values
    drive_motor_group.set_velocity(70, PERCENT)
    right_drive_1.set_velocity(70, PERCENT)
    left_drive_1.set_velocity(70, PERCENT)
    conveyor_belt_1.set_velocity(70, PERCENT)
    
    #set cylinders to down
    cylinder_left.set(True)
    cylinder_right.set(True)
    
    #move bot in circle into feeder and get balls
    drive_motor_group.spin_for(FORWARD, 440)
    right_drive_1.spin_for(FORWARD, 1280)
    drive_motor_group.spin(FORWARD)
    wait(700)
    drive_motor_group.stop()
    conveyor_belt_1.spin(FORWARD)
    wait(2000)
    conveyor_belt_1.stop()
    
    #move away from feeder
    drive_motor_group.spin_for(FORWARD, -400)
    
    #set slower velocity
    right_drive_1.set_velocity(40, PERCENT)
    left_drive_1.set_velocity(40, PERCENT)
   
   #180 degree turn to face long goal
    right_drive_1.spin_for(FORWARD, 620, wait=False)
    left_drive_1.spin_for(REVERSE, 620, wait=True)
    
    
    #set velocities back to normal and go towards goal
    right_drive_1.set_velocity(70, PERCENT)
    left_drive_1.set_velocity(70, PERCENT)
    drive_motor_group.spin_for(FORWARD, 80)
    
    #activate cylinders
    cylinder_left.set(False)
    cylinder_right.set(False)
    wait(1000)
    
    #unload Balls Stored
    conveyor_belt_1.spin(REVERSE)
    wait(3000)
    conveyor_belt_1.stop()

    #back away from goal and turn 90 degress right
    drive_motor_group.spin_for(FORWARD, -200)
    right_drive_1.spin_for(REVERSE, 360, wait=False)
    left_drive_1.spin_for(FORWARD, 360, wait=True)
    
    #move towards center
    drive_motor_group.spin_for(FORWARD, 450)
    cylinder_left.set(True)
    cylinder_right.set(True)
    right_drive_1.spin_for(FORWARD, 360, wait=False)
    left_drive_1.spin_for(REVERSE, 360, wait=True)
    

    conveyor_belt_1.spin(FORWARD)
    drive_motor_group.set_velocity(30, PERCENT)
    drive_motor_group.spin_for(FORWARD, 400)
    
    wait(500)

    conveyor_belt_1.stop()
    conveyor_belt_1.spin(FORWARD)
    drive_motor_group.set_velocity(40, PERCENT)
    drive_motor_group.spin_for(FORWARD, 360)
    drive_motor_group.set_velocity(70, PERCENT)
    wait(1000)
    conveyor_belt_1.stop()

# Run the drive code
drive = Thread(drive_task)