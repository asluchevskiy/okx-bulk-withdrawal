# -*- coding: utf-8 -*-
import random
import logging

log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # log message formatting


def random_float(a, b, diff=1):
    random_number = random.uniform(a, b)
    try:
        precision_a = len(str(a).split('.')[1])
    except IndexError:
        precision_a = 0
    try:
        precision_b = len(str(b).split('.')[1])
    except IndexError:
        precision_b = 0
    precision = max(precision_a, precision_b)
    return round(random_number, precision + diff)


def setup_logging(logger, log_file):
    # logging file handler
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)
