import threading

from threading import Lock, RLock
from Queue import Queue
from utils.common import JobState


def setQueue(size):
    global queue
    queue = Queue(size)


queue = Queue(50)
event = threading.Event()
jobstate = JobState.ST_APPENDING

lock = Lock()
results = open('result.log', 'w')
