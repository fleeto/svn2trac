#!/usr/bin/python
# -*- coding: utf-8 -*
'''
Created on 2012-11-10

@author: vincent
'''
import sys
import aopTrac
import aopSvnLook
import aopActionLog
import re
import os

TXTFILE = ['htm' ,'ini', 'conf', 'mxml',
           'txt',  'xml', 'ps', 'php', 
           'java', 'phtml', 'html', 'css',  'js', 'jsp', 'sql', 'wsdl', 
           'info', 'bat', 'sh', 'xsd']
def __isTxt(fileName):
    ext = os.path.os.path.splitext(fileName)
    return (len(ext) < 5) and (TXTFILE.count(ext) > 0)

def main(repo, rev, tracEnv):
    sl = aopSvnLook.SvnLook()
    sl.target = rev
    sl.targetType = "r"
    sl.repository = repo
    #record changed contents
    svnAuthor = sl.getAuthor()
    svnDiff = sl.getDiff()
    svnChanged = sl.getChanged()
    fileChanged = {}
    for line in svnChanged:
        fileName = line[2:]
        fileAction = line[0]
        fileSize = 0
        if (fileAction == "A") and (__isTxt(fileName)):
            fileContent = sl.cat(fileName)
            fileSize = len(fileContent.split("\n"));
        fileChanged[fileName] = "%s %d" % (fileAction, fileSize)
    svnLog = sl.getLog()
    ticketList = re.findall("\[ticket:(\d+)\]", svnLog)
    aopActionLog.writeAction(svnAuthor, svnDiff, fileChanged, ticketList, repo, rev)
    #Add a changeset to trac
    trac = aopTrac.Trac(tracEnv)
    trac.appendChangeset(repo, rev)
 
    
if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.stderr.write("Usage: %s Repositorypath TXN TracProjectPath\n" % (sys.argv[0]))
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
