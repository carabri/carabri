#!/usr/bin/env python3

import sys
sys.path.insert(0, '../common')

import json
import argparse
from apk_db import ApkDb

def main(args):
    with open(args.config) as f:
        config = json.load(f)

    apk_db = ApkDb(config['apk-database'])




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    input_ = parser.add_argument_group('input')
    input_.add_argument('--config', type=str, help="path to the config json file", default="./config.json")
    input_.add_argument('--log_dir', type=str, help="path to the log folder", default="./log/")

    arguments = parser.parse_args()
    main(arguments)