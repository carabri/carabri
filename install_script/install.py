#!/usr/bin/env python3

import os
import json

with open('./config.json') as f:
    config = json.load(f)

apks = config['apks']
device = '-e' if config['emulator'] else '-d'
uninstall_list = config['uninstall']

for app in uninstall_list:
    print('uninstalling %s' % app)
    os.system('adb %s uninstall "%s"' % (device, app))

for apk in apks:
    os.system('adb %s install -r "%s"' % (device, apk))
    # TODO run tests