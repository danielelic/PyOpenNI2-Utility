#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PyNiViewer
~~~~~~~~~~

This script implements a ONI file reader.


Usage: python2 PyNiViewew --v <capture.oni>

You should link the libOpenNI2.so and the OpenNI2 directory in the script path.
If they are located inside /usr/lib, you could

$ ln -s /usr/lib/libOpenNI2.so
$ ln -s /usr/lib/OpenNI2

:copyright: (c) 2015 by Daniele Liciotti.
:license: Apache2, see LICENSE for more details.
:date: 2015-04-15
"""

import os
import argparse
import numpy as np
import cv2
from primesense import openni2

def show(video_path):
        """
        Shows RGB and depth maps on two separate windows
        @param video_path: contains the ONI file path
        """
        try:
            openni2.initialize()
            dev = openni2.Device.open_file(video_path)
            print (dev.get_sensor_info(openni2.SENSOR_DEPTH))
        except (RuntimeError, TypeError, NameError):
            print(RuntimeError, TypeError, NameError)

        depth_stream = dev.create_depth_stream()
        color_stream = dev.create_color_stream()
        depth_stream.start()
        color_stream.start()
        while True:
                frame_depth = depth_stream.read_frame()
                frame_color = color_stream.read_frame()

                frame_depth_data = frame_depth.get_buffer_as_uint16()
                frame_color_data = frame_color.get_buffer_as_uint8()

                depth_array = np.ndarray((frame_depth.height, frame_depth.width), dtype = np.uint16, buffer = frame_depth_data)/10000. #0-10000mm to 0.-1.
                color_array = np.ndarray((frame_color.height, frame_color.width, 3), dtype = np.uint8, buffer = frame_color_data)
                color_array = cv2.cvtColor(color_array, cv2.COLOR_BGR2RGB)

                cv2.imshow('Depth', depth_array)
                cv2.imshow('Color', color_array)

                ch = 0xFF & cv2.waitKey(1)
                if ch == 27:
                        break      

        depth_stream.stop()
        color_stream.stop()
        openni2.unload()
        cv2.destroyAllWindows()

def main():
        """The entry point"""
        # set and parse the arguments list
        p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="")
        p.add_argument('--v', dest = 'video_path', action = 'store', default = '', help = 'path Video')
        args = p.parse_args()
        # show the capture!
        show(args.video_path)

if __name__ == '__main__':
        main()
