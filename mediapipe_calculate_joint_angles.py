import cv2
import mediapipe as mp
import csv
import math

def find_angle(point1, point2):
    # return the angles in the x, y, and z directions
    vector = (point2.x - point1.x, point2.y - point1.y, point2.z - point1.z)
    magnitude = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    
    cos_theta_x = vector[0] / magnitude
    cos_theta_y = vector[1] / magnitude
    cos_theta_z = vector[2] / magnitude
    
    theta_x = math.degrees(math.acos(cos_theta_x))
    theta_y = math.degrees(math.acos(cos_theta_y))
    theta_z = math.degrees(math.acos(cos_theta_z))
    return theta_x, theta_y, theta_z

def write_landmarks_to_csv(landmarks, timestamp, csv_data):
    print(f"Landmark coordinates for frame {timestamp}:")
    for idx, landmark in enumerate(landmarks):
        print(f"idx: {idx}, {mp_pose.PoseLandmark(idx).name}: (x: {landmark.x}, y: {landmark.y}, z: {landmark.z})")
        csv_data.append([timestamp, mp_pose.PoseLandmark(idx).name, landmark.x, landmark.y, landmark.z])
    print("\n")

def get_angles(cap, point1_idx, point2_idx, angle_idces):
    frame_count = 0
    fps = cap.get(cv2.CAP_PROP_FPS)

    csv_data = []
    r_arm_angles = []

    while cap.isOpened():
        ret, frame = cap.read()
        frame_count += 1
        timestamp = int(frame_count / fps) # timestamp in seconds of this frame
        if not ret:
            break
        
        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe Pose
        result = pose.process(frame_rgb)
        print('processed results')

        # Draw the pose landmarks on the frame
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Add the landmark coordinates to the list and print them
            write_landmarks_to_csv(result.pose_landmarks.landmark, timestamp, csv_data)
            point1 = result.pose_landmarks.landmark[point1_idx] # Assumes that NAO torso is perfectly upright
            point2 = result.pose_landmarks.landmark[point2_idx]
            angles = find_angle(point1, point2)
            wanted_angles = [angles[elem] for elem in angle_idces]
            r_arm_angles.append(wanted_angles)
        
        # Display the frame
        # cv2.imshow('MediaPipe Pose', frame)

        # Exit if 'q' keypyt


video_path = './r_arm.mov'
output_csv = './video_output.txt'

# Initialize MediaPipe Pose and Drawing utilities
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose()

# Open the video file
cap = cv2.VideoCapture(video_path)

shoulder_pitches = get_angles(cap, mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW, [0])


# write csv_data to the file
# with open(output_csv, 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerow(['Frame', 'Landmark', 'X', 'Y', 'Z'])
#     writer.writerows(csv_data)

# with open('output_angles_2.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(r_arm_angles)