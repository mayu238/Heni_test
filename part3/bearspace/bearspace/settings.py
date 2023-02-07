from datetime import datetime

BOT_NAME = 'bearspace'

SPIDER_MODULES = ['bearspace.spiders']
NEWSPIDER_MODULE = 'bearspace.spiders'

LOG_LEVEL = 'INFO'
LOG_FILE = 'C:/Users/Mayu/Desktop/test/part3/logs/bearspace%s_%s.txt' % (BOT_NAME,datetime.today().strftime("%Y-%m-%d"))
ROBOTSTXT_OBEY = True

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.05
AUTOTHROTTLE_MAX_DELAY = 0.1
AUTOTHROTTLE_DEBUG = False
CONCURRENT_REQUESTS_PER_DOMAIN = 6
DOWNLOAD_TIMEOUT = 90
DOWNLOAD_DELAY = 0.05
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'