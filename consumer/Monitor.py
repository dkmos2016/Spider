
import threading
import time
from Queue import Queue
import logging

from utils.common import JobState
from consumer.workers.DNSCheck import DNSCheck as Worker
import globalvar
from utils.LOGGER import LOGGER


class Monitor(threading.Thread):
    def __init__(self):
        super(Monitor, self).__init__()

    def run(self):
        # logger = logging.getLogger(threading.current_thread().name)
        while globalvar.jobstate != JobState.ST_FINISH:
            if not globalvar.event.is_set():
                LOGGER.debug('waiting for jobs...')
                globalvar.event.wait(timeout=3)
            else:
                idx, value = globalvar.queue.get()
                LOGGER.debug('get job {}, {}'.format(idx, value))
                if idx % 1000 == 0:
                    LOGGER.debug('processed {}'.format(idx))
                # print('{}: {}'.format(idx, value))
                # specific worker
                worker = Worker(idx, value)
                worker.run()
                LOGGER.debug('finish job {}, {}'.format(idx, value))
                time.sleep(0.3)

                if globalvar.queue.empty() and globalvar.event.is_set():
                    globalvar.jobstate = JobState.ST_FINISH
                    globalvar.event.clear()
                    break
        LOGGER.debug('done.')
