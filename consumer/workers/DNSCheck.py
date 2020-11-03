
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


class DNSCheck(object):
    domains = ['iyuji.cn', 'xfyun.cn']
    result = ''
    # dns = '114.114.114.114'
    dns = ''

    def __init__(self, idx, sub_domain):
        self.idx = idx
        self.sub_domain = sub_domain

    def run(self):
        for _domain in self.domains:
            domain = '{}.{}'.format(self.sub_domain, _domain)
            cont = popen('nslookup {} {}'.format(domain, self.dns)).read()

            # print('nslookup {}'.format(domain))

            globalvar.lock.acquire()
            # LOGGER.info("got lock")

            if 'Name:' in cont:
                # conts = cont.split('Non-authoritative answer:')[-1]
                LOGGER.info(domain)

                # globalvar.results.append(conts)
                globalvar.results.write(domain)
                globalvar.lock.release()
                # LOGGER.info("release lock")
                time.sleep(1)

            else:
                globalvar.lock.release()
                pass

