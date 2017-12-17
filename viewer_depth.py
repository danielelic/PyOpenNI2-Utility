#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
viewer_depth.py
~~~~~~~~~~

This script implements a ONI file reader.


Usage: python2 viewer_depth.py --v <capture.oni>

You should link the libOpenNI2.so and the OpenNI2 directory in the script path.
If they are located inside /usr/lib, you could

$ ln -s /usr/lib/libOpenNI2.so
$ ln -s /usr/lib/OpenNI2

:copyright: (c) 2015 by Daniele Liciotti.
:license: Apache2, see LICENSE for more details.
:date: 2017-05-05
"""

import argparse

import cv2
import numpy as np
from primesense import openni2


def show(video_path):
    """
    Shows depth map
    @param video_path: contains the ONI file path
    """
    dev = openni2.Device
    try:
        openni2.initialize()
        dev = openni2.Device.open_file(video_path)
        print(dev.get_sensor_info(openni2.SENSOR_DEPTH))
    except (RuntimeError, TypeError, NameError):
        print(RuntimeError, TypeError, NameError)

    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    while True:
        frame_depth = depth_stream.read_frame()
        frame_depth_data = frame_depth.get_buffer_as_uint16()
        depth_array = np.ndarray((frame_depth.height, frame_depth.width),
                                 dtype=np.uint16,
                                 buffer=frame_depth_data) / 2300.  # 0-10000mm to 0.-1.
        cv2.imshow('Depth', depth_array)

        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break

    depth_stream.stop()
    openni2.unload()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    """The entry point"""
    # set and parse the arguments list
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="")
    p.add_argument('--v', dest='video_path', action='store', default='', help='path Video')
    args = p.parse_args()
    # show the capture!
    show(args.video_path)
