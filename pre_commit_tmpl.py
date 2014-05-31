#!/usr/bin/python
# -*- coding: utf-8 -*
'''
Created on 2012-11-10

@author: vincent
'''

import sys
import aopTrac
import aopSvnLook
import re

def main(repo, txn, tracEnv):
    sl = aopSvnLook.SvnLook()
    sl.target = txn
    sl.targetType = "t"
    sl.repository = repo
    svnLog = sl.getLog()
    if len(svnLog) < 10:
        sys.stderr.write("Your message '%s' is too short(%d).\n" % (svnLog, len(svnLog)))
        sys.stderr.write ("Please enter a commit message which details what has changed during this commit.")
        sys.exit(1)
    ticketList = re.findall("\[ticket:(\d+)\]", svnLog)
    if len(ticketList) < 1:
        sys.stderr.write("""Please input a comment about which ticket you are working on.
The first line should be [ticket:1234]""")
        sys.exit(1)
    trac = aopTrac.Trac(tracEnv)
    for ticket in ticketList:
        ret = trac.getValidTicket(int(ticket))
        if not ret:
            sys.stderr.write("The ticket id in your log is invalid.")
            sys.exit(1)
    
    

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.stderr.write("Usage: %s Repositorypath TXN TracProjectPath\n" % (sys.argv[0]))
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

