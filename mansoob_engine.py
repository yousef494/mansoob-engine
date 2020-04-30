import time, subprocess, shlex
import os
from time import gmtime, strftime
from datetime import datetime
from array import array
from Properties import Properties
import sensor_reader as sensor_reader
import most_common
import requests

class MansoobEngine():
    
    PROP_FILE = '/home/pi/myworkspace/mansoob_v2/wtli.prop'

    def __init__(self):
        prop = Properties()
        prop.load(open(self.PROP_FILE))
        
        self.counter = 0
        self.tank_hight = int(prop['tank_hight'])        
        state = self.readLastState()
        self.global_pdata = state[1]
        
        self.prcessing_interval = int(prop['prcessing_interval'])     #in seconds,  300s = 5m
        self.set_prcessing_interval = int(prop['set_prcessing_interval'])     #in seconds,  300s = 5m
        self.r_prcessing_interval = int(prop['r_prcessing_interval'])     #in seconds,  300s = 5m

        self.api_url = prop['api_url']

        self.local_file = prop['local_file']
        self.state_file = prop['state_file']
        self.info_log = prop['info_log']
        self.error_log = prop['error_log']
        self.warning_log = prop['warning_log']
        self.stat_log = prop['stat_log']
        self.test_log = prop['test_log']
        self.access_tocken = prop['access_tocken']
        self.user_id = prop['user_id']
        self.device_id = prop['device_id']
        
    def main(self):
        self.run_command()

    def run_command(self):
        self.log("info","run_command:starting the script...")
        self.set_init_level()
        self.rest_prcessing_interval(self.set_prcessing_interval)
        output = self.read_currentLevel()
        if output:
            if(self.store(output.strip()) == False):
                self.rest_prcessing_interval(self.r_prcessing_interval)
        return output
    

    def read_currentLevel(self):
        output = sensor_reader.read()
        return output

    #Check if invalid
    def invalide(self, data, adata):
        try:
            if(data < 0):
                return True
            if(data - adata < -10):
                return True
            if(data - adata > 10):
                return True
            if(data > self.tank_hight-12):
                return True
            self.global_pdata = data
            self.log("info","invalide:valid data... "+str(data))
            return False
        except Exception, e:
            self.log("error","invalide:Error while validating the data..."+str(e))
            return True


    def set_init_level(self):
        self.log("info","set_init_level:getting the initial level...")
        i = 0
        a = array("i")
        while i < 4:
            output = self.read_currentLevel()
            if output:
                data = self.normalize(output.strip()) 
                if(data != "NAN"):
                    if(self.invalide(int(data),int(data)) == False):
                        a.append(int(data))
                        i = i+1

        self.global_pdata = most_common.most_common(a)
        return 0


    def store(self, sdata):
        data = self.normalize(sdata)
        if(data == "NAN"):
            return False
        if(data != "NAN"):
            invalid = self.invalide(int(data),self.global_pdata)
            if(invalid == True):
                self.counter = self.counter + 1
                if(self.counter > 3):
                    self.set_init_level()
                    self.counter = 0
                return False
            if(invalid == False):
                self.global_pdata = int(data)
                timestamp = str(datetime.now())
                # SHOULD BE TO API
                self.call_api(timestamp,data)
                self.storeState(data)
                self.counter = 0
                return True


    def rest_prcessing_interval(self, m):
        self.prcessing_interval = m

    def normalize(self, data):
        try:
            norm = self.tank_hight - int(data)
            return str(norm)
        except:
            self.log("warning","normalize:NAN, Problem in resolving the data... "+data)
            return str("NAN")

    def call_api(self, timestamp, data):
        json_data = {'timestamp': timestamp, 'level': data,
         'device_id': self.device_id, 'user_email': self.user_id}
        headers = {'x-access-token-api': self.access_tocken}
        response = requests.post(self.api_url, data = json_data, headers=headers)
        #response = requests.get(self.api_url, headers=headers)
        print(response.content)


    def storeState(self, level):
        logTime = str(datetime.now())
        with open(self.state_file, "w") as ofile:
            ofile.write(logTime)
            ofile.write(",")
            ofile.write(str(level))
            return
		
    def readLastState(self):
        try:
            logTime = str(datetime.now())
            with open(self.state_file, "rb") as ofile:
                lines = ofile.readlines()
                last_line = lines[-1]
                last_line = last_line.split(",")
                self.log("info",str(last_line))
                return last_line
        except Exception, e:
            return ['2016-10-06 17:49:14.670283,74',0]


    def log(self, type, message):
        logTime = str(datetime.now())
        if(type == "info"):
            with open(self.info_log, "a") as ofile:
                ofile.write(logTime+":"+message)
                ofile.write("\n")
                return
        if(type == "warning"):
            with open(self.warning_log, "a") as ofile:
                ofile.write(logTime+":"+message)
                ofile.write("\n")
                return
        if(type == "error"):
            with open(self.error_log, "a") as ofile:
                ofile.write(logTime+":"+message)
                ofile.write("\n")
                return
        if(type == "stat"):
            with open(self.stat_log, "a") as ofile:
                ofile.write(logTime+":"+message)
                ofile.write("\n")
                return
        if(type == "test"):
            with open(self.test_log, "a") as ofile:
                ofile.write(logTime+":"+message)
                ofile.write("\n")
                return
        else:
            print(logTime+":"+message)
            return


me= MansoobEngine()
me.main()