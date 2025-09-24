from vex import *

brain = Brain()
controller = Controller()

# Motors
conveyor_belt_1 = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)   # R1/R2
conveyor_belt_2 = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)   # A/B
left_drive_1  = Motor(Ports.PORT1,  GearSetting.RATIO_18_1, False)
right_drive_1 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)

# Pneumatics on Brain 3-wire G & H (together)
pneu_g = DigitalOut(brain.three_wire_port.g)
pneu_h = DigitalOut(brain.three_wire_port.h)

pneu_on = False  # latched state

def apply_pneumatics():
    pneu_g.set(pneu_on)
    pneu_h.set(pneu_on)

def drive_task():
    global pneu_on
    prev_L1 = False
    prev_L2 = False
    apply_pneumatics()

    while True:
        # full-speed tank (removed /2)
        drive_left  = controller.axis3.position()
        drive_right = controller.axis2.position()

        # deadband
        deadband = 5
        if abs(drive_left)  < deadband: drive_left  = 0
        if abs(drive_right) < deadband: drive_right = 0

        # conveyors
        if controller.buttonR1.pressing():
            conveyor_belt_1.spin(FORWARD, 100, PERCENT)
        elif controller.buttonR2.pressing():
            conveyor_belt_1.spin(REVERSE, 100, PERCENT)
        else:
            conveyor_belt_1.stop()

        if controller.buttonA.pressing():
            conveyor_belt_2.spin(FORWARD, 100, PERCENT)
        elif controller.buttonB.pressing():
            conveyor_belt_2.spin(REVERSE, 100, PERCENT)
        else:
            conveyor_belt_2.stop()

        # PNEUMATICS (SWAPPED): L1 = OFF, L2 = ON (latched, no momentary)
        L1_now = controller.buttonL1.pressing()
        L2_now = controller.buttonL2.pressing()

        if L1_now and not prev_L1:   # L1 pressed -> both OFF
            pneu_on = False
            apply_pneumatics()

        if L2_now and not prev_L2:   # L2 pressed -> both ON
            pneu_on = True
            apply_pneumatics()

        prev_L1 = L1_now
        prev_L2 = L2_now

        # drivetrain (full stick = full speed)
        left_drive_1.spin(FORWARD,  drive_left,  PERCENT)
        right_drive_1.spin(FORWARD, drive_right, PERCENT)

        sleep(20)

drive = Thread(drive_task)
