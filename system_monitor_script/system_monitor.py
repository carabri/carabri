#!/usr/bin/env python3

import subprocess
import json
import time
from datetime import datetime

with open('./config.json') as f:
    config = json.load(f)

device = '-e' if config['emulator'] else '-d'
sampling_interval = config['sample_interval']
while True:
    with open('./disk.log', 'a') as logfile:
        logfile.write('SAMPLE_TIME: ' + str(datetime.now()) + '\n\n\n')
        log = subprocess.call(['adb', 'shell', 'dumpsys', 'diskstats'], stdout=logfile)

    with open('./cpu.log', 'a') as logfile:
        logfile.write('SAMPLE_TIME: ' + str(datetime.now()) + '\n\n\n')
        log = subprocess.call(['adb', 'shell', 'dumpsys', 'cpuinfo'], stdout=logfile)

    with open('./memory.log', 'a') as logfile:
        logfile.write('SAMPLE_TIME: ' + str(datetime.now()) + '\n\n\n')
        log = subprocess.call(['adb', 'shell', 'dumpsys', 'meminfo'], stdout=logfile)

    with open('./data_dir.log', 'a') as logfile:
        logfile.write('SAMPLE_TIME: ' + str(datetime.now()) + '\n\n\n')
        log = subprocess.call(['adb', 'shell', 'du -h data/data'], stdout=logfile)

    time.sleep(sampling_interval)
