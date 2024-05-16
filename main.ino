#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Int64.h>
#include <std_msgs/Float64.h>
#include <SabertoothSimplified.h>

#define ST_ADDRESS 128 // Sabertooth address (default: 128)
#define MOTOR1 1       // Sabertooth motor 1
#define MOTOR2 2       // Sabertooth motor 2

SabertoothSimplified ST;

#include <std_msgs/Int64.h>
#include <array>
#include <string>
#include <sstream>
#include <vector>
ros::NodeHandle nh;

// Callback function to handle incoming joystick messages
void joystickCallback(const std_msgs::String &msg)
{

    // Access the joystick data from the message

    // fl.data = msg.data;
    std::string input = msg.data;
    std::vector<float> arr;
    std::istringstream iss(input.substr(1, input.length() - 2)); // Remove the enclosing brackets

    int num;
    char delimiter;
    while (iss >> num)
    {
        arr.push_back(num);
        iss >> delimiter;
    }

    // // vl.data = arr[0];
    // float yu = arr[3];
    // float yl = arr[2];
    // // Set motor 1 to move forward at full speed
    ST.motor(MOTOR1, constrain(map(arr[0], 1000, 2000, 127, -127), -127, 127));
    ST.motor(MOTOR2, constrain(map(arr[1], 1000, 2000, 127, -127), -127, 127));

    // // Set motor 2 to move backward at full speed
    // ST.motor(MOTOR2, yl);
    // vl.data = yu;
    // pub.publish(&msg);

    // Publish the new message
    while (!nh.connected())
    {
        nh.spinOnce();
    }
}

ros::Subscriber<std_msgs::String> joystickSub("joystick", &joystickCallback);

void setup()
{
    nh.initNode();
    nh.subscribe(joystickSub);
    // nh.subscribe(pxstateSub);
    // nh.subscribe(vstateSub);
    // nh.advertise(vals);
    // nh.advertise(pub);
    SabertoothTXPinSerial.begin(9600);
}

void loop()
{
    // vals.publish(&vl);
    // pub.publish(&fl);
    nh.spinOnce();
    // Add additional code here if needed
}
