
# encoding:utf8

import logging


def setLoggerFormat(fmt):
    logging.basicConfig(format=fmt)


logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(threadName)-10s: [func: %(funcName)-10s] [line: %(lineno)3d] - %(levelname)-6s: %(message)s')
LOGGER = logging.getLogger('BaseMonitor')
