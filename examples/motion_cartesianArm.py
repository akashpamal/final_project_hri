# -*- encoding: UTF-8 -*- 

'''Cartesian control: Arm trajectory example'''

import sys
import motion
import almath
from naoqi import ALProxy


def StiffnessOn(proxy):
  #We use the "Body" name to signify the collection of all joints
  pNames = "Body"
  pStiffnessLists = 1.0
  pTimeLists = 1.0
  proxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)


def main(robotIP):
    ''' Example showing a path of two positions
    Warning: Needs a PoseInit before executing
    '''

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

    # Send NAO to Pose Init
    postureProxy.goToPosture("StandInit", 0.5)

    effector   = "LArm"
    space      = motion.FRAME_ROBOT
    axisMask   = almath.AXIS_MASK_VEL    # just control position
    isAbsolute = True

    # Since we are in relative, the current position is zero
    currentPos = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    # Define the changes relative to the current position
    dx         =  0.00      # translation axis X (meters)
    dy         =  0.13     # translation axis Y (meters)
    dz         =  0.26      # translation axis Z (meters)
    dwx        =  -1.22      # rotation axis X (radians)
    dwy        =  0.52      # rotation axis Y (radians)
    dwz        =  0.01     # rotation axis Z (radians)
    
    # dx         =  0.12336114048957825      # translation axis X (meters)
    # dy         =  0.1323665827512741      # translation axis Y (meters)
    # dz         =  0.26347923278808594      # translation axis Z (meters)
    # dwx        =  -1.21964430809021      # rotation axis X (radians)
    # dwy        =  0.5219550132751465      # rotation axis Y (radians)
    # dwz        =  0.01353203784674406      # rotation axis Z (radians)
    targetPos  = [dx, dy, dz, dwx, dwy, dwz]
    
    pos1 = [0.14344285428524017, 0.13446059823036194, 0.5971754789352417, -1.6460217237472534, -0.9850037693977356, 0.2681563198566437]
    pos2 = [0.08367110043764114, 0.09527045488357544, 0.21045847237110138, -1.5316928625106812, 1.2437962293624878, -0.1373995989561081]

    # Go to the target and back again
    # path       = [targetPos, currentPos]
    path       = [pos1, pos2]
    times      = [3.0, 6.0] # seconds

    # currPos = motionProxy.getPosition(effector, space, isAbsolute)
    # print currPos
    
    motionProxy.positionInterpolation(effector, space, path,
                                      axisMask, times, isAbsolute)


if __name__ == "__main__":
    robotIp = "192.168.1.30"
    # robotIp = "172.0.0.1"

    if len(sys.argv) <= 1:
        print "Usage python motion_cartesianArm1.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
