#!/usr/bin/env python3
'''
Reads the current brightness level
'''

import asyncio
import logging
from digitalio import DigitalInOut, Direction
import config

RC_PIN = config.BRIGHTNESS['rc_pin']
NUM_READINGS = config.BRIGHTNESS['num_readings']
FACTOR_DARK = config.BRIGHTNESS['factor_dark']
LOGGER = logging.getLogger()

async def get_brightness(num_readings: int = 1, reading_timeout: int = 50) -> int:
    '''Returns the current brightness from 0 (dark) to 355 (lit)
    Keyword arguments:
    num_readings: int -- How many times the sensor should be queried
    reading_timeout: int -- Timeout in ms after which the room is considered dark
    '''
    lit = await is_lit(num_readings, reading_timeout)
    room_brightness = 255 if lit else 0
    LOGGER.debug('Room brightness: %d', room_brightness)
    return room_brightness

async def is_lit(num_readings: int = 5, reading_timeout: int = 200):
    '''Checks if the room is currently lit or dark
    Keyword arguments:
    num_readings: int -- How many times the sensor should be queried
    reading_timeout: int -- Timeout in ms after which the room is considered dark
    '''
    readings = []
    for _ in range(0, num_readings):
        with DigitalInOut(RC_PIN) as pin:
            reading = 0

            # setup pin as output and direction low value
            pin.direction = Direction.OUTPUT
            pin.value = False

            await asyncio.sleep(0.1)

            # setup pin as input and wait for low value
            pin.direction = Direction.INPUT

            # This takes about 1 millisecond per loop cycle
            while pin.value is False:
                reading += 1
                if reading > reading_timeout:
                    reading = -1
                    break
            readings.append(reading)
    num_dark = len([t for t in readings if t < 0])
    LOGGER.debug('%d%s of readings returned dark', 100.0 * num_dark / num_readings, '%')
    return num_dark < num_readings*FACTOR_DARK

async def main():
    '''Prints the current light status'''
    lit_status = await is_lit()
    if not lit_status:
        print('Dark')
    else:
        print('Lit')

if __name__ == '__main__':
    asyncio.run(main())

