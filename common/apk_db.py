"""
helper class, representing an apk database on the file system
"""

import os
import sys
import json


class ApkDb(object):
    def __init__(self, path_):
        self.path = path_
        self.load_from_fs()

    def load_from_fs(self):
        self.apks = {}
        print("initializing ApkDb from file system: " + self.path)
        for dirpath, dirnames, files in os.walk(self.path):
            for name in files:
                if name.lower().endswith(".json"):
                    app_info_file = os.path.join(dirpath, name)
                    print("  - processing: " + app_info_file)
                    with open(app_info_file) as f:
                        app_info = json.load(f)
                    for app_version in app_info:
                        self.insert_apk(app_version)
        #print(self.apks)

    def insert_apk(self, info):
        if info['app_id'] not in self.apks:
            self.apks[info['app_id']] = {}
        app = self.apks.get(info['app_id'])
        if info['version'] in app:
            sys.stderr.write("apks with the same version already exist! app_id: %s, version: %s" % (info['app_id'], info['version']))
            sys.exit(1)
        app[info['version']] = info['variants']

    @staticmethod
    def apk_key(app_id, app_version):
        return app_id+"_"+app_version