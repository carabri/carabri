"""
helper class, representing an apk database on the file system
"""

import datetime
import json
import os
import re
import sys
from dateutil.parser import parse


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
                    sys.stdout.write("  - processing: " + app_info_file)
                    with open(app_info_file) as f:
                        app_info = json.load(f)
                    imported_apks = 0
                    for app_version in app_info:
                        imported_apks += self.insert_apk(app_version, dirpath)
                    sys.stdout.write(" (%d apk files loaded)\n" % imported_apks)

    def insert_apk(self, info, dirpath):
        if info['app_id'] not in self.apks:
            self.apks[info['app_id']] = {}
        app = self.apks.get(info['app_id'])
        if info['version'] in app:
            self.die("apks with the same version already exist! app_id: %s, version: %s" % (info['app_id'], info['version']))
        for variant in info['variants']:
            variant['upload_time'] = self.parse_upload_time(variant['upload_time'])  # can return with None
            variant['screen_size'] = self.parse_screen_size(variant['screen_size'])
            variant['min_api_level'] = self.parse_api_level(variant['android_version_min'])  # can return with None
            variant['file_path'] = os.path.join(dirpath, variant['file_name'])
        app[info['version']] = list(filter(lambda x: x['upload_time'] and x['min_api_level'], info['variants']))
        return len(app[info['version']])

    # example:
    # 'nodpi'       -> ['nodpi']
    # '160dpi'      -> ['160dpi']
    # '213, 240dpi' -> ['213dpi', '240dpi']
    @staticmethod
    def parse_screen_size(screen_size):
        tokens = map(lambda x: x.strip(), screen_size.split(','))
        return map(lambda x: x if x.endswith('dpi') else x + 'dpi', tokens)

    # example:
    # 'Android 4.0 (Ice Cream Sandwich, API 14)'       -> 14
    # 'Android 6.0 (Marshmallow, API 23)'            -> 23
    @staticmethod
    def parse_api_level(android_version):
        m = re.search('(?<=API )\d+', android_version)
        if m:
            return int(m.group(0))
        return None  # not able to parse android version, the given apk will be skipped

    # standard iso format, like: 'April 28, 2016 at 1:47AM GMT+0200'
    @staticmethod
    def parse_upload_time(upload_time):
        try:
            return parse(upload_time)
        except ValueError:
            return None  # exception while converting date, the given apk will be skipped

    def get_sorted_apk_list(self, filter_app_ids, filter_uploaded_after=datetime.MINYEAR, filter_uploaded_before=datetime.MAXYEAR,
                            filter_architectures=['any'], filter_api_level=21, filter_screen_size=['nodpi']):

        selected_apks = []
        if 'any' not in filter_architectures: filter_architectures.append('any')
        if 'nodpi' not in filter_screen_size: filter_screen_size.append('nodpi')

        for app_id, app_versions in self.apks.items():
            if app_id in filter_app_ids:
                for app_version, app_variants in app_versions.items():
                    selected_variant = self.select_variant(app_variants, filter_uploaded_after, filter_uploaded_before, filter_architectures, filter_api_level, filter_screen_size)
                    if selected_variant:
                        selected_apks.append(selected_variant)
        return sorted(selected_apks, key=lambda x: x['upload_time']);

    @staticmethod
    def select_variant(app_variants, filter_uploaded_after, filter_uploaded_before, filter_architectures, filter_api_level, filter_screen_size):
        filtered_variants = list(filter(lambda x: filter_uploaded_after <= x['upload_time'] <= filter_uploaded_before and
                                                  any(arch in filter_architectures for arch in x['architectures']) and
                                                  any(screen in filter_screen_size for screen in x['screen_size']) and
                                                  filter_api_level >= x['min_api_level']
                                        , app_variants))
        if filtered_variants:
            return filtered_variants[0]
        else:
            return None

    @staticmethod
    def die(error_message):
        sys.stdout.write(error_message)
        sys.exit(1)
