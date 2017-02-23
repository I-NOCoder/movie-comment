

import os
import tempfile


__version__ = '0.1.2'
'''
DATA_DB = os.path.join(tempfile.gettempdir(), 'fake_useragent_{version}.json'.format(  # noqa
    version=__version__,
))
'''
HERE = os.path.abspath(os.path.dirname(__file__))
DATA_DB = os.path.join(HERE, 'data/fake_useragent.json') #get abspath

BROWSERS_STATS_PAGE = 'http://www.w3schools.com/browsers/browsers_stats.asp'

BROWSER_BASE_PAGE = 'http://useragentstring.com/pages/useragentstring.php?name={browser}'  # noqa

BROWSERS_COUNT_LIMIT = 50

REPLACEMENTS = {
    ' ': '',
    '_': '',
}

SHORTCUTS = {
    'internet explorer': 'internetexplorer',
    'ie': 'internetexplorer',
    'msie': 'internetexplorer',
    'google': 'chrome',
    'googlechrome': 'chrome',
    'ff': 'firefox',
}

OVERRIDES = {
    'IE': 'Internet Explorer',
}

HTTP_TIMEOUT = 10

HTTP_RETRIES = 5

HTTP_DELAY = 5

try:
    from config import *  # noqa
except ImportError:
    pass
