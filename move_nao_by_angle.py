import csv
import math
import time
from naoqi import ALProxy
import codecs

angles_data = []

csv_path = 'C:/Users/ishah/OneDrive/Documents/HRI/final_project_hri/nao_angles.csv'

# Supply fieldnames manually since the CSV file has no header row.
fieldnames = ["Time", "RShoulderRoll", "LShoulderRoll"]

with codecs.open(csv_path, 'r', 'utf-8-sig') as f:
    reader = csv.DictReader(f, fieldnames=fieldnames, skipinitialspace=True)
    # Optionally print the fieldnames to verify
    print("CSV Fieldnames:", reader.fieldnames)
    for row in reader:
        angles_data.append(row)

# Verify that the keys are as expected.
if angles_data:
    print("Keys in first row:", angles_data[0].keys())
else:
    print("No rows found in CSV!")

TRANQUILITY = "192.168.1.30"
# TRANQUILITY = "172.0.0.1"
robot_port = 9559        

try:
    motionProxy = ALProxy("ALMotion", TRANQUILITY, robot_port)
except Exception as e:
    print("Could not create ALMotion proxy:", e)
    exit()

# Wake up the robot (activates the motors).
motionProxy.wakeUp()
# Optionally, set stiffness for the specific joints.
joint_names = ["RShoulderRoll", "LShoulderRoll"]
# motionProxy.setStiffnesses(["RShoulderPitch"], 1.0)
motionProxy.setStiffnesses(joint_names, 1.0)

interpolation_time = 0.3  # seconds for each command
times = [interpolation_time] * len(joint_names)  # Same duration for all joints

for i, row in enumerate(angles_data):
    t_val = float(row["Time"])

    r_shoulder_deg = float(row["RShoulderRoll"])
    l_shoulder_deg = float(row["LShoulderRoll"])

    # Convert degree values to radians.
    r_shoulder_rad = math.radians(r_shoulder_deg)
    l_shoulder_rad = math.radians(l_shoulder_deg)
    
    target_angles_deg = [r_shoulder_deg, l_shoulder_deg]
    target_angles_rad = [r_shoulder_rad, l_shoulder_rad]
    print("Sample", i, "Time:", t_val, "Target angles (degrees):", target_angles_deg)
    
    # Command the robot to move to the given angles.
    motionProxy.angleInterpolation(joint_names, target_angles_rad, 0.1, True)
    
    time.sleep(0.05)

# for i, angle_values in enumerate(angles_list):
#     target_angles = []
#     for j, joint in enumerate(joint_names):
#         angle_deg = angle_values[j]
#         angle_rad = math.radians(angle_deg)

#         # angle_clamped = max(min(angle_rad, 1.5), -1.5)
#         target_angles.append(angle_rad)
    
    # print(f"Sample {i}: Setting joints {joint_names} with target angles {target_angles} (radians)")
    # Use angleInterpolation to command the robot.
    # The parameters are:
    #   - joint_names: list of joints
    #   - target_angles: list of target angles (in radians)
    #   - times: list of durations (seconds) for the interpolation to complete
    #   - isAbsolute: True so that the angles are interpreted as absolute values.

    # Test a simple movement on one joint to see if the robot responds.
    # motionProxy.angleInterpolation("RShoulderPitch", math.radians(20), 1.0, True)
    # limits = motionProxy.getLimits("LShoulderRoll")
    # print("RShoulderPitch limits:", limits)
    # Command the robot to move the right shoulder with a more extreme angle
    # motionProxy.angleInterpolation("LShoulderPitch", math.radians(60), 1.0, True)
    # motionProxy.angleInterpolation("LShoulderRoll", math.radians(0), 1.0, True)
    # motionProxy.angleInterpolation("LShoulderPitch", math.radians(60), 1.0, True)



    # motionProxy.angleInterpolation(joint_names, target_angles, times, True)
        
    # time.sleep(0.5)


print("All commands sent to the Nao robot.")
