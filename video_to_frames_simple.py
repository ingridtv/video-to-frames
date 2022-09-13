"""
Convert video files to frames (simple version). If you have one video per
patient, and want the whole video as one sequence, use this file.

The output structure is as follows:
--Patient_001
    |---Sequence_001
        |---frame_1.png
        |---frame_2.png
        |---...
--Patient_002
    |---Sequence_001
        |---frame_1.png
        |---frame_2.png
        |---...
--Patient_003
    |---Sequence_001
        |---frame_1.png
        |---frame_2.png
        |---...
...
"""

import os
import math

import imageio
import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm

from utils.video_utilities import VideoTrimmingLimits, get_trim_start_end_frames


# =======================================================
#   Set input/output folders and frame interval
# =======================================================
INPUT_DATA_PATH = "/path/to/raw/videos"     # folder containing raw videos
OUTPUT_PATH = "/path/to/processed/dataset"  # folder in which to put the processed dataset

EXTRACT_FRAME_INTERVAL = 1  # Extract every x frames
# =======================================================


VIDEO_LIST = [fn for fn in os.listdir(INPUT_DATA_PATH) if
              (fn.lower().endswith('.avi') or fn.lower().endswith('.mpg'))]

for p_idx, filename in tqdm(enumerate(VIDEO_LIST), 'Patient'):

    # Create ./Patient_XX/Sequence_XX directory
    seq_dir = os.path.join(OUTPUT_PATH, f'Patient_{p_idx + 1:03d}/Sequence_{1:03d}')
    os.makedirs(seq_dir, exist_ok=True)

    # Get full path to video file
    video_path = os.path.join(INPUT_DATA_PATH, filename)

    # Read the video data
    vid_reader = imageio.get_reader(video_path)
    metadata = vid_reader.get_meta_data()
    fps = metadata['fps']
    duration = metadata['duration']
    nb_frames = math.floor(fps * duration)

    # TODO: If using full video, set start time = 0 and end time = duration,
    #   but you can also get these numbers elsewhere and specify
    trim_time = VideoTrimmingLimits(t1=0., t2=1.)
    start_frame, end_frame = get_trim_start_end_frames(trim_time, fps, nb_frames)

    # Extract the given frames
    for frnb, fr in enumerate(tqdm(range(start_frame, end_frame, int(EXTRACT_FRAME_INTERVAL)), 'Frames')):
        arr = np.asarray(vid_reader.get_data(fr))  # Array: [H, W, 3]

        # Display figure and image
        figure_size = (metadata['size'][0] / 100, metadata['size'][1] / 100)
        fig = plt.figure(figsize=figure_size)
        plt.imshow(arr, aspect='auto')

        # Adjust layout to avoid margins, axis ticks, etc. Save and close.
        plt.axis('off')
        plt.tight_layout(pad=0)
        plt.savefig(os.path.join(seq_dir, f'frame_{frnb:d}.png'))
        # plt.show()     # show() used only when debugging
        plt.close(fig)
