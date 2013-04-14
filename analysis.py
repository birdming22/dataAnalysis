#!/usr/bin/env python
# encoding: utf-8

import datalink

import sys
import scipy
import scipy.fftpack
import pylab
from scipy import pi
'''
t = scipy.linspace(0,120,4000)
acc = lambda t: 10*scipy.sin(2*pi*2.0*t) + 5*scipy.sin(2*pi*8.0*t) + 2*scipy.random.random(len(t))

signal = acc(t)

FFT = abs(scipy.fft(signal))
freqs = scipy.fftpack.fftfreq(signal.size, t[1]-t[0])

pylab.subplot(211)
pylab.plot(t, signal)
pylab.subplot(212)
pylab.plot(freqs,20*scipy.log10(FFT),'x')
pylab.show()
'''

def main():
    if len(sys.argv) < 2:
        print 'usage: analysis.py sample/1.dat'
        return

    IN_FILE = sys.argv[1]
    dl = datalink.Datalink()
    dataList = []
    # read file
    with open(IN_FILE, 'rb') as f:
        c = f.read(1)
        dl.processMessage(ord(c))
        while c:
            #print ord(c)
            c = f.read(1)
            try:
                data = dl.processMessage(ord(c))
                if data is not None:
                    if len(data) == 8:
			dataList.extend(data)
                    else:
                        print 'corrupt data:', data
            except:
                pass

    t = scipy.linspace(0, 100, len(dataList))

    FFT = abs(scipy.fft(dataList))
    freqs = scipy.fftpack.fftfreq(len(dataList), t[1]-t[0])

    pylab.subplot(211)
    pylab.plot(t, dataList)
    pylab.subplot(212)
    pylab.plot(freqs,20*scipy.log10(FFT),'x')

    pylab.show()


if __name__ == '__main__':
    main()
