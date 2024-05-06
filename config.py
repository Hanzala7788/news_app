# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# NewsAPI key (replace with your own key)
NEWS_API_KEY = 'b81ea533a66e4e86add5feacf4ed40bb'

# Default country for top headlines
DEFAULT_COUNTRY = 'in'

# Cache timeout in seconds (1 hour)
CACHE_TIMEOUT = 3600

# Enable/disable debug mode
DEBUG = True