#!usr/bin/python

import urllib
import json
import os


def check_cache_dir(cache_path):
    print "Checking cache..."
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
        print "Cache created"
    else:
        print "OK"


def get_set_json(abbr):
    url = "https://mtgjson.com/json/{}.json".format(abbr)
    response = urllib.urlopen(url)
    if response.code != 404:
        json_data = json.loads(response.read().decode("UTF-8"))
        return json_data
    else:
        print "Unable to load set", abbr
        return ""


def get_cache_content(cache_path):
    cached_sets = []
    for file in os.listdir(cache_path):
        if file.endswith(".txt"):
            file = file[:-4]
            cached_sets.append(file)
    return cached_sets


def process_set_json(path, raw_json):
    if raw_json.__len__() == 0:
        return
    abbr = raw_json["code"]
    if abbr == "CON":
        abbr = "CFX"
    set_path = os.path.join(path, "{0}.txt".format(abbr))
    lines = []
    for card in raw_json["cards"]:
        lines.append(card["name"].encode("UTF-8"))
    with open(set_path, "w+") as file:
        file.write('\n'.join(lines))
    print "OK"


def create_cache(cache_path, sets):
    check_cache_dir(cache_path)
    loaded_sets = get_cache_content(cache_path)
    for set in sets:
        if not set.isupper():
            set = set.upper()
        if not set in loaded_sets:
            print "Downloading", set
            process_set_json(cache_path,  get_set_json(set))
        else:
            print "Skipping", set


def read_from_cache(cache_path, abbr):
    set_path = "{0}/{1}.txt"
    reading_abbr = abbr if abbr != "CON" else "CFX"
    file_path = set_path.format(cache_path, reading_abbr)
    if not os.path.exists(file_path):
        print "Unable to locate file", file_path
        return
    with open(file_path) as file:
        return file.readlines()