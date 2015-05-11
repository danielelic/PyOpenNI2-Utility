#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PyNiSimpleViewer
~~~~~~~~~~

This script implements a depth stream reader.


Usage: python2 PyNiSimpleViewer

You should link the libOpenNI2.so and the OpenNI2 directory in the script path.
If they are located inside /usr/lib, you could

$ ln -s /usr/lib/libOpenNI2.so
$ ln -s /usr/lib/OpenNI2

:copyright: (c) 2015 by Daniele Liciotti.
:license: Apache2, see LICENSE for more details.
:date: 2015-05-11
"""

import numpy as np
from primesense import openni2
from primesense import _openni2 as c_api

import cv2

try:
	openni2.initialize()
	dev = openni2.Device.open_any()
	print (dev.get_sensor_info(openni2.SENSOR_DEPTH))
except (RuntimeError, TypeError, NameError):
	print(RuntimeError, TypeError, NameError)
depth_stream = dev.create_depth_stream()
color_stream = dev.create_color_stream()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 640, resolutionY = 480, fps = 30))
color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX = 640, resolutionY = 480, fps = 30))
depth_stream.start()
color_stream.start()

shot_idx = 0

while True:
	frame_depth = depth_stream.read_frame()
	frame_color = color_stream.read_frame()

	frame_depth_data = frame_depth.get_buffer_as_uint16()
	frame_color_data = frame_color.get_buffer_as_uint8()

	depth_array = np.ndarray((frame_depth.height, frame_depth.width), dtype = np.uint16, buffer = frame_depth_data)
	color_array = np.ndarray((frame_color.height, frame_color.width, 3), dtype = np.uint8, buffer = frame_color_data)
	color_array = cv2.cvtColor(color_array, cv2.COLOR_BGR2RGB)
	cv2.imshow('Depth', depth_array)
	cv2.imshow('Color', color_array)

	ch = 0xFF & cv2.waitKey(1)
	if ch == 27:
		break
	if ch == ord(' '):
		fn_depth = 'depth_shot_%03d.png' % shot_idx
		fn_color = 'color_shot_%03d.png' % shot_idx
		cv2.imwrite(fn_depth, depth_array)
		cv2.imwrite(fn_color, color_array)
		print fn_depth, 'saved'
		print fn_color, 'saved'
		shot_idx += 1
depth_stream.stop()
color_stream.stop()
openni2.unload()
cv2.destroyAllWindows()
