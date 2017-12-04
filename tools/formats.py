#!usr/bin/python

import os
import json
from common import Enviroment


def read_formats(path_to_formats):
    env = Enviroment()
    if os.path.exists(path_to_formats):
        with open(path_to_formats, 'r') as file:
            data = json.loads(file.read())
            env.sets = [x.upper().encode('ascii')  for x in data["legal_sets"]]
            env.banned = [x.lower().encode('ascii')  for x in data["banned_cards"]]
    else:
        raise IOError()
    return env
