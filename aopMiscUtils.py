# -*- coding: utf-8 -*
'''
Created on 2012-11-10

@author: vincent
'''
import subprocess

ERRORLOG = "/tmp/aopexec.error.log"

def execCommand(cmd):
    p = subprocess.Popen(cmd, shell=True, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE, 
                         stdin=subprocess.PIPE)
    output, errInfo = p.communicate()
    if len(errInfo) > 0:
        return errInfo
    else:
        return output
