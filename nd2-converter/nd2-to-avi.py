# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 14:08:13 2023

@author: Emmanuel
"""
#%%gui version pkgs
import os
import cv2
from nd2reader import ND2Reader
import time
import tkinter as tk
from tkinter import filedialog

#%% compression and conversion main function

# gui function to select input and output directories
def select_input_directory():
    input_dir = filedialog.askdirectory(title="Select Input Directory")
    if input_dir:
        input_directory.set(input_dir)
        print(f"Input directory: {input_directory.get()}")

def select_output_directory():
    output_dir = filedialog.askdirectory(title="Select Output Directory")
    if output_dir:
        output_directory.set(output_dir)
        print(f"Output directory: {output_directory.get()}")
        
# main conversion function
def run_conversion():
    input_dir = input_directory.get()
    output_dir = output_directory.get()

    if not os.path.exists(input_dir):
        print("Input directory does not exist!")
        return

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    frame_rate = 90.82
    nd2_files = [file for file in os.listdir(input_dir) if file.endswith(".nd2")]

    start_time = time.time()

    for nd2_file in nd2_files:
        file_name = os.path.splitext(nd2_file)[0]
        input_path = os.path.join(input_dir, nd2_file)

        with ND2Reader(input_path) as f:
            height, width = f[0].shape
            output_video_path = os.path.join(output_dir, f"{file_name}.avi")

            video = cv2.VideoWriter(output_video_path,
                                    cv2.VideoWriter_fourcc(*'XVID'),
                                    frame_rate,
                                    (width, height),
                                    False)

            for i, frame in enumerate(f):
                frame = frame / 2 ** 8
                video.write(frame.astype('uint8'))
                print(f"Converting {nd2_file} - Frame {i}")

            video.release()

    end_time = time.time()
    runtime = end_time - start_time
    print(f"Conversion complete! Total runtime: {runtime:.2f} seconds. Framerate: {frame_rate}")

    # close the Tkinter window after conversion is complete
    root.destroy()


# gui setup
root = tk.Tk()
root.title("ND2 to AVI Conversion")

input_directory = tk.StringVar()
output_directory = tk.StringVar()

# create buttons
input_label = tk.Label(root, text="Input Directory:")
input_label.grid(row=0, column=0)

input_entry = tk.Entry(root, textvariable=input_directory, width=40)
input_entry.grid(row=0, column=1, padx=5)

input_button = tk.Button(root, text="Browse", command=select_input_directory)
input_button.grid(row=0, column=2, padx=5)

output_label = tk.Label(root, text="Output Directory:")
output_label.grid(row=1, column=0)

output_entry = tk.Entry(root, textvariable=output_directory, width=40)
output_entry.grid(row=1, column=1, padx=5)

output_button = tk.Button(root, text="Browse", command=select_output_directory)
output_button.grid(row=1, column=2, padx=5)

convert_button = tk.Button(root, text="Convert", command=run_conversion)
convert_button.grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
