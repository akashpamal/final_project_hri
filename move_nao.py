import csv
import math
import time
from naoqi import ALProxy

angles_list = []
with open('output_angles.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        angle_values = list(map(float, row))
        angles_list.append(angle_values)

# TRANQUILITY = "192.168.1.30"
TRANQUILITY = "172.0.0.1"
robot_port = 9559        

try:
    motionProxy = ALProxy("ALMotion", TRANQUILITY, robot_port)
except Exception as e:
    print("Could not create ALMotion proxy:", e)
    exit()


joint_names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw"]

interpolation_time = 1.0  # seconds for each command
times = [interpolation_time] * len(joint_names)  # Same duration for all joints

for i, angle_values in enumerate(angles_list):
    target_angles = []
    for j, joint in enumerate(joint_names):
        angle_deg = angle_values[j]
        angle_rad = math.radians(angle_deg)

        # angle_clamped = max(min(angle_rad, 1.5), -1.5)
        target_angles.append(angle_rad)
    
    # print(f"Sample {i}: Setting joints {joint_names} with target angles {target_angles} (radians)")
    # Use angleInterpolation to command the robot.
    # The parameters are:
    #   - joint_names: list of joints
    #   - target_angles: list of target angles (in radians)
    #   - times: list of durations (seconds) for the interpolation to complete
    #   - isAbsolute: True so that the angles are interpreted as absolute values.
    motionProxy.angleInterpolation(joint_names, target_angles, times, True)
        
    time.sleep(0.5)


print("All commands sent to the Nao robot.")
