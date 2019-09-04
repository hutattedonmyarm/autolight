#!/usr/bin/env python3
'''Queries the lgihtsensor and octpotint
and turns the neopixels on/off accordingly'''

import signal
import sys
import asyncio
import board
import neopixel
import brightness
import octoprint
import config
import os
import logging
from logging import handlers

LOGGER = logging.getLogger()

def signal_handler(sig, hand):
    LOGGER.info('Signal handler called: %s, %s', sig, hand)
    '''
    if PIXELS:
        PIXELS.fill((0, 0, 0))
    '''
    sys.exit(0)

async def main():
    '''Queries the lightsensor and octoprint
    and turns the neopixels on/off accordingly'''
    signal.signal(signal.SIGINT, signal_handler)
    log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'autolight.log')
    handler = handlers.TimedRotatingFileHandler(log_file, interval=1, when='D')
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(module)s:%(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
    LOGGER.addHandler(handler)
    LOGGER.setLevel(logging.DEBUG)
    pixel_pin = config.AUTOLIGHT['pixel_pin']

    # The number of NeoPixels
    num_pixels = config.AUTOLIGHT['num_pixels']

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    order = config.AUTOLIGHT['pixel_order']

    pixels = neopixel.NeoPixel(pixel_pin,
                               num_pixels,
                               brightness=config.AUTOLIGHT['pixel_brightness'],
                               auto_write=True,
                               pixel_order=order)
    sleep_time = config.AUTOLIGHT['sleep_time']
    async with octoprint.get_session() as session:
        while True:
            try:
                print_status = await octoprint.is_printing_async(session)
                LOGGER.info('Is printing? %s', print_status)
                light = 0
                if print_status:
                    current_brightness = await brightness.get_brightness()
                    LOGGER.info('Brightness %s', current_brightness)
                    light = 255 - current_brightness
                pixels.fill((light, light, light))
                LOGGER.info('Setting light to %s', light) 
                await asyncio.sleep(sleep_time)
            except Exception as ex:
                LOGGER.error(ex)
                pixels.fill((0, 0, 0))
                sys.exit(1)

asyncio.run(main())

