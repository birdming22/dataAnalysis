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

    Sensor Data is 10 bits and packed into two bytes.
    ------------------------------------------------
    | Byte | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
    ------------------------------------------------
    |      |     Data1         |     Data2         |
    ------------------------------------------------
    """
    def __init__(self):
        self.state = STATE.SYNC
        self.dataCount = 0
        self.data = []
        self.seqNum = None
        self.result = None

    def _unpack(self):
        dataLen = len(self.result)
        if dataLen % 2 != 0:
            print 'reuslt:', self.result
            self.result = self.result[:dataLen - 1]
            print 'reuslt:', self.result
        dataList = []
        for i in range(dataLen):
            if i % 2 == 0:
                print i
                # for hoya's pcb
                #dataList.append(1023 - self.result[i+1] * 32 - self.result[i])
                # for whyang's pcb
                dataList.append(self.result[i+1] * 32 + self.result[i])
        return dataList

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
                return self._unpack()
            self.dataCount += 1
            if self.dataCount == DATA.FRAME_SIZE:
                self.data.append(ch)
                self.result = list(self.data)
                self.dataCount = 0
                self.data = []
                self.state = STATE.SYNC
                return self._unpack()
            else:
                self.data.append(ch)
