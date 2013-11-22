#!/usr/bin/env python

import argparse
import json

from cfg_tool import To_dict
from cfg_tool import Trans_key

conf = {}

def to_dict(data):
    with open(data) as f:
        return To_dict().out(f.read())

def find_primary(data):
    conf = to_dict(data)
    for k, v in conf.items():
        if isinstance(v, dict) and 'primary' in v:
            print v['primary']

def translator(data):
    find_primary(data)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cfg', type=str)
    args = parser.parse_args()

    translator(args.cfg)

if __name__ == '__main__':
    main()


