#!/usr/bin env python2
# -*- coding: utf-8 -*-
""" Permet de lancer le server applicatif speechserver 
    USAGE: python server.py PORT 
    default port: 8010 """

import speechserver

if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 2:
        try:
            PORT = int(sys.argv[1])
        except TypeError:
            print("Please provide an int !")
    else:
        PORT = 8010
        print("Port set to default : %s" % PORT)

    print("Launching server ...")
    speechserver.main.run(PORT)
