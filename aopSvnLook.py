# -*- coding: utf-8 -*
'''
Created on 2012-11-9

@author: vincent
'''
import os
import aopMiscUtils

class SvnLook:
    def __init__(self, basePath = "/usr/bin"):
        self.lookCmd = os.path.join(basePath, "svnlook")
        self.repository = ""
        self.target = ""
        self.targetType = "r"
        
    def __getLookResult(self, cmdpath, subcommand, repos, para):
        cmd = '%s %s %s %s' % (cmdpath, subcommand, para, repos)
        return aopMiscUtils.execCommand(cmd)
    def __formatResult(self, s):
        retList = s.split("\n")
        from string import strip
        return filter(None, map(strip, retList))

    def getLog(self):
        ret = self.__getLookResult(self.lookCmd, "log",
                        "-%s %s" % (self.targetType, self.target),
                        self.repository)
        return ret
    def getAuthor(self):
        ret = self.__getLookResult(self.lookCmd, "author",
                        "-%s %s" % (self.targetType, self.target),
                        self.repository)
        return ret.strip()
    def getChanged(self):
        ret = self.__getLookResult(self.lookCmd, "changed",
                        "-%s %s" % (self.targetType, self.target),
                        self.repository)
        return self.__formatResult(ret)
    def getDiff(self):
        ret = self.__getLookResult(self.lookCmd, "diff",
                        "-%s %s" % (self.targetType, self.target),
                        self.repository)
        return ret
    def cat(self, fileName):
        ret = aopMiscUtils.execCommand(
                            '%s %s -%s %s %s %s' % 
                            (self.lookCmd, "cat", self.targetType,
                             self.target, self.repository, fileName))
        return ret
