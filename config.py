# API access
OKX_API_KEY = 'OKEX_API_KEY'
OKX_API_SECRET_KEY = 'OKEX_API_SECRET_KEY'
OKX_API_PASSPHRASE = 'OKEX_API_PASSPHRASE'

BINANCE_API_KEY = 'BINANCE_API_KEY'
BINANCE_API_SECRET_KEY = 'BINANCE_API_SECRET'

# files
WALLETS_FILE = 'wallets.txt'
COMPLETE_WALLETS_FILE = 'complete_wallets.txt'

# logging
LOG_TO_FILE = True
LOG_FILE = 'default.log'

# default VAR values
DEFAULT_MIN_DELAY = 30
DEFAULT_MAX_DELAY = 60

DEFAULT_TOKEN = 'ETH'
DEFAULT_NETWORK_OKX = 'ETH-Arbitrum One'
DEFAULT_NETWORK_BINANCE = 'ARBITRUM'

DEFAULT_MIN_AMOUNT = 0.001
DEFAULT_MAX_AMOUNT = 0.002

# you can store your VARs in the local_config.py file also
try:
    from local_config import *
except ImportError:
    pass
