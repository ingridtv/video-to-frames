"""
Utilities for reading and processing .csv (and .txt) files
"""

import csv


class NoMatchingFileError(Exception):
    def __init__(self, msg=None):
        if msg is not None:
            self.msg = msg
        else:
            self.msg = "No matching file was found"


# =====================================
#   HELPER FUNCTIONS
# =====================================

def read_csv_file(filename, has_header=False, include_header=False):
    """
    Read a .csv file with samples/data specified by row and return the content
    as a list of lists.

    filename : str, or path-like
        The path to the .csv file
    has_header : bool
        Whether the .csv file has a header specifying column contents
    include_header : bool
        Whether to include the header as the first row, or just return the
        actual file contents

    """
    print(f"Reading {filename} as .csv")

    with open(filename, newline='') as csvfile:
        reader = csv.reader(
            csvfile, delimiter=';', #quotechar='|',
            skipinitialspace=True,
        )

        if has_header:
            if include_header:
                i = 0   # start with first (header) row
            else:
                i = 1   # start with first content row
        else:
            i = 0   # start with first row and first content row

        data = []
        for row in reader:
            data.append([])
            for c in row:
                data[i].append(c)
            i += 1

        return data


def sort_data_by_row(data, has_header=False, include_header=False):
    if has_header:
        if include_header:
            samples = data      # do not skip first row
        else:
            samples = data[1:]  # skip first (header) row
    else:
        samples = data  # use all data if has_header=False

    d = {}
    for idx, sample in enumerate(samples):  # For each row
        entry = {
            'item': sample[0],  # name of item (filename or lymph node station)
            'start_time': float(sample[1]),  # time in seconds
            'end_time': float(sample[2]),    # time in seconds
        }
        d[idx] = entry

    return d


def parse_ebus_video_file(filename):
    """
    Each video clip has one associated line in the file `filename`. Each
    line in the file is formatted as:
    Video file name;Start trim (s);End trim (s)

    For example:
    EBUS-20160215-202451.avi;1322;1415
    EBUS-20210604-092427.avi;250;420
    EBUS-20210608-091758.avi;515;745
    ...

    with time in seconds at which to trim the video given for each video clip.
    """
    from ebus.ebus_utils.video_utilities import VideoTrimmingLimits

    data = read_csv_file(filename, include_header=True)
    data_dict = sort_data_by_row(data, include_header=False)    # skip header

    time_points_per_file = []
    for key, entry in data_dict.items():
        fn = entry['item']
        trim_at = VideoTrimmingLimits(
            t1=entry['start_time'],
            t2=entry['end_time'],
        )
        time_points_per_file.append([fn, trim_at])

    return time_points_per_file


def parse_lymph_node_stations_file(filename):
    """
    Each video clip has one associated lymph node station and time file. Each
    line in the file is formatted as:
    Lymph node;Start trim (s);End trim (s)

    For example:
    4R;17.4;25.2
    4L;34.1;39.5
    7L;126.3;141.8
    ...

    with time in seconds given for each of the recorded lymph node stations.
    """

    from ebus.ebus_utils.video_utilities import VideoTrimmingLimits

    data = read_csv_file(filename, has_header=False)    # files have no header
    data_dict = sort_data_by_row(data, has_header=False)

    time_points_per_station = []
    for key, entry in data_dict.items():
        lymph_node = entry['item']
        trim_at = VideoTrimmingLimits(
            t1=entry['start_time'],
            t2=entry['end_time'],
        )
        time_points_per_station.append([lymph_node, trim_at])

    return time_points_per_station

