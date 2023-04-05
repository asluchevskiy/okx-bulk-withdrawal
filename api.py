# -*- coding: utf-8 -*-
import logging
from okex.Funding_api import FundingAPI
from okex.exceptions import OkexAPIException


class API:
    def __init__(self, api_key, api_secret_key, api_passphrase):
        self._api = FundingAPI(api_key=api_key, api_secret_key=api_secret_key, passphrase=api_passphrase,
                               use_server_time=False, flag='0')
        self.logger = logging.getLogger('okx_api')
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
            self.logger.error('%s; Address %s; %s' % (resp['code'], to_address, resp['msg']))
        else:
            self.logger.info(f'OK: {amount} {coin} to {to_address} on {chain}')
        return resp
