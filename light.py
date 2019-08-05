#!/usr/bin/env python3
import signal
import sys
import time
import asyncio
import board
import neopixel
import brightness


def signal_handler(sig, frame):
        pixels.fill((0, 0, 0))
        sys.exit(0)

async def main():
    signal.signal(signal.SIGINT, signal_handler)
    pixel_pin = board.D12

    # The number of NeoPixels
    num_pixels = 8

    # The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
    # For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
    ORDER = neopixel.GRB

    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=True,
                               pixel_order=ORDER)
    sleep_time = 0.5
    while True:
        try:
            #b = await brightness.is_lit()
            #light = 0 if b else 255
            b = await brightness.get_brightness()
            light = 255 - b
            #print(f'Setting neopixel brightness to {light}')
            await asyncio.sleep(sleep_time)
            pixels.fill((light, light, light))
        except Exception as ex:
            print(ex)
            pixels.fill((0,0,0))
            sys.exit(1)

asyncio.run(main())
