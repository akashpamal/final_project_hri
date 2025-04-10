# %%
import cv2
import mediapipe as mp
import csv
import math
import pandas as pd
import json
import matplotlib.pyplot as plt
import requests

"""
Given a video file and sampling_frequency, finds the landmarks and writes them out to a json file
sampling_frequency of n means 1 in ever n frames is processed/saved

Returns the json object, also writes it to a file
"""
def process_video(video_in_file, json_out_file, sampling_frequency=3):
    cap = cv2.VideoCapture(video_in_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = -1
    
    landmarks_json = dict() # timestamp : [landmarks]
    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1
        
        timestamp = float(frame_count / fps) # timestamp in seconds of this frame
        
        if frame_count % sampling_frequency != 0: # only record body poses with sampling_frequency frequency
            # print('ignoring timestamp:', timestamp, 'params: timestamp', timestamp, 'sampling_frequency', sampling_frequency)
            # TODO debug this sampling frequency
            continue

        if not ret: # TODO make this more robust?
            break
        
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        result = pose.process(frame_rgb)

        # Draw the pose landmarks on the frame
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        landmarks = dict()
        for idx, landmark in enumerate(result.pose_world_landmarks.landmark):
            landmarks[mp_pose.PoseLandmark(idx).name] = [landmark.x, landmark.y, landmark.z]
        landmarks_json[timestamp] = landmarks
        # Display the frame
        cv2.imshow('MediaPipe Pose', frame)
        cv2.waitKey(33)

        # Exit if 'q' keypyt
    with open(json_out_file, 'w', encoding='utf-8') as json_file:
        json.dump(landmarks_json, json_file, ensure_ascii=False, indent=4)
    return landmarks_json

def mediapipe_to_nao_coords(mediapipe_coordinate):
    scale_factor = 1/3
    nao_coordinate = [mediapipe_coordinate[2] * scale_factor,
                  mediapipe_coordinate[1] * scale_factor,
                  -mediapipe_coordinate[0] * scale_factor]
    return nao_coordinate
    
def send_wrists_coords(landmarks):
    
    try:
        l_wrist_mediapipe = landmarks["LEFT_WRIST"]
        r_wrist_mediapipe = landmarks["RIGHT_WRIST"]
    except KeyError:
        print('No left wrist detected')
        return
    l_wrist_nao = mediapipe_to_nao_coords(l_wrist_mediapipe) + [0,0,0]
    r_wrist_nao = mediapipe_to_nao_coords(r_wrist_mediapipe) + [0,0,0]
    data = {
        # "key": "value"
        "movementType": "coordinate",
        'chainName': "LArm",
        'position': l_wrist_nao,  # Example coordinates
    }
    response = requests.post(url, json=data)
    

    # Print the server's response
    # print("Response status code:", response.status_code)
    # print('response:', response.text)
    # data = {
    #     # "key": "value"
    #     "movementType": "coordinate",
    #     'chainName': "RArm",
    #     'position': r_wrist_nao,  # Example coordinates
    # }
    # response = requests.post(url, json=data)
    
# %%
def process_camera_input():
    # Initialize MediaPipe Pose
    with mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, min_detection_confidence=0.5) as pose:
        cap = cv2.VideoCapture(0)  # Open the default camera (camera index 0)
        # landmarks_json = dict()  # Dictionary to store landmarks for each frame
        
        frame_count = -1
        
        while cap.isOpened():
            ret, frame = cap.read()
            frame_count += 1
            
            if not ret:
                print("Failed to capture frame. Continuing...")
                # break
            
            # Convert the frame to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame with MediaPipe Pose
            result = pose.process(frame_rgb)
            
            # If pose landmarks are detected, extract and store them
            if result.pose_landmarks:
                landmarks = dict()
                for idx, landmark in enumerate(result.pose_world_landmarks.landmark):
                    landmarks[mp_pose.PoseLandmark(idx).name] = [landmark.x, landmark.y, landmark.z]
                # print('landmarks:', landmarks)
                print('left_wrist', landmarks.get("LEFT_WRIST"))
                send_wrists_coords(landmarks)
                
                # Add the landmarks to the dictionary (using frame count as key)
                # landmarks_json[frame_count] = landmarks
                
                # Draw the pose landmarks on the frame
                mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            
            # Display the frame with landmarks drawn
            cv2.imshow('MediaPipe Pose', frame)
            
            # Exit if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Release the camera and close OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
        
        # Print the landmarks JSON
        # print(json.dumps(landmarks_json, indent=4))

# Initialize MediaPipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()
url = "http://127.0.0.1:5001/receive_json"

process_camera_input()
"""
landmarks_json = process_video(video_in_file='./movement.mov', json_out_file='landmarks.json') # also returns the json
times = sorted(landmarks_json.keys())
print('Times:', times) # lists each timestamp at which we have saved the body pose. This can be adjusted with the sampling_frequency parameter
l_wrist_poses = [landmarks_json[time]['LEFT_WRIST'] for time in times]
l_wrist_mediapipe_x = [elem[0] for elem in l_wrist_poses]
l_wrist_mediapipe_y = [elem[1] for elem in l_wrist_poses]
l_wrist_mediapipe_z = [elem[2] for elem in l_wrist_poses]

plt.plot(times, l_wrist_mediapipe_x, label='Left Wrist X')
plt.plot(times, l_wrist_mediapipe_y, label='Left Wrist Y')
plt.plot(times, l_wrist_mediapipe_z, label='Left Wrist Z')
plt.xlabel('Time (s)')
plt.ylabel('Left Wrist Position (m)')
plt.title('Mediapipe Left Wrist Position vs Time')
plt.legend()
plt.grid(True)
plt.show()


# Mediapipe axes:
# X axis points down
# Y axis to the left
# Z axis points forward
# 
# Nao axes:
# Z axis points up
# Y axis points to the left
X axis points forward


# Assume Nao is about 1/3rd of the height of a human
scale_factor = 1/3
l_wrist_nao_z = [-elem * scale_factor for elem in l_wrist_mediapipe_x]
l_wrist_nao_y = [elem * scale_factor + .2 for elem in l_wrist_mediapipe_y]
l_wrist_nao_x = [elem * scale_factor + .2 for elem in l_wrist_mediapipe_z]

with open("nao_coords.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "LarmX", "LarmY", "LArmZ"])
    for i in range(len(times)):
        row = [times[i], l_wrist_nao_x[i], l_wrist_nao_y[i], l_wrist_nao_z[i]]
        writer.writerow(row)
        
        
plt.plot(times, l_wrist_nao_x, label='Left Wrist X')
plt.plot(times, l_wrist_nao_y, label='Left Wrist Y')
plt.plot(times, l_wrist_nao_z, label='Left Wrist Z')
plt.xlabel('Time (s)')
plt.ylabel('Left Wrist Position (m)')
plt.title('Nao Left Wrist Position vs Time')
plt.legend()
plt.grid(True)
plt.show()
"""
# %%
