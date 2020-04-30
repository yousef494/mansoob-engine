import time, subprocess, shlex
from time import gmtime, strftime
from datetime import datetime
from array import array
from Properties import Properties
#import sensor_reader
import most_common
import requests

class MansoobEngine():
    
    PROP_FILE = 'wtli.prop'

    def __init__(self):
        prop = Properties()
        prop.load(open(self.PROP_FILE))   
        self.api_url = 'http://localhost:2903/api/v1/reading/'
        self.state_file = 'data.wtli'

    def migrate_data(self):
        self.readLastState()

    def call_api(self, timestamp, data):
        json_data = {'timestamp': timestamp, 'level': data}
        headers = {'x-access-token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjM0MSwiaWF0IjoxNTg3MDU1NzI3LCJleHAiOjE1ODcxNDIxMjd9.12sGAZaZf8ymD__-SvoTUQOahWHO6WZi_-Gr8Ki3JIA'}
        response = requests.post(self.api_url, data = json_data, headers=headers)
        #response = requests.get(self.api_url, headers=headers)
        print(response.content)
		
    def readLastState(self):
        try:
            with open(self.state_file, "rb") as ofile:
                lines = ofile.readlines()
                for line in lines:
                    line = line.split(",")
                    self.call_api(line[0], int(line[1]))
                    time.sleep(1)
        except Exception, e:
            print(e)



me= MansoobEngine()
me.migrate_data()