
from enum import Enum


class JobState(Enum):
    ST_APPENDING = 'putting'
    ST_PUT_DONE = 'put done'
    ST_FINISH = 'all finished'


class Common(object):
    pass
