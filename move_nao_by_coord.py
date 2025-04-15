'''Cartesian control: Arm trajectory example'''

import sys
import motion
import almath
from naoqi import ALProxy
import codecs
import csv
import unicodedata
import time
from datetime import datetime
from datetime import timedelta

from flask import Flask, request, jsonify
app = Flask(__name__)

def StiffnessOn(proxy):
  #We use the "Body" name to signify the collection of all joints
  pNames = "Body"
  pStiffnessLists = 1.0
  pTimeLists = 1.0
  proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
  pNames = "LArm"
  proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
  pNames = "RArm"
  proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)
  pNames = "Head"
  proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def setup(robotIP):
    ''' Example showing a path of two positions
    Warning: Needs a PoseInit before executing
    '''

    global motionProxy
    # Init proxies.
    try:
        motionProxy = ALProxy("ALMotion", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    # Set NAO in Stiffness On
    StiffnessOn(motionProxy)
    postureProxy.goToPosture("StandInit", 0.5)
    

    # # Enable collision detection on LArm chain.
    pEnable = True
    success = motionProxy.setCollisionProtectionEnabled('LArm', pEnable)
    success = motionProxy.setCollisionProtectionEnabled('RArm', pEnable)

    # # Send NAO to Pose Init
    return motionProxy

def move_coord(chainName, position, fractionMaxSpeed=0.8):
    # Example showing how to set LArm Position, using a fraction of max speed
    # chainName = "LArm"
    space     = motion.FRAME_TORSO
    # axisMask         = 7 # just control position
    axisMask         = almath.AXIS_MASK_X + almath.AXIS_MASK_Y + almath.AXIS_MASK_Z
    # axisMask         = almath.AXIS_MASK_Y + almath.AXIS_MASK_Z
    chainName = unicodedata.normalize('NFKD', chainName).encode('ascii', 'ignore')
    print('moving', chainName, 'to', position)
    
    # chainName = "LArm"
    frame     = motion.FRAME_TORSO
    useSensor = False

    # Get the current position of the chainName in the same frame
    current = motionProxy.getPosition(chainName, frame, useSensor)
    # position[0] = current[0]
    # position[1] = current[1]
    # position[2] = current[2]
    motionProxy.setPosition(chainName, space, position, fractionMaxSpeed, axisMask)
    
    # Write desired, current to a CSV file
    # with open('positions.csv', 'a') as f:
    #     writer = csv.writer(f)
    #     writer.writerow([desired[0], desired[1], desired[2], current[0], current[1], current[2]])
    print ('desired_position:', position)
    print ('current_position:', current)

# def move_angle()

@app.route('/receive_json', methods=['POST'])
def receive_json():
    # Parse JSON data from the request
    data = request.get_json()
    

    if data['movementType'] == 'coordinate':
        chainName = data['chainName']
        position = data['position']
        # print('chainName', type(chainName), chainName)
        # print('position', type(position), position)
        move_coord(chainName, position)
    elif data['movementType'] == 'coordinate':
        pass
    else:
        print('movementType', data['movementType'], 'not yet implemented')
    
    # chainName = "LArm"
    # frame     = motion.FRAME_TORSO
    # useSensor = False
    # curr_pos = motionProxy.getPosition(chainName, frame, useSensor)
    # past_positions.append(curr_pos)
        
    return jsonify({"status": "success", "received_data": data}) # Respond with a success message

motionProxy = None
past_positions = []

if __name__ == "__main__":
    robotIp = "192.168.1.30"
    setup(robotIp) # initializes motionProxy variable

    app.run(port=5001)
    """
    {
        "movement_type": "coordinate" // or "angle",
        "joint_name": "LShoulderRoll",
        "joint_angles": [0.5, 0.6, 0.7], // or "joint_coordinates": [0.1, 0.2, 0.3]
    }
    """
