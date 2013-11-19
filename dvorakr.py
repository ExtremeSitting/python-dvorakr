#!/usr/bin/env python

import re
import argparse
import json
from string import maketrans
from copy import deepcopy
from collections import defaultdict


conf = {}
temp = {}
new_conf = {}

specials = {'LeftBracket': '[',
            'RightBracket': ']',
            'KeypadMinus': '-',
            'KeypadPlus': '+',
            'Period': '.',
            'Comma': ','}

trans_specials = {"'": '1', ',': '2', '.': '3', '\\': '4', '=': '5', '-': '6',
                    ';': '7', '[': '8', ']': '9'}

q_top = 'qwertyuiop[]'
q_mid = "asdfghjkl;'"
q_bott = 'zxcvbnm,./'

def invert_dict(d):
    '''Takes a dictionary as an argument. Makes the values keys and the keys
        their values.'''
    new_dict = defaultdict(list)
    for k, v in d.iteritems():
        new_dict[v].append(k)
    return dict(new_dict)

def get_keys():
    top = "',.pyfgcrl/="
    mid = 'aoeuidhtns-'
    bott = ';qjkxbmwvz'
    return top.upper(), mid.upper(), bott.upper()
#    top = raw_input('Top row: ').upper()
#    mid = raw_input('Middle row: ').upper()
#    bott = raw_input('Bottom row: ').upper()
#    return top, mid, bott

def make_transtable(user_keys, sys_keys):
    return maketrans(user_keys, sys_keys)

def trans_key(key):
    top, mid, bott = get_keys()
    top_tab = make_transtable(top, q_top.upper())
    mid_tab = make_transtable(mid, q_mid.upper())
    bott_tab = make_transtable(bott, q_bott.upper())
    if key in q_top.upper():
        return key.translate(top_tab)
    elif key in q_mid.upper():
        return key.translate(mid_tab)
    elif key in q_bott.upper():
        return key.translate(bott_tab)

def key_val(line):
    return line.replace(' = ', ' ').split()

def parse_line(line):
    reg = re.compile('^\w+ = [\w\d\.]+')
    dic = re.compile('^\w+$')
    bbrack = re.compile('^{$')
    brack_data = re.compile('^\t\w+ = [\w\d]+')
    ebrack = re.compile('^}$')
    terr = re.compile('TERRAIN')
    if not temp:
        if terr.match(line):
            pass
        if reg.match(line):
            key, val = key_val(line)
            if val in specials:
                val = specials[val]
            conf[key] = val
        elif dic.match(line):
            temp[line.strip('\n')] = {}
    else:
        if bbrack.match(line):
            pass
        elif brack_data.match(line):
            key, val = key_val(line)
            temp[temp.keys()[0]][key] = val
        elif ebrack.match(line):
            conf[temp.keys()[0]] = temp[temp.keys()[0]]
            temp.clear()
#            get_keys()

def get_data(cfg):
    with open(cfg, 'rU') as f:
        for line in f:
            try:
                parse_line(line)
            except:
                pass
    parse(conf)

def parse(data):
    new_conf = deepcopy(conf)
    for key in data:
        if isinstance(data[key], dict) and 'primary' in data[key]:
            if len(data[key]['primary']) == 1:
                trans = trans_key(data[key]['primary'])
                new_conf[key]['primary'] = trans
                print key, '\n', new_conf[key]
                print conf[key], '\n'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('cfg', type=str)
    args = parser.parse_args()

    get_data(args.cfg)

if __name__ == '__main__':
    main()
