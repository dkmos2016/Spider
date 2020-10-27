
import threading
import time
from Queue import Queue
import logging

from utils.common import JobState
from utils.Worker import Worker
import globalvar
from utils.LOGGER import LOGGER


class Monitor(threading.Thread):
    def __init__(self):
        super(Monitor, self).__init__()

    def run(self):
        # logger = logging.getLogger(threading.current_thread().name)
        while globalvar.jobstate != JobState.ST_FINISH:
            if not globalvar.event.is_set():
                LOGGER.info('waiting for jobs...')
                globalvar.event.wait(timeout=3)
            else:
                idx, value = globalvar.queue.get()
                LOGGER.info('get job {}, {}'.format(idx, value))
                if idx % 1000 == 0:
                    print('processed {}'.format(idx))
                # print('{}: {}'.format(idx, value))
                # specific worker
                worker = Worker(idx, value)
                worker.run()
                LOGGER.info('finish job {}, {}'.format(idx, value))
                time.sleep(0.3)

                if globalvar.queue.empty() and globalvar.event.is_set():
                    globalvar.jobstate = JobState.ST_FINISH
                    globalvar.event.clear()
                    break
        LOGGER.info('done.')
