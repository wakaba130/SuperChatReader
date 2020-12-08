##
# cording:utf-8
##

import os
import json
import pprint as pp

def loader(file):
    json_list = []
    with open(file, 'r') as fp:
        for _line in fp:
            json_dict = json.loads(_line.replace('\n', ''))
            json_list.append(json_dict)
    return json_list

if __name__ == "__main__":
    json_list = loader("log/zK5IGA4e7mc.log")
    for param in json_list:
        print("[by {}]\n {}\n".format(param['displayName'], param['displayMessage']))