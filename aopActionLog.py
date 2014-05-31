# -*- coding: utf-8 -*
'''
Created on 2012-11-10

@author: vincent
'''
import sqlite3
import re
import uuid

SVNLOGDB ="/var/data/share/cmtools/svnlog.sqlite"

def writeAction(author, diff, changed, bugList, repos, revision):
    #参数解析
    fileChanged = {}
    for line in changed:
        line = re.sub("\s+", " ", line).strip()
        fileAction = line[0]
        fileName = line[2:]
        fileChanged[fileName] = fileAction
    diffLines = __diffSummary(diff) #变更行数
    
    for fileName, fileDiff in changed.items():
        fileAction = fileDiff[0]
        diffLines = diffLines + int(fileDiff[2:]) 
    if author=="":
        author="None"
    actionId = str(uuid.uuid4())
    sqlList = []
    actionSql = """INSERT INTO actions 
    (action_id, bug_id, file_count, line_count, author, repos, revision)
    VALUES ("%s", "%s", %d, %d, "%s", "%s", %d)"""
    sqlList.append(actionSql % (actionId, bugList[0], len(changed), 
                                diffLines, author, repos, int(revision)))
    for fileName, fileDiff in changed.items():
        fileAction = fileDiff[0]
        diffLines = diffLines + int(fileDiff[2:])     
        fileSql = """INSERT INTO files (action_id, filepath, change_type)
        VALUES ("%s", "%s", "%s")"""
        fileSql = fileSql % (actionId, fileName.strip(), fileAction)
        sqlList.append(fileSql)
    #写入其他的bugList    
    for bugId in bugList:
        if bugId == bugList[0]: 
            continue
        actionSql = """INSERT INTO actions 
        (action_id, bug_id, file_count, line_count, author, repos, revision) 
        VALUES ("%s", "%s", %d, %d, "%s", "%s", %d)"""
        actionSql = actionSql % (uuid.uuid4(), bugId, 0, 0, author, repos, int(revision))
        sqlList.append(actionSql)
    
    conn = sqlite3.connect(SVNLOGDB)
    cursor = conn.cursor()
    for sql in sqlList:
        #sys.stderr.write(sql + "\n")
        cursor.execute(sql)        
    conn.commit()
    conn.close()

def getUpdateSummary(firstDay, lastDay):
    conn = sqlite3.connect(SVNLOGDB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    sql = "SELECT * FROM actions where action_time > '%s' and action_time < '%s'"
    sql %= (firstDay.strftime("%Y-%m-%d"), lastDay.strftime("%Y-%m-%d"))
    cur.execute(sql)
    row = cur.fetchone()
    # 开始统计
    actionCount = 0
    totalLine = 0
    totalFile = 0
    bugList = {}
    userList = {}
    while row:
        actionCount += 1
        # Bug计数
        bugId = row["bug_id"]
        lineCount = int(row["line_count"])
        fileCount = int(row["file_count"])
        if not bugId in bugList:
            bugList[bugId] = 1
        else:
            bugList[bugId] += 1
        # 用户计数
        user = row["author"]
        if not user in userList:
            userList[user] = {}
            userList[user]["actionCount"] = 1
            userList[user]["bugList"] = []
            userList[user]["lineCount"] = 0
            userList[user]["fileCount"] = 0
        else:
            userList[user]["actionCount"] += 1
        if not bugId in userList[user]["bugList"]:
            userList[user]["bugList"].append(bugId)
        userList[user]["lineCount"] += lineCount
        userList[user]["fileCount"] += fileCount
        totalLine += lineCount
        totalFile += fileCount
        row = cur.fetchone()
    summary = {}
    summary["totalLine"] = totalLine
    summary["totalFile"] = totalFile
    summary["userList"] = userList
    summary["ticketList"] = bugList
    return summary

def __diffSummary(diff):
    totalLine = 0
    diffList = diff.split("\n")
    import string
    diffList = filter(None, map(string.strip, diffList))
    for line in diffList:
        if line[0] == "+" or line[0] == "-":
            totalLine = totalLine + 1
    return totalLine