import threading
import time
from Queue import Queue
from random import randint

from utils.common import JobState
from utils.LOGGER import LOGGER

import globalvar


class BaseSpider(threading.Thread):
    def __init__(self, cipher):
        self.cipher = cipher
        super(BaseSpider, self).__init__()

    def run(self):
        sz = len(self.cipher)
        LOGGER.info('total size: {}'.format(sz))
        for idx in range(0, sz + 1, 16):
            # for idx in range(-1, -49, -16):
            globalvar.queue.put((idx, self.cipher[0:idx:]))
            if not globalvar.queue.empty():
                globalvar.jobstate = JobState.ST_APPENDING
                globalvar.event.set()

        globalvar.jobstate = JobState.ST_PUT_DONE
