#!/usr/bin/env python

import re
import json


class To_dict(object):

    def __init__(self):
        self.__conf = {}
        self.__temp = {}

    def __gen_lines(self, data):
        for line in data.split('\n'):
            yield line

    def __key_val(self, line):
        return line.replace(' = ', ' ').split()

    def __terrain(self, line):
        pass

    def __variables(self, line):
        key, val = self.__key_val(line)
        self.__conf[key] = val

    def out(self, data):
        var = re.compile('^\w+ = [\w\d\.]+')
        dic = re.compile('^\w+$')
        beg_brace = re.compile('^{$')
        brace_data = re.compile('^\t\w+ = [\w\d]+')
        end_brace = re.compile('^}$')
        terr = re.compile('^TERRAIN')
        for line in iter(self.__gen_lines(data)):
            if not self.__temp:
                if terr.match(line):
                    self.__terrain(line)
                elif var.match(line):
                    self.__variables(line)
                elif dic.match(line):
                    self.__temp[line.strip('\n')] = {}
            else:
                try:
                    if beg_brace.match(line):
                        pass
                    elif brace_data.match(line):
                        key, val = self.__key_val(line)
                        self.__temp[self.__temp.keys()[0]][key] = val
                    elif end_brace.match(line):
                        self.__conf[self.__temp.keys()[0]] = self.__temp[self.__temp.keys()[0]]
                        self.__temp.clear()
                except:
                    pass
        return self.__conf

from string import maketrans

class Trans_key(object):

    def __init__(self):
#        self.user_top = ''
#        self.user_mid = ''
#        self.user_bott = ''
        self.q_top = 'qwertyuiop[]'
        self.q_mid = "asdfghjkl;'"
        self.q_bott = 'zxcvbnm,./'
        self.trans_q_top = 'qwertyuiop89'
        self.trans_q_mid = "asdfghjkl71"
        self.trans_q_bott = 'zxcvbnm234'
        self.user_top = ''
        self.user_mid = ''
        self.user_bott = ''

    def invert_dict(self, d):
        return {v:k for k, v in d.items()}

    def rep_spec(self, char):
        spec_chars = {
                        '\\': '0',
                        "'": '1',
                        ',': '2',
                        '.': '3',
                        '/': '4',
                        '=': '5',
                        '-': '6',
                        ';': '7',
                        '[': '8',
                        ']': '9'}
        cfg_spec = {'LeftBracket': '[',
                    'RightBracket': ']',
                    'Period': '.',
                    'Comma': ',',
                    'Slash': '/',
                    'Equals': '=',
                    'Semicolon': ';',
                    'Minus': '-',
                    'Quote': "'",
                    'Backslash': '\\'}
        if char in spec_chars:
            return spec_chars[char]
        elif char in cfg_spec:
            return spec_chars[cfg_spec[char]]
        else:
            return char

    def get_keys(self):
        prompt = 'Type the {row} row: '
        for row in ['top', 'middle', 'bottom']:
            chars = ''.join([self.rep_spec(char) for char in raw_input(prompt.format(row=row))])
            if row == 'top':
                self.user_top = chars
            elif row == 'middle':
                self.user_mid = chars
            else:
                self.user_bott = chars

    def prep_cfg_spec(self, cfg):
        for k, v in cfg.items():
            if isinstance(v, dict) and 'primary' in v:
                cfg[k]['primary'] = self.rep_spec(cfg[k]['primary'])
        return cfg

    def translate(self, cfg):
        cfg = self.prep_cfg_spec(cfg)
        top_tab = maketrans(self.trans_q_top, self.user_top)
        mid_tab = maketrans(self.trans_q_mid, self.user_mid)
        bott_tab = maketrans(self.trans_q_bott, self.user_bott)
        for k, v in cfg.items():
            if isinstance(v, dict) and 'primary' in v:
                char = v['primary'].lower()
                if char in self.trans_q_top:
#                    print char, char.translate(top_tab).upper()
                    cfg[k]['primary'] = char.translate(top_tab).upper()
                elif char in self.trans_q_mid:
#                    print char, char.translate(mid_tab).upper()
                    cfg[k]['primary'] = char.translate(mid_tab).upper()
                elif char in self.trans_q_bott:
#                    print char, char.lower().translate(bott_tab).upper()
                    cfg[k]['primary'] = char.lower().translate(bott_tab).upper()
        return cfg

