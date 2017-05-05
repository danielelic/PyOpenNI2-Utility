#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PyNiSplitter.py
~~~~~~~~~~~~

This script implements a ONI file splitter that writes RGB and depth images.


Usage: python2 PyNiSplitter.py --v <ONI file>

You should link the libOpenNI2.so and the OpenNI2 directory in the script path.
If they are located inside /usr/lib, you could

$ ln -s /usr/lib/libOpenNI2.so
$ ln -s /usr/lib/OpenNI2

:copyright: (c) 2015 by Daniele Liciotti.
:license: Apache2, see LICENSE for more details.
:date: 2017-05-05
"""

import numpy as np
import argparse
from primesense import openni2
import cv2


def split(video_path):
    """
    Split the ONI file into RGB and depth maps and shows using two separate windows
    @param video_path: contains the ONI file path
    """
    openni2.initialize()
    dev = openni2.Device.open_file(video_path)
    print(dev.get_sensor_info(openni2.SENSOR_DEPTH))
    depth_stream = dev.create_depth_stream()
    color_stream = dev.create_color_stream()
    depth_stream.start()
    color_stream.start()
    while True:
        frame_depth = depth_stream.read_frame()
        frame_color = color_stream.read_frame()

        frame_depth_data = frame_depth.get_buffer_as_uint16()
        frame_color_data = frame_color.get_buffer_as_uint8()

        depth_array = np.ndarray((frame_depth.height, frame_depth.width), dtype=np.uint16, buffer=frame_depth_data)
        color_array = np.ndarray((frame_color.height, frame_color.width, 3), dtype=np.uint8, buffer=frame_color_data)
        color_array = cv2.cvtColor(color_array, cv2.COLOR_BGR2RGB)

        cv2.imwrite("./depth/depth_" + str("{:020d}".format(frame_depth.timestamp)) + ".png", depth_array)
        cv2.imwrite("./color/color_" + str("{:020d}".format(frame_color.timestamp)) + ".png", color_array)

        cv2.imshow("depth", depth_array)
        cv2.imshow("color", color_array)

        ch = 0xFF & cv2.waitKey(1)
        if ch == 27:
            break

    depth_stream.stop()
    color_stream.stop()
    openni2.unload()
    cv2.destroyAllWindows()


def main():
    """The entry point"""
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="")
    p.add_argument('--v', dest='video_path', action='store', default='', help='path file *.oni')
    args = p.parse_args()
    split(args.video_path)


if __name__ == '__main__':
    main()
