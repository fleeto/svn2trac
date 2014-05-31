# -*- coding: utf-8 -*
'''
Created on 2012-11-10

@author: vincent
'''
from trac.env import open_environment
import aopMiscUtils

TRACADMIN = "trac-admin"

class Trac:
    def __init__(self, envpath):
        self.envPath = envpath
        env = open_environment(envpath)
        self.db = env.get_db_cnx()
    def getValidTicket(self, ticket):
        cursor = self.db.cursor()
        cursor.execute("SELECT COUNT(id) FROM ticket WHERE "
                       "status <> 'closed' AND id = %d" % ticket)
        row = cursor.fetchone()        
        return row and row[0]>=1
    def appendChangeset(self, repos, revision):
        cmdPattern = '%s %s changeset added %s %d'
        cmd = cmdPattern % (TRACADMIN, self.envPath, repos, int(revision))
        return aopMiscUtils.execCommand(cmd)