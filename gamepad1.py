import pygame
import rospy
from std_msgs.msg import Float64MultiArray,String
from flask_cors import CORS
from flask import Flask,jsonify,request
from flask_socketio import SocketIO, emit


waypoints = [] 

def get_motor_speeds(right_stick_x, right_stick_y, left_stick_x):
    if(left_stick_x<1498 or left_stick_x>1502):
        if(left_stick_x<1498):
            return (1300,1700)
        else:
            return (1700,1300)
    
    left_speed = right_stick_y
    right_speed = right_stick_y
    if(right_stick_y<1498 and right_stick_y <1498):
        left_speed=1300
        right_speed=1300
    elif(right_stick_y>1502 and right_stick_y>1502):
        left_speed=1700
        right_speed=1700
    print(f"right_stick_x: {right_stick_x}; right_stick_y: {right_stick_y}")
    if(right_stick_y<1499 and right_stick_x<1499):
        right_speed = 1300
        left_speed = 1200
    elif(right_stick_y<1499 and right_stick_x>1501):
        left_speed = 1300
        right_speed = 1200
    elif(right_stick_y>1501 and right_stick_x<1499):
        left_speed = 1600
        right_speed = 1700
    elif(right_stick_y>1501 and right_stick_x>1501):
        left_speed = 1700
        right_speed = 1600
    
    return (int(left_speed),int(right_speed))
def joystick():
    rospy.init_node('joystickVal', anonymous=True)
    pub = rospy.Publisher('joystick', String, queue_size=15)
    rate = rospy.Rate(10)
    pygame.init()
    pygame.joystick.init()

    if pygame.joystick.get_count() == 0:
        print("No joystick detected.")
        return

    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print("Initialized joystick:", joystick.get_name())

    axes = joystick.get_numaxes()
    buttons = joystick.get_numbuttons()

    print("Number of axes:", axes)
    print("Number of buttons:", buttons)

    # Initialize previous values
    prev_values = {
        "left_stick_x": 0,
        "left_stick_y": 0,
        "right_stick_x": 0,
        "right_stick_y": 0,
        "LT": 0,
        "RT": 0,
        "DPad_up": 0,
        "DPad_down": 0,
        "DPad_left": 0,
        "DPad_right": 0,
        "buttons": [0] * buttons  # Initialize to zeros for all buttons
    }

    while True:
        pygame.event.pump()

        # Read current values
        left_stick_x = joystick.get_axis(0)
        left_stick_y = joystick.get_axis(1)
        right_stick_x = joystick.get_axis(3)
        right_stick_y = joystick.get_axis(4)
        LT = joystick.get_axis(2)
        RT = joystick.get_axis(5)
        DPad_up = joystick.get_hat(0)[1]
        DPad_down = -joystick.get_hat(0)[1]
        DPad_left = -joystick.get_hat(0)[0]
        DPad_right = joystick.get_hat(0)[0]
        current_buttons = [joystick.get_button(i) for i in range(buttons)]

        # Check for changes and print if there are any
        changes_detected = False

        if (left_stick_x, left_stick_y) != (prev_values["left_stick_x"], prev_values["left_stick_y"]):
            print(f"Left Stick: xval={left_stick_x:.2f}; yval={left_stick_y:.2f}")
            changes_detected = True

        if (right_stick_x, right_stick_y) != (prev_values["right_stick_x"], prev_values["right_stick_y"]):
            print(f"Right Stick: xval={right_stick_x:.2f}; yval={right_stick_y:.2f}")
            changes_detected = True

        if LT != prev_values["LT"]:
            print(f"LT={LT:.2f}")
            changes_detected = True

        if RT != prev_values["RT"]:
            print(f"RT={RT:.2f}")
            changes_detected = True

        if DPad_up != prev_values["DPad_up"]:
            print("DPad Up pressed" if DPad_up == 1 else "DPad Up released")
            changes_detected = True

        if DPad_down != prev_values["DPad_down"]:
            print("DPad Down pressed" if DPad_down == 1 else "DPad Down released")
            changes_detected = True

        if DPad_left != prev_values["DPad_left"]:
            print("DPad Left pressed" if DPad_left == 1 else "DPad Left released")
            changes_detected = True

        if DPad_right != prev_values["DPad_right"]:
            print("DPad Right pressed" if DPad_right == 1 else "DPad Right released")
            changes_detected = True

        for i in range(buttons):
            if current_buttons[i] != prev_values["buttons"][i]:
                print(f"Button {i} {'pressed' if current_buttons[i] == 1 else 'released'}")
                changes_detected = True

        if changes_detected:
            print()  # Add a blank line between different changes

        # Update previous values
        prev_values["left_stick_x"] = left_stick_x
        prev_values["left_stick_y"] = left_stick_y
        prev_values["right_stick_x"] = right_stick_x
        prev_values["right_stick_y"] = right_stick_y
        prev_values["LT"] = LT
        prev_values["RT"] = RT
        prev_values["DPad_up"] = DPad_up
        prev_values["DPad_down"] = DPad_down
        prev_values["DPad_left"] = DPad_left
        prev_values["DPad_right"] = DPad_right
        prev_values["buttons"] = current_buttons
        msg = String()
        left_stick_x = int((left_stick_x + 1) * 500 + 1000)
        left_stick_y = int((left_stick_y + 1) * 500 + 1000)
        right_stick_x = int((right_stick_x + 1) * 500 + 1000)
        right_stick_y = int((right_stick_y + 1) * 500 + 1000)
        (left_motor, right_motor) = get_motor_speeds(right_stick_x,right_stick_y,left_stick_x)
        print(f"Left Motor: {left_motor}; Right Motor: {right_motor}")
        LT = float((LT + 1) * 500 + 1000)
        RT = float((RT + 1) * 500 + 1000)
        DPad_up = float((DPad_up + 1) * 500 + 1000)
        DPad_down = float((DPad_down + 1) * 500 + 1000)
        DPad_left = float((DPad_left + 1) * 500 + 1000)
        DPad_right = float((DPad_right + 1) * 500 + 1000)
        for i in range(11):
            current_buttons[i] = 2000 if current_buttons[i]==1 else 1000
        msg.data = ','.join([str(left_stick_x), str(left_stick_y), str(right_stick_x), str(right_stick_y), str(current_buttons[0]), str(current_buttons[1]), str(current_buttons[2]), str(current_buttons[3]), str(current_buttons[4]), str(current_buttons[5]), str(current_buttons[6]), str(current_buttons[7]), str(current_buttons[8]), str(current_buttons[9]), str(current_buttons[10]), str(DPad_left), str(DPad_right), str(DPad_up), str(DPad_down), str(LT), str(RT)])
        # print(msg.data)
        pub.publish(str(left_motor)+","+str(right_motor))
        
        rate.sleep()

    

if __name__ == "__main__":
        joystick()


# [leftX,leftY,rightX,rightY,B0,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,DL,DR,DU,DD,LT,RT]