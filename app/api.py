# -*- coding: utf-8 -*-
import logging
from pprint import pprint
from decimal import Decimal
from okex.Funding_api import FundingAPI
from okex.exceptions import OkexAPIException
from binance import Client
from binance.exceptions import BinanceAPIException


class BaseApi:
    def __init__(self):
        self.logger = logging.getLogger('okx_api')

    def get_coins(self):
        raise NotImplementedError

    def get_networks(self, coin):
        raise NotImplementedError

    def withdraw_coin(self, coin, amount, to_address, chain):
        raise NotImplementedError


class OkxApi(BaseApi):
    def __init__(self, api_key, api_secret_key, api_passphrase):
        super().__init__()
        self._api = FundingAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=api_passphrase,
                               use_server_time=False, flag='0')
        self._currency_data = {}  # dict of all coins and chains for this coin
        self._chain_min_fee_data = {}  # store minimum chain fee to send transaction

    def get_coins(self):
        if not self._currency_data:
            try:
                resp = self._api.get_currency()
                for coin in resp['data']:
                    ccy = coin['ccy']
                    if ccy not in self._currency_data:
                        self._currency_data[ccy] = [coin['chain']]
                    else:
                        self._currency_data[ccy].append(coin['chain'])
                    self._chain_min_fee_data[coin['chain']] = coin['minFee']
            except OkexAPIException as ex:
                self.logger.error(ex)
        return list(self._currency_data.keys())

    def get_networks(self, coin):
        self.get_coins()
        return self._currency_data.get(coin, [])

    def withdraw_coin(self, coin, amount, to_address, chain):
        self.get_coins()  # will cache data if not cached before
        try:
            resp = self._api.coin_withdraw_new(ccy=coin, amt=amount, dest=4, toAddr=to_address,
                                               fee=self._chain_min_fee_data.get(chain, 0), chain=chain)
        except OkexAPIException as ex:
            self.logger.error(ex)
            return
        if resp['code'] != '0':  # say after audit to Andrey the code 949328
            status = False
            self.logger.error('%s; Address %s; %s' % (resp['code'], to_address, resp['msg']))
        else:
            status = True
            self.logger.info(f'OK: {amount} {coin} to {to_address} on {chain}')
        return status, resp


class BinanceApi(BaseApi):
    def __init__(self, api_key, api_secret_key):
        super().__init__()
        self._client = Client(api_key=api_key, api_secret=api_secret_key)
        self._coin_data = {}

    def get_coins(self):
        if not self._coin_data:
            resp = self._client.get_all_coins_info()
            for coin in resp:
                if coin['coin'] not in self._coin_data:
                    self._coin_data[coin['coin']] = coin
        return list(self._coin_data.keys())

    def get_networks(self, coin):
        self.get_coins()
        if coin in self._coin_data:
            return [n['network'] for n in self._coin_data[coin]['networkList']]
        else:
            return []

    def withdraw_coin(self, coin, amount, to_address, chain):
        self.get_coins()
        network = None
        fee = 0.0
        withdraw_integer_multiple = Decimal('0.00000001')
        # get coin information
        if coin not in self._coin_data:
            self.logger.error(f'No such coin: {coin}')
            return False, None
        # get network fee
        for n in self._coin_data[coin]['networkList']:
            if n['network'] == chain:
                network = n
                fee = float(n['withdrawFee'])
                withdraw_integer_multiple = Decimal(n['withdrawIntegerMultiple'])
                break
        if not network:
            self.logger.error(f'No such network: {chain}')
            return False, None
        # withdraw API call
        try:
            total_amount = round(amount+fee, withdraw_integer_multiple.as_tuple().exponent * -1)
            resp = self._client.withdraw(coin=coin, network=chain, address=to_address, amount=total_amount)
        except BinanceAPIException as ex:
            self.logger.error('Address %s; %s' % (to_address, ex))
            return False, None
        else:
            self.logger.info(f'OK: {amount} {coin} to {to_address} on {chain}')
            return True, resp
