import tkinter as tk
from tkinter import filedialog
import cv2
import os
from nd2reader import ND2Reader
import numpy as np

class ROISelectionApp:
    def __init__(self, master):
        self.master = master
        self.file_path = ""
        self.folder_path = tk.StringVar()  # Variable to store the selected folder path
        self.csv_folder_path = tk.StringVar(value="results/") # Default csv save path
        self.roi_x = tk.IntVar(value=10)  # Default value for ROI X
        self.roi_y = tk.IntVar(value=0)   # Default value for ROI Y
        self.roi_height = tk.IntVar(value=2048)  # Default value for ROI Height
        self.roi_width = tk.IntVar(value=400)    # Default value for ROI Width
        self.canny_upper = tk.IntVar(value=255)  # Default value for ROI Height
        self.canny_lower = tk.IntVar(value=85)    # Default value for ROI Width
        self.max_centroid_distance = tk.IntVar(value=50)  # max distance an object will travel between frames
        self.timeout = tk.IntVar(value=7)    # How long before an object is considered lost
        self.save_overlay = tk.IntVar()
        self.files = []  # Empty list that will accept an individual file, or files from a folder

        self.create_widgets()

    def create_widgets(self):
        # File selection button
        tk.Label(self.master, text="For individual .nd2 file").grid(row=0, column=0, padx=5, pady=5)
        self.file_button = tk.Button(self.master, text="Choose File", command=self.choose_file)
        self.file_button.grid(row=0, column=1, padx=5, pady=5)

        # Folder selection button
        tk.Label(self.master, text="For .nd2 files in a folder").grid(row=1, column=0, padx=5, pady=5)
        self.folder_button = tk.Button(self.master, text="Choose Folder", command=self.choose_folder)
        self.folder_button.grid(row=1, column=1, padx=5, pady=5)

        # csv output folder selection button
        tk.Label(self.master, text="Choose .csv save path").grid(row=0, column=2, padx=5, pady=5)
        self.csv_button = tk.Button(self.master, text="Choose Folder", command=self.choose_csv_output)
        self.csv_button.grid(row=0, column=3, padx=5, pady=5)

        # ROI X input field
        tk.Label(self.master, text="ROI X (px):").grid(row=2, column=0, padx=5, pady=5)
        self.roi_x_entry = tk.Entry(self.master, textvariable=self.roi_x)
        self.roi_x_entry.grid(row=2, column=1, padx=5, pady=5)

        # ROI Y input field
        tk.Label(self.master, text="ROI Y (px):").grid(row=3, column=0, padx=5, pady=5)
        self.roi_y_entry = tk.Entry(self.master, textvariable=self.roi_y)
        self.roi_y_entry.grid(row=3, column=1, padx=5, pady=5)

        # ROI Height input field
        tk.Label(self.master, text="ROI Height (px):").grid(row=4, column=0, padx=5, pady=5)
        self.roi_height_entry = tk.Entry(self.master, textvariable=self.roi_height)
        self.roi_height_entry.grid(row=4, column=1, padx=5, pady=5)

        # ROI Width input field
        tk.Label(self.master, text="ROI Width (px):").grid(row=5, column=0, padx=5, pady=5)
        self.roi_width_entry = tk.Entry(self.master, textvariable=self.roi_width)
        self.roi_width_entry.grid(row=5, column=1, padx=5, pady=5)

        # ROI Preview button
        self.roi_button = tk.Button(self.master, text="Preview ROI", command=self.preview_roi)
        self.roi_button.grid(row=6, column=0, padx=5, pady=5)

        # Canny Upper
        tk.Label(self.master, text="Canny Upper:").grid(row=2, column=2, padx=5, pady=5)
        self.canny_upper_entry = tk.Entry(self.master, textvariable=self.canny_upper)
        self.canny_upper_entry.grid(row=2, column=3, padx=5, pady=5)

        # Canny Lower
        tk.Label(self.master, text="Canny Lower:").grid(row=3, column=2, padx=5, pady=5)
        self.canny_lower_entry = tk.Entry(self.master, textvariable=self.canny_lower)
        self.canny_lower_entry.grid(row=3, column=3, padx=5, pady=5)

        # Max Centroid Distance
        tk.Label(self.master, text="Max Centroid Distance (px):").grid(row=4, column=2, padx=5, pady=5)
        self.max_centroid_distance_entry = tk.Entry(self.master, textvariable=self.max_centroid_distance)
        self.max_centroid_distance_entry.grid(row=4, column=3, padx=5, pady=5)

        # Timeout threshold
        tk.Label(self.master, text="Timeout Threshold (frames):").grid(row=5, column=2, padx=5, pady=5)
        self.timeout_entry = tk.Entry(self.master, textvariable=self.timeout)
        self.timeout_entry.grid(row=5, column=3, padx=5, pady=5)

        # Save overlay checkbox
        self.save_overlay_checkbox = tk.Checkbutton(self.master, text="Save Overlay?", variable=self.save_overlay, command=self.on_checkbox_click)
        self.save_overlay_checkbox.grid(row=6, column=1, columnspan=1, padx=5, pady=5)

        # Button to confirm selections
        self.confirm_button = tk.Button(self.master, text="Confirm", command=self.confirm_selections)
        self.confirm_button.grid(row=6, column=2, columnspan=2, padx=5, pady=5)

        # Quit button
        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_ui)
        self.quit_button.grid(row=6, column=3, padx=5, pady=5)

    def choose_file(self):
        self.file_path = filedialog.askopenfilename()
        print("Selection:", self.file_path)

    def choose_folder(self):
        self.folder_path.set(filedialog.askdirectory())  # Set the selected folder path
        print("Selection:", self.folder_path.get())

    def choose_csv_output(self):
        self.csv_folder_path.set(filedialog.askdirectory())  # Set the selected folder path
        print("csv save path:", self.csv_folder_path.get())

    def on_checkbox_click(self):
        if self.save_overlay.get() == 1:
            print("An overlay of tracked objects will be saved!")
        else:
            print("An overlay of tracked objects will not be saved")

    def input_handling(self):
        # Input handling
        if self.folder_path.get():
            self.files = [os.path.join(self.folder_path.get(), f) for f in os.listdir(self.folder_path.get())]
        if self.file_path:
            self.files = [self.file_path]

    def confirm_selections(self):
        self.error_handling()
        self.input_handling()

        print(".csv results save path:", self.csv_folder_path.get())
        # print("ROI X:", self.roi_x.get())
        # print("ROI Y:", self.roi_y.get())
        # print("ROI Height:", self.roi_height.get())
        # print("ROI Width:", self.roi_width.get())
        # print("Canny Upper:", self.canny_upper.get())
        # print("Canny Lower:", self.canny_lower.get())
        # Close the Tkinter window
        self.master.destroy()

    def error_handling(self):
        if self.file_path == '' and self.folder_path.get() == '':
            raise ValueError("No file selected!")
        if self.file_path and self.folder_path.get():
            raise ValueError(
                "...Why did you pick a file AND a folder? Choose ONE or the OTHER. What did you expect to happen? :)")

    def preview_roi(self):
        if self.file_path == '' and self.folder_path.get() == '':
            print("Choose a file first!")
        else:
            self.input_handling()

        with ND2Reader(self.files[0]) as nd2_file:
            frame_data = nd2_file[0]
            image = frame_data
            cv2.namedWindow("Select ROI. Press enter to confirm, 'c' to cancel", cv2.WINDOW_NORMAL)
            ROI = cv2.selectROI("Select ROI. Press enter to confirm, 'c' to cancel", image, cv2.WINDOW_NORMAL)
            cv2.destroyAllWindows()
            self.roi_x.set(ROI[0])
            self.roi_y.set(ROI[1])
            self.roi_width.set(ROI[2])
            self.roi_height.set(ROI[3])

    def get_roi(self):
        ROI = (self.roi_x.get(), self.roi_y.get(), self.roi_height.get(), self.roi_width.get())
        return ROI

    def quit_ui(self):
        self.master.destroy()
        quit(2)


def create_UI():
    root = tk.Tk()
    root.iconbitmap(r'count.ico')
    root.title("Count Objects Until No Tomorrow (C.O.U.N.T.)")
    app = ROISelectionApp(root)
    root.mainloop()
    return app
