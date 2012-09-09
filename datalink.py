#!/usr/bin/env python
# encoding: utf-8
"""
 Data Link is for protocol between android and arduino
 
 @author birdming22
"""
from constant import *

class Datalink:
    """
    -----------------------------------------------
    | 255 | SeqNum | Data1 | Data2 | ... | Data16 |
    -----------------------------------------------
    """
    def __init__(self):
        self.state = STATE.SYNC
        self.dataCount = 0
        self.data = []
        self.seqNum = None
        self.result = None

    def processMessage(self, ch):
        if self.state == STATE.SYNC:
            if ch == 255:
                self.state = STATE.SEQ
        elif self.state == STATE.SEQ:
            # validata
            if self.seqNum == ch:
                self.seqNum = ch + 1
                if self.seqNum == 128:
                    self.seqNum = 0
                self.state = STATE.DATA
            else:
                if self.seqNum is None:
                    self.seqNum = ch + 1
                    if self.seqNum == 128:
                        self.seqNum = 0
                    self.state = STATE.DATA
                else:
                    print 'validation error'
                    print 'seqNum', self.seqNum
                    print 'ch:', ch
                    print 'result:', self.result
                    print 'data:', self.data
                    self.state = STATE.SYNC
                    self.seqNum = None
        else:
            if ch == 255:
                self.result = list(self.data)
                self.dataCount = 0
                self.data = []
                self.state = STATE.SYNC
                return self.result
            self.dataCount += 1
            if self.dataCount == DATA.FRAME_SIZE:
                self.data.append(ch)
                self.result = list(self.data)
                self.dataCount = 0
                self.data = []
                self.state = STATE.SYNC
                return self.result
            else:
                self.data.append(ch)
