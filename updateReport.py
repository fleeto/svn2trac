# -*- coding: utf-8 -*
'''
Created on 2012-11-10

@author: vincent
'''
import sys
import re
import datetime
import aopActionLog
def __getDateFromStr(dateStr):
    mat = re.match("(\d+)-(\d+)-(\d+)", dateStr)
    if not mat:
        sys.exit(1)
    year = int(mat.group(1))
    month = int(mat.group(2))
    day = int(mat.group(3))
    return datetime.date(year, month, day)
def main(fromDate, toDate):
    firstDay = __getDateFromStr(fromDate)
    lastDay = __getDateFromStr(toDate)
    summary = aopActionLog.getUpdateSummary(firstDay, lastDay)
    print summary
 
         
if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: %s Repositorypath TXN TracProjectPath\n" % (sys.argv[0]))
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2])