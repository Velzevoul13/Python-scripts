import cv2
import pandas
from datetime import datetime


base_frame = None   # This frame will be the base for all checks
status_list = [None, None]
movement_list = []
df = pandas.DataFrame(columns=["Start", "End"])

camera_feed = cv2.VideoCapture(0)   # Turning the camera on

while True:
    check, frame = camera_feed.read()   # Storing the captured frames to a variable.

    movement_status = 0

    gray_scale_feed = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # Converting the frames to gray scale
    gray_scale_feed = cv2.GaussianBlur(gray_scale_feed, (21, 21), 0)    # adding Gaussian blur to increase detail

    if base_frame is None:              # Storing to the base frame the first frame the camera captures
        base_frame = gray_scale_feed    # and ignoring all consequent frames
        continue

    delta_frame = cv2.absdiff(base_frame, gray_scale_feed)  # Calculate the difference of the base frame to all consequent
    threshold_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1] # Differences will be displayed as white pixels
    threshold_frame = cv2.dilate(threshold_frame, None, iterations=2)   # Broadening the white pixels area

    (cnts, _) = cv2.findContours(threshold_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find contours

    for contour in cnts:    # Checking for contours in the frames
        if cv2.contourArea(contour) < 1000:     # If they are bigger than 1000 pixels
            continue
        movement_status = 1

        (x, y, width, height) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 3)   # Draw a green rectangle
        status_list.append(movement_status)

        if status_list[-1] == 1 and status_list[-2] == 0:
            movement_list.append(datetime.now())
        if status_list[-1] == 0 and status_list[-2] == 1:
            movement_list.append(datetime.now())


    cv2.imshow("Live Camera Feed Gray Scale", gray_scale_feed)  # Showing the feed of all channels
    cv2.imshow("Delta Feed", delta_frame)
    cv2.imshow("Threshold Frame", threshold_frame)
    cv2.imshow("Live Camera Feed", frame)

    terminate_key = cv2.waitKey(1)
    if terminate_key == ord('q'):   # Terminating the application
        if movement_status == 1:
            movement_list.append(datetime.now())
        break

for i in range(0, len(movement_list), 2):
    df = df.append({"Start": movement_list[i], "End": movement_list[i+1]}, ignore_index=True)

df.to_csv("Movement_List.csv")

camera_feed.release()   # closing the camera
cv2.destroyAllWindows()     # Destroying any open window of the script
