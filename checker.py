#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 20:25:29 2020
@author: sincorchetes
@blog: https://echemosunbitstazo.es
@twitter: @sincorchetes
"""
import subprocess as Request
from sys import exit as exit
from sys import argv as shell_args


class Nagios:
    def __init__(self):
        self.ok = 0
        self.warning = 2
        self.critical = 1
        self.unknown = 3
    
    def set_status(self,status):
        if status == self.ok:
            exit(self.ok)
        elif status == self.warning:
            exit(self.warning)
        elif status == self.critical:
            exit(self.critical)
        else:
            exit(self.unknown)

class Mensajes:
    msg_wks = "Hay %i de %i workers en total. | busy=%i;%i;%i total=%i"
    msg_wks_unknown = "Hubo un problema para obtener los workers, por favor revisar. "
    no_arg = "Faltan argumentos."
    something_wrong = "Hubo un problema"
    
class Consulta:
    def __init__(self,host):
        self.nagios = Nagios()
        self.msg = Mensajes()
        self.url = "http://%s/server-status?auto" % (host)
        self.param = [ "curl","-s",self.url]
        self.get_raw_data = Request.Popen(self.param,shell=False,stdout=Request.PIPE)
        self.parse_data = self.get_raw_data.stdout.read().decode("utf-8").split()
        
        self.total_access = int(self.parse_data[2])
        self.total_kbytes = int(self.parse_data[5])
        self.uptime = int(self.parse_data[7])
        self.pet_sec = float(self.parse_data[9])
        self.bytes_sec = float(self.parse_data[11])
        self.bytes_req = float(self.parse_data[13])
        self.busy_wks = int(self.parse_data[15])
        self.idle_wks = int(self.parse_data[17])
        
    def wks_status(self,wks,warning,critical):
        if self.busy_wks < warning and self.busy_wks < critical:
            print(self.msg.msg_wks % (self.busy_wks,wks,self.busy_wks,warning,critical,wks))
            self.nagios.set_status(0)
        elif self.busy_wks >= warning and self.busy_wks < critical:
            print(self.msg.msg_wks % (self.busy_wks,wks,self.busy_wks,warning,critical,wks))
            self.nagios.set_status(2)
        elif self.busy_wks > warning and self.busy_wks >= critical:
            print(self.msg.msg_wks % (self.busy_wks,wks,self.busy_wks,warning,critical,wks))
            self.nagios.set_status(1)
        else:
            print(self.msg.msg_wks_unknown)
            self.nagios.set_status(3)
            
            
    def __del__(self):
        pass

if __name__ == "__main__":
    
    if len(shell_args) == 1:
        print(Mensajes().no_arg)
    
    elif shell_args[2] == "workers":
       workers = Consulta(shell_args[1])
       workers.wks_status(int(shell_args[3]),int(shell_args[4]),int(shell_args[5]))
       del workers
    else:
        print(Mensajes().something_wrong)
    
