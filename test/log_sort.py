##
# cording:utf-8
##

import os
import json
import pprint as pp

json_list = []
with open("T0Z1JaqyUY0.log", 'r') as fp:
    for m in fp:
        obj = json.loads(m.replace('\n', ''))
        json_list.append(obj)

json_list.sort(key=lambda x: x['publishedAt'])        
pp.pprint(json_list)