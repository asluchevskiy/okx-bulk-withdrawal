# -*- coding: utf-8 -*-
import config
import logging
from app.api import BinanceApi
from app.utils import setup_logging, run_withdraw


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    api = BinanceApi(api_key=config.BINANCE_API_KEY, api_secret_key=config.BINANCE_API_SECRET_KEY)
    if config.LOG_TO_FILE:
        setup_logging(api.logger, config.LOG_FILE)
    run_withdraw(api=api,
                 wallets_file=config.WALLETS_FILE,
                 complete_wallets_file=config.COMPLETE_WALLETS_FILE,
                 token=config.DEFAULT_TOKEN,
                 network=config.DEFAULT_NETWORK_BINANCE,
                 min_amount=config.DEFAULT_MIN_AMOUNT,
                 max_amount=config.DEFAULT_MAX_AMOUNT,
                 min_delay=config.DEFAULT_MIN_DELAY,
                 max_delay=config.DEFAULT_MAX_DELAY)
