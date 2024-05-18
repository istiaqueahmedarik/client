import time
import pygame
import socketio
import keyboard
# import rospy
# from std_msgs.msg import int64MultiArray,String
from flask_cors import CORS
from flask import Flask,jsonify,request
from flask_socketio import SocketIO, emit
sio = socketio.Client()

DEADZONE = 50

# sio.connect('http://192.168.1.111:5476')
sio.connect('http://192.168.1.155:5476')

sio.on('connect', lambda: print('Connected to server'))
sio.on('disconnect', lambda: print('Disconnected from server'))
# sio.on('rover', lambda data: print(data.message))

# waypoints = [] 
def getMotorSpeed(x,y):
    if(x>1400 and x<1000 and (y>1600 or y<1600)):
        return (y,y)
    elif(y>1400 and y<1600):
        return (x,3000-x)
        
    

def calculate_motor_speeds(x, y):
    # Normalize joystick inputs to range -1 to 1
    normalized_x = (x - 1500) / 500
    normalized_y = (y - 1500) / 500

    # Compute motor speeds in the normalized range
    left_motor_speed = normalized_y + normalized_x
    right_motor_speed = normalized_y - normalized_x

    # Ensure motor speeds stay within the range -1 to 1
    left_motor_speed = max(min(left_motor_speed, 1), -1)
    right_motor_speed = max(min(right_motor_speed, 1), -1)

    # Determine if the joystick is in a pure forward or backward position
    is_forward_backward = abs(normalized_x) < 0.1

    # Scale down the speeds based on distance from the center for diagonal movement
    if not is_forward_backward:
        scale_factor = max(abs(normalized_x), abs(normalized_y))
        left_motor_speed *= (1 - 0.5 * scale_factor)
        right_motor_speed *= (1 - 0.5 * scale_factor)

    # Map normalized motor speeds to the range 1000 to 2000
    left_motor = (left_motor_speed + 1) * 500 + 1000
    right_motor = (right_motor_speed + 1) * 500 + 1000
    if((left_motor<1500+DEADZONE and left_motor>1500-DEADZONE) or (right_motor<1500+DEADZONE and right_motor>1500-DEADZONE)):
        left_motor = 1500
        right_motor = 1500
    return int(left_motor), int(right_motor)

def joystick():
    # rospy.init_node('joystickVal', anonymous=True)
    # pub = rospy.Publisher('joystick', String, queue_size=15)
    # rate = rospy.Rate(10)
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

    while True:
        l = False
        if(keyboard.is_pressed('l')):
            l = True
        pygame.event.pump()
        leftY = joystick.get_axis(3)
        leftX = joystick.get_axis(2)
        rightY = joystick.get_axis(1)
        rightX = joystick.get_axis(0)
        gripper_of = joystick.get_button(2)
        gripper_on = joystick.get_button(3)
        base = joystick.get_axis(4)
        lifter_mode = joystick.get_axis(5)
        speed_mode = joystick.get_button(1)
        lifter = joystick.get_axis(6)
        arm = joystick.get_button(0)
        # map from -1 to 1 to 1000 to 2000
        # leftMotor = (leftY+1)*500+1000
        leftY = int((leftY+1)*500+1000)
        leftX = int((leftX+1)*500+1000)
        rightY = int((rightY+1)*500+1000)
        rightX = int((rightX+1)*500+1000)
        arm = int((arm+1)*500+1000)
        base = int((base+1)*500+1000)
        speed_mode = int((speed_mode+1)*500+1000)
        lifter = int((lifter+1)*500+1000)
        lifter_mode = int((lifter_mode+1)*500+1000)
        light = int((l+1)*500+1000)
        gripper_of = int((1 - gripper_of) * 500 + 1000)
        gripper_on = int(gripper_on * 500 + 1500)
        gripper = gripper_on
        if(gripper_of!=1500):
            gripper = gripper_of



        # print(f"leftY: {leftY}, leftX: {leftX}, rightY: {rightY}, rightX: {rightX}, arm: {arm}, speed_mode: {speed_mode}, arm_mode: {arm_mode}, lifter: {lifter}")
        (leftMotor,rightMotor) = calculate_motor_speeds(rightX,rightY)
        # s = str(23)+s
        s = "["
        s += str(leftMotor)+","
        s += str(rightMotor)+","
        s += str(leftX)+","
        s += str(leftY)+","
        s+= str(base)+","
        s+=str(lifter)+","
        s+=str(gripper)+","
        s+=str(lifter_mode)+","
        s+=str(speed_mode)+","
        s+=str(arm)+","
        s+=str(light)
        s+="]"


        sio.emit('joystick_data', s)
        # left_motor,right_motor,leftX,leftY,DL,DR,DU,DD,LT,RT,B0,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10
        time.sleep(0.1)
        # rate.sleep()
        # 15(B) 16(x) 17(y)
        # 11 (DR)
        # 8 (DU)
        # 13

    

if __name__ == "__main__":
        joystick()


# [leftX,leftY,rightX,rightY,B0,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,DL,DR,DU,DD,LT,RT]