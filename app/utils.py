# -*- coding: utf-8 -*-
import random
import logging
import time

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


def read_wallet_file(file_name):
    wallets = []
    try:
        with open(file_name, 'r') as f:
            for line in f:
                wallet = line.strip()
                if wallet:
                    wallets.append(wallet)
    except FileNotFoundError:
        pass
    return wallets


def run_withdraw(api, wallets_file, complete_wallets_file, token, network,
                 min_amount, max_amount, min_delay, max_delay, thread_stop_event=None):
    wallets = read_wallet_file(wallets_file)
    complete_wallets = set(read_wallet_file(complete_wallets_file))
    for idx, wallet in enumerate(wallets, 1):
        if wallet in complete_wallets:
            api.logger.info(f'{wallet} is in the complete wallets list')
            continue
        amount = random_float(min_amount, max_amount)
        delay = random.randint(min_delay, max_delay)
        status, resp = api.withdraw_coin(token, amount, wallet, network)
        if status:
            complete_wallets.add(wallet)
            with open(complete_wallets_file, 'a') as fw:
                fw.write(f'{wallet}\n')
        else:
            continue
        if idx != len(wallets):
            api.logger.debug(f'delay {delay}s')
            for sec in range(delay * 10):
                if thread_stop_event and thread_stop_event.is_set():
                    return
                time.sleep(0.1)
