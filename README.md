# Count Objects Until No Tomorrow (C.O.U.N.T.)
_Ah-ah-ah!_ 
## Description
This project is an object tracking system implemented in Python. It provides functionality for detecting and 
tracking objects in video frames using cv2 canny edge detection. The intended application of this project is to 
track cells that flow through a CF-DEP device. Cell response to DEP is recorded within results.csv 

**General workflow:**
1. Conversion. nd2 files are converted into pngs.
2. Background Subtraction. The first frame is subtracted from all subsequent frames
3. cv2.Canny Edge Detection and cv2.findContours
4. Centroid Distance Tracking. For an object in frame _n_, the object detected in frame _n_ + 1 that has traveled 
   the smallest distance from the object in frame _n_ is the same object.
5. Results. Results are saved to a .csv file.

## Features
- Object detection and tracking in video frames or .nd2 files.
- Background subtraction
- Exporting tracking data to a CSV file.
- User interface 

## How to install
Installation is extremely simple, just

## How to use:
Run main.py

A UI will appear with lots of information.

The region of interest (ROI) is where the tracking will occur.

"Choose .csv path" will change where the results file is saved. By default, the file will save in the "results" folder.

"Canny upper" and "Canny lower" are the bounds for edge hysteresis thresholding. Choosing a 3:1 (default) or 2:1 
ratio works well. 

"Max centroid distance" is the maximum allowable distance an object can travel between frames.

"Timeout Threshold (frames)" is the amount of time before a labeled object is considered gone. Sometimes, the object 
being tracked will be lost by the algorithm. This value is how long the algorithm will continue looking for an 
object before giving up. For example, if an object is labeled with ID = 3 and disappears for a frame, that's OK because 
the 
timeout is 
longer 
than one frame. If the object reappears before the timeout threshold, then tracking will continue and the object 
will be reassigned it's label ID = 3. If an object dissapears for longer than the threshold, its considered gone and 
the 
label (ID = 3) is retired. No more objects will be assigned with that exact label. 




The "Save overlay?" checkbox will allow the user to save an overlay of tracked object labels on top of the inputted 
frames. The overlay frames currently save to the folder named 'nd2_results'. If you are only interested in counts 
of cells, you don't need to save overlays. The overlay is a good way to visualize tracking behavior. 


"Preview ROI" will allow you to define your own ROI on an image. A file/folder must be selected first to open an 
image. To create the ROI, click and drag on the image in the new window. To confirm your ROI, press "enter" or 
"space" and to cancel your selection, press "c"

## Notes to self:
ffmpeg -i 50_kHz.mp4 -vf fps=1 image-%03d.png

convert to images until 1 second into video

ffmpeg -ss 0 -t 1 -i 50_kHz.mp4 image-%03d.png

ffmpeg -framerate 7 -i canny_image-%03d.png canny.mp4

ffmpeg -framerate 10 -i frame_%d.png tracking.mp4


