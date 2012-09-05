#!/usr/bin/env python
# encoding: utf-8

import datalink

IN_FILE = "71.dat"

def main():
    dl = datalink.Datalink()
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
                    if len(data) != 16:
                        print 'data:', data
            except:
                pass


if __name__ == '__main__':
    main()
