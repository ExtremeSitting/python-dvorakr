#!/usr/bin/env python

from cfg_tool import To_dict
from cfg_tool import Trans_key
import json


to_dict = To_dict()
trans_key = Trans_key()
with open('settings.cfg') as f:
    conf = to_dict.out(f.read())

trans_key.get_keys()

#print json.dumps(trans_key.translate(conf), indent=4)
trans_key.translate(conf)
