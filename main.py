# -*- coding: utf-8 -*-
from api import API
import config
import logging
import time
import random
from utils import random_float

api = API(api_key=config.API_KEY, api_secret_key=config.API_SECRET_KEY, api_passphrase=config.API_PASSPHRASE)


def setup_logging(log_file):
    # logging file handler
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # log message formatting
    file_handler.setFormatter(formatter)
    api.log.addHandler(file_handler)


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


def run_withdraw(token, network, min_amount, max_amount, min_delay, max_delay):
    wallets = read_wallet_file(config.WALLETS_FILE)
    complete_wallets = set(read_wallet_file(config.COMPLETE_WALLETS_FILE))
    for idx, wallet in enumerate(wallets, 1):
        if wallet in complete_wallets:
            api.log.info(f'{wallet} is in the complete wallets list')
            continue
        amount = random_float(min_amount, max_amount)
        delay = random.randint(min_delay, max_delay)
        print(token, amount, wallet, network, delay)
        resp = api.withdraw_coin(token, amount, wallet, network)
        if resp['code'] == '0':
            complete_wallets.add(wallet)
            with open(config.COMPLETE_WALLETS_FILE, 'a') as fw:
                fw.write(f'{wallet}\n')
        if idx != len(wallets):
            time.sleep(delay)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    if config.LOG_TO_FILE:
        setup_logging(config.LOG_FILE)
    run_withdraw(token=config.DEFAULT_TOKEN,
                 network=config.DEFAULT_NETWORK,
                 min_amount=config.DEFAULT_MIN_AMOUNT,
                 max_amount=config.DEFAULT_MAX_AMOUNT,
                 min_delay=config.DEFAULT_MIN_DELAY,
                 max_delay=config.DEFAULT_MAX_DELAY)
