import cv2
import time
import glob
import os
from emailing import send_email
from threading import Thread

# Open the video capture from the default camera (camera index 0)
video = cv2.VideoCapture(0)

# Allow some time for the camera to warm up
time.sleep(1)

# Initialize a variable to store the first frame for reference
first_frame = None
status_list = []
count = 1

def clean_folder():
    """
    Function to clean the 'images' folder by removing all PNG files.
    """
    print('Cleaning folder....')
    images = glob.glob('images/*.png')
    for image in images:
        os.remove(image)
    print('Folder has been cleaned')


# Infinite loop to capture and process frames from the webcam
while True:
    status = 0
    # Read a frame from the webcam
    check, frame = video.read()
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to the grayscale frame
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    # If it's the first frame, store it as the reference frame
    if first_frame is None:
        first_frame = gray_frame_gau

    # Calculate the absolute difference between the current frame and the reference frame
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    # Apply a binary threshold to the difference frame
    thresh_frame = cv2.threshold(delta_frame, 55, 255, cv2.THRESH_BINARY)[1]
    # Perform dilation on the threshold frame
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    # Display the dilated frame with moving object outlines
    cv2.imshow('Webcam Video', dil_frame)

    # Find contours in the dilated frame
    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the detected contours
    for contour in contours:
        # If the contour area is smaller than 5000 pixels, skip it
        if cv2.contourArea(contour) < 5000:
            continue
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(contour)
        # Draw a green rectangle around the detected object
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            cv2.imwrite(f"images/{count}.png", frame)
            count = count + 1
            all_images = glob.glob('images/*.png')
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]

    # Append the current status (0 or 1) to the status list
    status_list.append(status)
    # Keep only the last two elements in the status list
    status_list = status_list[-2:]

    # Check if the status transitioned from 1 (object detected) to 0 (no object detected)
    if status_list[0] == 1 and status_list[1] == 0:
        # Create a new thread to send an email with the image containing the detected object
        email_thread = Thread(target=send_email, args=(image_with_object,))
        # Set the email thread as a daemon thread, which will terminate if the main program exits
        email_thread.daemon = True
        # Create a new thread to clean the images folder
        clean_thread = Thread(target=clean_folder)
        # Set the clean folder thread as a daemon thread
        clean_thread.daemon = True
        # Start the email thread to send the email with the image
        email_thread.start()

    # Print the current status list (useful for debugging or monitoring)
    print(status_list)

    # Display the original frame with object detection rectangles
    cv2.imshow("Video", frame)

    # Wait for a key press and check if it's 'q' to break the loop
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# Release the video capture object
video.release()

# Start the thread to clean the folder
clean_thread.start()






