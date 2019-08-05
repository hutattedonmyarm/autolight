#!/usr/bin/env python3

# Example for RC timing reading for Raspberry Pi
# using CircuitPython Libraries

import time
import asyncio
import sys
import board
from digitalio import DigitalInOut, Direction

RCpin = board.D23
NUM_READINGS = 5
FACTOR_DARK = 0.7

async def get_brightness(num_readings=1, reading_timeout=50):
    lit = await is_lit(num_readings, reading_timeout)
    return 255 if lit else 0

async def is_lit(num_readings=5, reading_timeout=200):
    readings = []
    for ctr in range(0, num_readings):
        #print(f'Reading {ctr}', file=sys.stderr)
        with DigitalInOut(RCpin) as rc:
            reading = 0

            # setup pin as output and direction low value
            rc.direction = Direction.OUTPUT
            rc.value = False

            await asyncio.sleep(0.1)

            # setup pin as input and wait for low value
            rc.direction = Direction.INPUT

            # This takes about 1 millisecond per loop cycle
            while rc.value is False:
                reading += 1
                if reading > reading_timeout:
                    #print('seems dark')
                    #readings.append(-1)
                    reading = -1
                    break
            readings.append(reading)
    num_dark = len([t for t in readings if t < 0])
    return num_dark < num_readings*FACTOR_DARK

async def main():
    b = await is_lit()
    if not b:
        print('Dark')
    else:
        print('Lit')
if __name__=='__main__':
    asyncio.run(main())
