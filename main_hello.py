
import cv2

from picamera2 import Picamera2
from ultralytics import YOLO
#import time

# Set up the camera with Picam
picam2 = Picamera2()
size_img = 640
picam2.preview_configuration.main.size = (640,480)
picam2.preview_configuration.main.format = "RGB888" #RGB888
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

# Load YOLOv8
model = YOLO("first_model_ncnn_model") #or your model

while True:
    # Capture a frame from the camera
    frame = picam2.capture_array()

    # Run YOLO model on the captured frame and store the results
    results = model(frame, conf=0.7, imgsz=size_img, max_det=5,rect=True, half= True, int8=False, device="cpu")
    
    #results = model("test1.png", conf=0.7, imgsz=size_img, max_det=5,rect=True, half= True, int8=False, device="cpu")

    # Output the visual detection data, we will draw this on our camera preview window
    annotated_frame = results[0].plot()

    # Get inference time
    inference_time = results[0].speed['inference']
    fps = 1000 / inference_time  # Convert to milliseconds

    #fps=1/(end-start)
    text = f'FPS: {fps:.1f}'

    # Define font and position
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = annotated_frame.shape[1] - text_size[0] - 10  # 10 pixels from the right
    text_y = text_size[1] + 10  # 10 pixels from the top


    # Draw the text on the annotated frame
    cv2.putText(annotated_frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)


    # Display the resulting frame
    cv2.imshow("Camera", annotated_frame)

    # Exit the program if q is pressed
    if cv2.waitKey(1) == ord("q"):
        break

# Close all windows
cv2.destroyAllWindows()
