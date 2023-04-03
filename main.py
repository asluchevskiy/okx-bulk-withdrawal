# -*- coding: utf-8 -*-
from api import API
import config
import logging
import time
import random
from utils import random_float

api = API(api_key=config.API_KEY, api_secret_key=config.API_SECRET_KEY, api_passphrase=config.API_PASSPHRASE)


def run():
    wallets = []
    with open(config.WALLETS_FILE, 'r') as f:
        for wallet in f:
            wallet = wallet.strip()
            if wallet:
                wallets.append(wallet)
    for idx, wallet in enumerate(wallets, 1):
        amount = random_float(config.DEFAULT_MIN_AMOUNT, config.DEFAULT_MAX_AMOUNT)
        delay = random.randint(config.DEFAULT_MIN_DELAY, config.DEFAULT_MAX_DELAY)
        # print(f'amount: {amount}, address: {wallet}, delay: {delay}, coin: {config.DEFAULT_TOKEN}, '
        #       f'network: {config.DEFAULT_NETWORK}')
        api.withdraw_coin(config.DEFAULT_TOKEN, amount, wallet, config.DEFAULT_NETWORK)
        if idx != len(wallets):
            time.sleep(delay)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    run()
