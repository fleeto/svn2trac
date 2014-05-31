#!/usr/bin/python
# -*- coding: utf-8 -*

'''
Created on 2012-11-9

@author: vincent
'''
import sys
import aopSvnLook
import aopTrac

def main():
    print "Hello"
    svnLook = aopSvnLook.SvnLook()
    svnLook.repository = "/var/data/repos/test"
    svnLook.target = "1"
    svnLook.targetType = "r"
    print svnLook.getChanged()
    
    Trac = aopTrac.Trac("/var/data/trac/2012001518/")
    print Trac.getValidTicket(1)
if __name__ == '__main__':
    main()
else:
    sys.exit(1)
