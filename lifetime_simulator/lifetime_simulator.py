#!/usr/bin/env python3

import sys

sys.path.insert(0, '../common')

import os
import json
import argparse
import time
import subprocess

from dateutil.parser import parse
from apk_db import ApkDb

import pytz


def main(config, log_dir):
    apk_db = ApkDb(config['apk-database'])
    apk_list = apk_db.get_sorted_apk_list(config['apks'],
                                          filter_uploaded_after=parse(config['after']).replace(tzinfo=pytz.UTC),
                                          filter_uploaded_before=parse(config['before']).replace(tzinfo=pytz.UTC),
                                          filter_architectures=[config['architecture']],
                                          filter_api_level=config['api-version'],
                                          filter_screen_size=['nodpi'])

    print("\n%d apk will be installed based on the specified filters" % len(apk_list))
    for apk in apk_list:
        install_app(apk, config['emulator'])
        for test in config['tests']:
            for sequence in range(0, test['repeat']):
                execute_test(apk, test['test-id'], test['command'], sequence, log_dir)


def install_app(app, emulator):
    device = '-e' if config['emulator'] else '-d'
    print("\n===\n%04d-%02d-%02d installing apk:  app_id=%s, version=%s, apk=%s" % (app['upload_time'].year, app['upload_time'].month, app['upload_time'].day, app['app_id'], app['version'],
                                                                                         app['file_path']))
    step_start_time = time.time()
    install_command = 'adb %s install -r "%s"' % (device, app['file_path'])
    status_code = subprocess.call(install_command, shell=True, cwd=".", env=os.environ.copy())
    if (status_code != 0): die("ERROR!\ninstallation failure (see error log above)\ninstall command: %s\nstatus code: %d\n" % (install_command, status_code))
    print("installation finished successfully (%.2f secs)\n===" % (time.time() - step_start_time))


def execute_test(app, test_id, command, sequence, log_dir):
    print("---  executing test: %s (repeat seq: %d)" % (test_id, sequence))
    step_start_time = time.time()
    env = os.environ.copy()
    env['TEST_ID'] = test_id
    env['RELEASE_DATE'] = str(app['upload_time'])
    env['SEQUENCE'] = str(sequence)
    env['LOG_DIR'] = log_dir
    env['APP_ID'] = app['app_id']
    env['APP_VERSION'] = app['version']
    status_code = subprocess.call(command, shell=True, cwd=".", env=env)
    if (status_code != 0): die("ERROR!\ntest execution failure.\nstatus code: %d\ntest id: %s\ntest sequence: %d\ntest command: %s" % (status_code, test_id, sequence, command))
    print("---  done (%.2f secs)" % (time.time() - step_start_time))


def validate_config(config_file):
    with open(config_file) as f:
        config = json.load(f)
    if 'emulator' not in config: die("missing mandatory field in config file: emulator")
    if 'apk-database' not in config: die("missing mandatory field in config file: apk-database")
    if 'api-version' not in config: die("missing mandatory field in config file: api-version")
    if 'apks' not in config: die("missing mandatory field in config file: apks")
    if 'tests' not in config: die("missing mandatory field in config file: tests")
    if 'architecture' not in config: config['after'] = "x86"
    if 'after' not in config: config['after'] = "2010-01-01"
    if 'before' not in config: config['before'] = "2099-12-31"
    if 'screen-size' not in config: config['screen-size'] = "nodpi"

    for test in config['tests']:
        if 'test-id' not in test: die("missing mandatory field in config file: test.test-id")
        if 'command' not in test: die("missing mandatory field in config file: test.command")
        if 'repeat' not in test: test['repeat'] = 1

    return config


def die(error_message):
    sys.stderr.write("\n" + error_message + "\n")
    sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    input_ = parser.add_argument_group('input')
    input_.add_argument('--config', type=str, help="path to the config json file", default="./config.json")
    input_.add_argument('--log_dir', type=str, help="path to the log folder", default="./log/")

    arguments = parser.parse_args()
    config = validate_config(arguments.config)
    main(config, arguments.log_dir)
