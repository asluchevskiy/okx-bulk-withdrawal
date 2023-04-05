# -*- coding: utf-8 -*-
from api import API
import config
import logging
import time
import random
from utils import random_float, setup_logging


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
        print(token, amount, wallet, network, delay)
        resp = api.withdraw_coin(token, amount, wallet, network)
        if resp['code'] == '0':
            complete_wallets.add(wallet)
            with open(config.COMPLETE_WALLETS_FILE, 'a') as fw:
                fw.write(f'{wallet}\n')
        else:
            continue
        if idx != len(wallets):
            for sec in range(delay*10):
                if thread_stop_event and thread_stop_event.is_set():
                    return
                time.sleep(0.1)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    okx_api = API(api_key=config.API_KEY, api_secret_key=config.API_SECRET_KEY, api_passphrase=config.API_PASSPHRASE)
    if config.LOG_TO_FILE:
        setup_logging(okx_api.logger, config.LOG_FILE)
    run_withdraw(api=okx_api,
                 wallets_file=config.WALLETS_FILE,
                 complete_wallets_file=config.COMPLETE_WALLETS_FILE,
                 token=config.DEFAULT_TOKEN,
                 network=config.DEFAULT_NETWORK,
                 min_amount=config.DEFAULT_MIN_AMOUNT,
                 max_amount=config.DEFAULT_MAX_AMOUNT,
                 min_delay=config.DEFAULT_MIN_DELAY,
                 max_delay=config.DEFAULT_MAX_DELAY)
