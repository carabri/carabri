"""
TODO: add readme/more info
Produces two log files in current directory:
-results.txt currently shows startup time after reboot
-log.txt currently shows logcat stream of ActivityManager
"""

import subprocess
import os
import time
import json

with open('./config.json') as f:
    config = json.load(f)


device = '-e' if config['emulator'] else '-d'

search_func_name = ''
if os.name == 'nt':
    search_func_name = 'findstr'
else:
    search_func_name = 'grep'

with open('results.txt','w+') as results:
    with open('log.txt','w+') as log:
        subprocess.call("adb %s shell stop" % (device))
        subprocess.call("adb %s shell start" % (device))
        start_time = time.time()
        time.sleep(.5)
        
        while b'running' in subprocess.check_output("adb %s shell getprop init.svc.bootanim" % (device)):
            pass
        startup_time = time.time() - start_time

        results.write("Startup time: " + str(startup_time) + " seconds")
        #clear the logcat
        subprocess.call("adb %s logcat -c" % (device))
        log_start = subprocess.Popen("adb %s logcat -s ActivityManager:I | %s Displayed" % (device,search_func_name), stdout = log, stderr=subprocess.STDOUT)
        
        subprocess.call("adb %s shell am start -n com.android.browser/.BrowserActivity" % (device))
        subprocess.call("adb %s shell am start -n com.android.dialer/.DialtactsActivity" % (device))
        subprocess.call("adb %s shell am start -n com.android.gallery/com.android.camera.GalleryPicker" % (device))
        
        log_start.terminate()