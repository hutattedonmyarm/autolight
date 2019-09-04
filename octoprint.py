#!/usr/bin/env python3
"""
Fetches print status from Octoprint
"""
import asyncio
import logging
from typing import Dict
import aiohttp
import config

HTTPHeaders = Dict[str, str]

API_KEY = config.OCTOPRINT['api_key']
BASE_ADDRESS = config.OCTOPRINT['base_address']
LOGGER = logging.getLogger('Octoprint')

def get_headers() -> HTTPHeaders:
    '''Returns the auth hearders to connect to Octoprint'''
    return {
        'X-Api-Key': API_KEY,
        'Content-Type': 'application/json'
    }

def get_session() -> aiohttp.ClientSession:
    '''Creates and returns a new session to connect to Octprint'''
    headers = get_headers()
    return aiohttp.ClientSession(headers=headers)

def is_printing() -> bool:
    '''Checks synchronously if the printer is currently printing.'''
    return asyncio.run(is_printing_async())

async def is_printing_async(session: aiohttp.ClientSession = None):
    '''Checks asynchronously if the printer is currently printing.
    Creates a new session if None is supplied
    Keyword arguments:
    session -- a aiohttp.ClientSession (default None)
    '''
    if session is None:
        async with get_session() as session:
            return await is_printing_async(session)
    try:
        async with session.get(BASE_ADDRESS + '/api/job') as resp:
            if resp.status != 200:
                LOGGER.debug('Could not connect to %s: HTTP %d', BASE_ADDRESS, resp.status)
                return False
            job = await resp.json()
            LOGGER.debug('Print job %s', job)
            print_time_left = job["progress"]["printTimeLeft"]
            is_print_running = bool(print_time_left)
            LOGGER.debug('Printing? %s', is_print_running)
            return is_print_running
    except Exception as exception:
        Logger.error('Error connecting to Octporint: %s', exception)
        return False


async def main():
    '''Prints the current status'''
    print('Printing?', await is_printing_async())

if __name__ == '__main__':
    asyncio.run(main())

