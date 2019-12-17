#!/usr/bin/python3

import argparse
import requests
import json
import smtplib
import sys
import time
import yaml

num_di_channels = 8
di_channels = {}
yaml_config = ''
HIGH = 1
LOW  = 0
email_from=""

def set_yaml_config(config_file='/usr/local/monitoring/monitoring.yaml'):
    cfg = ''
    try:
        with open(config_file, 'r') as fp:
            cfg = yaml.load(fp)
    except:
        print("Can't open yaml config file")
        sys.exit(1)
    return(cfg)

def alertmail(status,yaml):
    if status == 0:
        m = yaml['alert_low_message']
    else:
        m = yaml['alert_high_message']
    body = "Subject: Alert " + yaml['label'] + "\n\n Status: " + yaml['label'] + " " + m + '\n'
    for e in yaml['alert_recipients']:
        try:
            with smtplib.SMTP('localhost',25) as server:
                server.sendmail(email_from,e,body)
        except:
            print('Mail failed')



def alerttest(di,status,yaml):
    condition = False
    di_last_read = di_channels[di]
    if status != di_last_read['last_status']:
        if status == HIGH and yaml['alert_on_high'] or status == LOW and yaml['alert_on_low']:
            t = time.time()
            if yaml['alert_interval'] > 0:
                timestamp = di_channels[di]['alert_timestamp']
                if int(timestamp) + int(yaml['alert_interval']) < t:
                    condition = True
                else:
                    condition = False
            else:
                condition = True
        di_last_read['last_status'] = status
        if condition:
            di_last_read['alert_timestamp'] = int(time.time())
    
    return condition

def run(yaml):
    while True:
        error = False
        try:
            reply = requests.get("http://192.168.1.254/api/slot/0/io/di", headers={"Content-Type":"application/json","Accept":"vdn.dac.v1"})
        except:
            print("Connection error")
            time.sleep(5)
            error = True
        if not error:
            if reply.status_code == 200:
                json_blob = ''
                try:
                    json_blob = json.loads(reply.content.decode('utf-8'))
                    status = json_blob['io']['di']
                    for entry in status:
                        di = entry['diIndex']
                        if alerttest(di,entry['diStatus'],yaml[di]):
                            alertmail(entry['diStatus'],yaml[di])
                except ValueError:
                    print("Error processing json blob")
             
        time.sleep(2)

if __name__ == "__main__":
    yaml_config = set_yaml_config()
    for n in range(0,num_di_channels):
        di_channels[n] = {"alert_timestamp": 0, "last_status": yaml_config['di_channels'][n]['start_state']}
    run(yaml_config['di_channels'])

