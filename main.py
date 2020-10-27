
import threading
import time
import base64

from utils.BaseSpider import BaseSpider
from utils.Monitor import Monitor
import globalvar
from utils.LOGGER import LOGGER as logger
from utils.Provider import Provider


def test():
    pass


data = 'Jslc!wPjTsPbDY8LHju5wYUjRtFDNYZXjmOBSPfviZ' \
       '!MZRdfOofA0Hh1h2IbGgRl2Nov7nRZXhdTzaVbIBvWXYRvhjgSnmjAoHWZOTRdSGPtKxgQmm2gwNChgDf8qDC2pvuY6OHVICaNvAsXs6zwg' \
       '!0UVR6kdv8f0nmQ6rZjQGMC7!pVQjvB3ocPAVCGzc-EW6gThwqrgSri5HatWM6XUA~~ '

if __name__ == '__main1__':
    _data = data.replace('~', '=').replace('!', '/').replace('-', '+')
    _data = base64.decodestring(_data)
    baseSpider = BaseSpider(_data)
    baseSpider.start()

    for i in range(10):
        monitor = Monitor()
        monitor.start()

    while threading.active_count() > 1:
        time.sleep(3)
    else:

        result = ''

        for key, value in sorted(globalvar.results.items(), key=lambda d: d[0], reverse=False):
            # print('key: {}, value: {}'.format(key, value))
            result += value

        print('{}'.format(result))

        print('---------all thread done---------')

if __name__ == '__main__':
    provider = Provider(r"H:\Workspace\pycharm\Spider\log")
    provider.start()

    for i in xrange(30):
        monitor = Monitor()
        monitor.start()
        # monitor.start()

    while True:
        if threading.active_count() > 1:
            logger.info("some threads not finish. Just waiting...")
            time.sleep(10)
        else:
            break

    # with open('result.txt', 'w') as f:
    #     for value1, value2 in globalvar.results:
    #         f.write('{} {}\n'.format(value1, value2))

    logger.info('main thread done.')
