#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
oni2avi.py
~~~~~~~~~~

This script implements a ONI file reader.


Usage: python2 oni2avi.py --v <capture.oni>

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


def openDevice(video_path):
    try:
        openni2.initialize()
        dev = openni2.Device.open_file(video_path)
        pbs = openni2.PlaybackSupport(dev)

        pbs.set_repeat_enabled(False)
        pbs.set_speed(-1.0)

        return dev
    except (RuntimeError, TypeError, NameError):
        print(RuntimeError, TypeError, NameError)


def saveDepth(dev):
    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    avi_depth = cv2.VideoWriter('depth.avi', cv2.cv.CV_FOURCC(*'XVID'),
                                depth_stream.get_video_mode().fps,
                                (depth_stream.get_video_mode().resolutionX,
                                 depth_stream.get_video_mode().resolutionY))
    depth_scale_factor = 255.0 / depth_stream.get_max_pixel_value()
    frame_depth = depth_stream.read_frame()

    while frame_depth.frameIndex < depth_stream.get_number_of_frames():
        frame_depth = depth_stream.read_frame()
        frame_depth_data = frame_depth.get_buffer_as_uint16()
        depth_array = np.ndarray((frame_depth.height, frame_depth.width),
                                 dtype=np.uint16,
                                 buffer=frame_depth_data)
        depth_uint8 = cv2.convertScaleAbs(depth_array, alpha=depth_scale_factor)
        depth_colored = cv2.applyColorMap(depth_uint8, cv2.COLORMAP_HSV)

        avi_depth.write(depth_colored)

    depth_stream.stop()
    openni2.unload()
    cv2.destroyAllWindows()


def saveColor(dev):
    color_stream = dev.create_color_stream()
    color_stream.start()

    avi_color = cv2.VideoWriter('color.avi', cv2.cv.CV_FOURCC(*'XVID'),
                                color_stream.get_video_mode().fps,
                                (color_stream.get_video_mode().resolutionX,
                                 color_stream.get_video_mode().resolutionY))

    frame_color = color_stream.read_frame()

    while frame_color.frameIndex < color_stream.get_number_of_frames():
        frame_color = color_stream.read_frame()
        frame_color_data = frame_color.get_buffer_as_uint8()
        color_array = np.ndarray((frame_color.height, frame_color.width, 3),
                                 dtype=np.uint8,
                                 buffer=frame_color_data)
        color_array = cv2.cvtColor(color_array, cv2.COLOR_BGR2RGB)

        avi_color.write(color_array)

    color_stream.stop()
    openni2.unload()
    cv2.destroyAllWindows()


def main():
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="")
    p.add_argument('--v', dest='video_path', action='store', default='', help='path Video')
    args = p.parse_args()
    dev = openDevice(args.video_path)
    saveDepth(dev)
    dev = openDevice(args.video_path)
    saveColor(dev)


if __name__ == '__main__':
    main()
