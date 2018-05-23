#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
from os import system
import logging
import subprocess

import amd_fan_config

VERSION = '1.2.0'
__author__ = 'Aleksandr Jashhuk, Zoer, R5AM, www.r5am.ru'


def clear_console():
    """ Clean the console """
    system('clear')


def valid_range(minimum, maximum, variable):
    """
    Check range of valid values
        :param minimum: Minimum value
        :param maximum: Maximum value
        :param variable: Check value
        :return: True - value is valid
    """
    if (variable >= minimum) and (variable <= maximum):
        result = True
    else:
        result = False
    return result


def get_temp(gpu_number):
    """
    Return the temperature of a given GPU
        :param gpu_number: GPU number
        :return: GPU temperature
    """
    command = 'ethos-smi -g {0} | grep "* Temperature" | cut -f 4 -d " "'.format(gpu_number)
    temp = subprocess.check_output(command, shell=True).decode('utf-8')
    return int(temp[:-2])


def get_fan_speed(gpu_number):
    """
    Return fan speed of a given GPU
        :param gpu_number: GPU number
        :return: Fan speed
    """
    command = 'ethos-smi -g {0} | grep "* Fan Speed" | cut -f 5 -d " "'.format(gpu_number)
    fan_speed = subprocess.check_output(command, shell=True).decode('utf-8')
    return int(fan_speed[:-2])


def fan_speed_set(gpu_number, new_fan_speed):
    """
    Sets a new fan speed for a given GPU
        :param gpu_number: GPU number
        :param new_fan_speed: New speed in percentage
    """
    if amd_fan_config.DEBUG_LEVEL == 'DEBUG':
        command = 'sudo ethos-smi --gpu {0} --fan {1}'.format(gpu_number, new_fan_speed)
    else:
        command = 'sudo ethos-smi --gpu {0} --fan {1} > /dev/null'.format(gpu_number, new_fan_speed)
    system(command)


def set_logging_level():
    """
    Set and return logger with debug level from config file
        :return: Logger
    """
    log = logging.getLogger('main')

    if amd_fan_config.DEBUG_LEVEL == 'DEBUG':
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)d %(levelname)s in \'%(module)s\' at line %(lineno)d: %(message)s', '%Y-%m-%d %H:%M:%S')
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)
    log.addHandler(handler)

    return log


def get_gpu_number(log):
    """
    Returns the number of GPU
        :return: GPU number
    """
    command = 'ethos-smi | grep "\[" | grep "\]" | grep GPU | tail -1 | cut -f 1 -d " "'
    gpu_count = subprocess.check_output(command, shell=True).decode('utf-8')[3:]
    number = int(gpu_count) + 1     # Count from 0
    log.debug('gpu_count: {0}'.format(number))
    return int(number)


def set_initial_fan_speed(gpu_count):
    """
    Sets the initial fan speed when the program starts
        :param gpu_count: Number of video cards in the system
    """
    for gpu in range(gpu_count):
        fan_speed_set(gpu, amd_fan_config.INIT_FAN_SPEED)


def set_new_fan_speed_for_all(gpu_count, log):
    """
    Sets the fan speed for all graphics cards
        :param gpu_count: Number of video cards in the system
        :param log: Logger
    """
    new_fan_speed = amd_fan_config.INIT_FAN_SPEED
    for gpu in range(gpu_count):

        current_temp = get_temp(gpu)
        current_fan_speed = get_fan_speed(gpu)
        log.debug('-========================= GPU {0} ==========================-'.format(gpu))
        log.debug('GPU {0}: Temp: {1}°C, Fan speed: {2}%'.format(gpu, current_temp, current_fan_speed))

        if not valid_range(amd_fan_config.LOW_TEMP, amd_fan_config.HIGH_TEMP, current_temp):
            log.debug('GPU {0}: Out of temperature range {1}...{2} °C'
                      .format(gpu, amd_fan_config.LOW_TEMP, amd_fan_config.HIGH_TEMP))

            # Increase the speed
            if current_temp > amd_fan_config.HIGH_TEMP:
                if current_fan_speed < 100:
                    new_fan_speed = current_fan_speed + amd_fan_config.SPEED_STEP

            # Decrease the speed
            if current_temp < amd_fan_config.LOW_TEMP:
                if current_fan_speed > 0:
                    new_fan_speed = current_fan_speed - amd_fan_config.SPEED_STEP

            if new_fan_speed != current_fan_speed:
                fan_speed_set(gpu, new_fan_speed)
                # log.debug("GPU {0}: Fan speed set to: {1}%".format(gpu, new_fan_speed))


def main():
    """
    Main function
    """

    # Clean the console
    clear_console()

    # Logger
    log = set_logging_level()

    # GPU number
    gpu_number = get_gpu_number(log)

    # Set initial fan speed
    set_initial_fan_speed(gpu_number)

    while True:
        set_new_fan_speed_for_all(gpu_number, log)
        time.sleep(amd_fan_config.SLEEP_TIME)
        log.debug("\n\n-======================================================="
                  "===========================================================-")
        log.debug("A new cycle of change of fan speed. Cycle time: {0} seconds.".format(amd_fan_config.SLEEP_TIME))


if __name__ == '__main__':
    main()
