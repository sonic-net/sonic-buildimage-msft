#!/usr/bin/env python3

# Name: startup_tsa_tsb.py, version: 1.0
#
# Description: Module contains the definitions to the VOQ Startup TSA-TSB service

import subprocess
import sys, getopt
from threading import Timer
import os.path

def getPlatform():
    platform_key = "DEVICE_METADATA['localhost']['platform']"
    platform = (subprocess.check_output(['sonic-cfggen', '-d', '-v', platform_key.replace('"',"'")]).strip()).decode()
    return platform

def getNumAsics():
    platform = getPlatform()
    asic_config_file = '/usr/share/sonic/device/{}/asic.conf'.format(platform)
    file = open(asic_config_file, 'r')
    Lines = file.readlines()
    for line in Lines:
       field = line.split('=')[0].strip()
       if field == "NUM_ASIC":
         return line.split('=')[1].strip()
    return 0

def getTsbTimerInterval():
    platform = getPlatform()
    conf_file = '/usr/share/sonic/device/{}/startup-tsa-tsb.conf'.format(platform)
    file = open(conf_file, 'r')
    Lines = file.readlines()
    for line in Lines:
       field = line.split('=')[0].strip()
       if field == "STARTUP_TSB_TIMER":
         return line.split('=')[1].strip()
    return 0

def getSonicConfig(ns, config_name):
    return subprocess.check_output(['sonic-cfggen', '-d', '-v', config_name.replace('"', "'"), '-n', ns.replace('"', "'")]).strip()

def getSubRole(asic_ns):
    sub_role_config = "DEVICE_METADATA['localhost']['sub_role']"
    sub_role = (getSonicConfig(asic_ns, sub_role_config)).decode()
    return sub_role

def getTsaConfig(asic_ns):
    tsa_config = 'BGP_DEVICE_GLOBAL.STATE.tsa_enabled'
    tsa_ena = (getSonicConfig(asic_ns, tsa_config)).decode()
    print('{}: {} - CONFIG_DB.{} : {}'.format(__file__, asic_ns, tsa_config, tsa_ena))
    return tsa_ena

def get_tsa_status():
    asic_num = getNumAsics()
    counter = 0
    for asic_id in range(int(asic_num)):
       asic_ns = 'asic{}'.format(asic_id)
       sub_role = getSubRole(asic_ns)
       if sub_role == 'FrontEnd':
          tsa_enabled = getTsaConfig(asic_ns)
          if tsa_enabled == 'false':
             counter += 1
    if counter == int(asic_num):
       return True;
    else:
       return False;

def config_tsa():
    tsa_ena = get_tsa_status()
    if tsa_ena == True:
       print("{}: Configuring TSA".format(__file__))
       subprocess.check_output(['TSA']).strip()
    else:
        print("{}: Either TSA is already configured or switch sub_role is not Frontend - not configuring TSA".format(__file__))
    return tsa_ena

def config_tsb():
    print("startup_tsa_tsb: Configuring TSB")
    subprocess.check_output(['TSB']).strip()
    tsb_issued = True
    return

def start_tsb_timer(interval):
    global timer
    print("{}: Starting timer with interval {} seconds to configure TSB".format(__file__, interval))
    timer = Timer(int(interval), config_tsb)
    timer.start()
    timer.join()
    return

def print_usage():
    print ("Usage: startup_tsa_tsb.py [options] command")
    print ("options:")
    print("  -h | --help       : this help message")
    print("command:")
    print("start     : start the TSA/TSB")
    print("stop      : stop the TSA/TSB")
    return

def start_tsa_tsb(timer):

    #Configure TSA if it was not configured already in CONFIG_DB
    tsa_enabled = config_tsa()
    if tsa_enabled == True:
      #Start the timer to configure TSB
      start_tsb_timer(timer)
    return

def stop_tsa_tsb():
    #for future use
    return

def main():
    platform = getPlatform()
    conf_file = '/usr/share/sonic/device/{}/startup-tsa-tsb.conf'.format(platform)
    #This check should be moved to service file or make this feature as configurable.
    #Adding it here for now.
    if not os.path.exists(conf_file):
       print ("{} does not exist, exiting the service".format(conf_file))
       return
    if len(sys.argv) <= 1:
       print_usage()
       return

    # parse command line options:
    try:
       opts, args = getopt.getopt(sys.argv[1:], 'h:', ['help' ])
    except getopt.GetoptError:
       print_usage()
       return

    for opt, arg in opts:
       if opt in ("-h", "--help"):
          print_usage()
          return

    for arg in args:
        if arg == 'start':
           tsb_timer = getTsbTimerInterval()
           start_tsa_tsb(tsb_timer)
        elif arg == 'stop':
           stop_tsa_tsb()
        else:
           print_usage()
           return

    return

if __name__ == "__main__":
    main()
