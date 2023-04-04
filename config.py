# API access
API_KEY = 'OKEX_API_KEY'
API_SECRET_KEY = 'OKEX_API_SECRET_KEY'
API_PASSPHRASE = 'OKEX_API_PASSPHRASE'

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
DEFAULT_NETWORK = 'ETH-Arbitrum one'

DEFAULT_MIN_AMOUNT = 0.001
DEFAULT_MAX_AMOUNT = 0.002

# you can store your VARs in the local_config.py file also
try:
    from local_config import *
except ImportError:
    pass
