# -*- coding: utf-8 -*-
from struct import pack


class TimeZone(object):

    def __init__(self, flag, tz1, tz2, tz3):
        self.flag = flag
        self.tz1 = tz1
        self.tz2 = tz2
        self.tz3 = tz3

    def repack(self):
        return pack("<IIII", 1 if self.flag else 0, self.tz1, self.tz2, self.tz3)

    def __str__(self):
        return '<Timezone>: {} : ({} {}, {})'.format(self.flag, self.tz1, self.tz2, self.tz3)

    def __repr__(self):
        return '<Timezone>: {} : ({} {}, {})'.format(self.flag, self.tz1, self.tz2, self.tz3)

