import rospy
from std_msgs.msg import String
import threading

def publish_data():
    pub = rospy.Publisher('topic_name', String, queue_size=10)
    rate = rospy.Rate(10)  # Publish at 10 Hz
    while not rospy.is_shutdown():
        msg = String()
        msg.data = "Sample data"
        pub.publish(msg)
        print("Published data")
        rate.sleep()

def other_tasks():
    rate = rospy.Rate(10)  # Publish at 10 Hz

    for i in range(10):
        rospy.loginfo("Task %d" % i)
        rate.sleep()

if __name__ == '__main__':
    rospy.init_node('node_name')

    pub_thread = threading.Thread(target=publish_data)
    pub_thread.start()

    other_tasks()

    pub_thread.join()