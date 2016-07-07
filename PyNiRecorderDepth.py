#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
PyNiRecorder
~~~~~~~~~~~~

This script implements a ONI file writer.


Usage: python2 PyNiRecorderDepth.py

You should link the libOpenNI2.so and the OpenNI2 directory in the script path.
If they are located inside /usr/lib, you could

$ ln -s /usr/lib/libOpenNI2.so
$ ln -s /usr/lib/OpenNI2

:copyright: (c) 2015 by Daniele Liciotti.
:license: Apache2, see LICENSE for more details.
:date: 2016-07-07
"""
import time
from primesense import openni2
from primesense import _openni2 as c_api
import argparse


def main():
    # set and parse the arguments list
    p = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                description="")
    p.add_argument('-time',
                   dest='time',
                   action='store',
                   default='',
                   help='no of seconds')
    p.add_argument('-cycle',
                   dest='cycle',
                   action='store',
                   default='',
                   help='no of cycles')
    args = p.parse_args()

    try:
        openni2.initialize()  # can also accept the path of the OpenNI redistribution
    except:
        print ("Device not initialized")
        return

    try:
        dev = openni2.Device.open_any()
    except:
        print ("Unable to open the device")

    print dev.get_sensor_info(openni2.SENSOR_DEPTH)
    depth_stream = dev.create_depth_stream()

    depth_stream.set_video_mode(
            c_api.OniVideoMode(pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM,
                               resolutionX=320,
                               resolutionY=240,
                               fps=30))
    dev.set_image_registration_mode(True)
    depth_stream.start()

    for i in range(int(args.cycle)):
        print('iteration : {}'.format(i))

        rec = openni2.Recorder(time.strftime("%Y%m%d%H%M%S") + ".oni")
        rec.attach(depth_stream)
        print("Start video recorder...")
        rec.start()
        time.sleep(int(args.time))
        print("Stop video recorder...")
        rec.stop()

    depth_stream.stop()
    openni2.unload()


if __name__ == '__main__':
    main()
