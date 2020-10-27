import threading
import globalvar
from time import sleep
from LOGGER import LOGGER as logger
from utils.common import JobState
from Queue import Full


class Provider(threading.Thread):

    def __init__(self, fpath):
        self._file = open(fpath, 'r')
        super(Provider, self).__init__()

    def procedure(self):
        for idx, line in enumerate(self._file.readlines()):
            line = line.replace('\n', '')
            # if globalvar.queue.full():
            #     logger.info("queue is full, waiting...")
            # else:
            #     logger.info("put data {}".format(line))
            while True:
                try:
                    globalvar.queue.put((idx+1, line), timeout=3)
                    logger.info("put data {}, {}".format(idx, line))
                    break
                except Full as e:
                    logger.info("queue is full, waiting...")

            if not globalvar.queue.empty():
                globalvar.jobstate = JobState.ST_APPENDING
                globalvar.event.set()

        globalvar.jobstate = JobState.ST_PUT_DONE

    def run(self):
        self.procedure()
        super(Provider, self).run()
