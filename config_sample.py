"""
Configuration for the automatic printer lights
"""
import board

OCTOPRINT = {
    'api_key': '',
    'base_address': 'http://ADDRESS:PORT'
}

BRIGHTNESS = {
    'rc_pin': board.D23,
    'num_readings': 5,
    'factor_dark': 0.7
}

AUTOLIGHT = {
    'pixel_pin': board.D12,
    'sleep_time': 0.5
}
