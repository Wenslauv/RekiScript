#!usr/bin/python

import os
import sys

from tools.common import Enviroment
from tools.formats import read_formats
from tools.data import create_cache, check_cache_dir, read_from_cache

CONFIG_FILE_NAME = "config"
FORMATS_PATH = "formats/{0}.json"
CACHE_DIR = "cache"

IGNORED_CARDS = ['plains', 'island', 'swamp', 'mountain', 'forest', 'relentless rats']


class Config:
    predefine = None
    legal_sets = []
    banned_cards = []
    decklists_path = "decklists"

    def get_enviroment(self):
        env = Enviroment()
        env.sets = [x.upper() for x in self.legal_sets]
        env.banned = [x.lower() for x in self.banned_cards]
        return env



def build_card_base(sets):
    card_base = {}
    for set in sets:
        cardlist = read_from_cache(CACHE_DIR, set)
        cardlist = [x.lower() for x in cardlist]
        cardlist = [x.strip('\n') for x in cardlist]
        for card in cardlist:
            if card_base.has_key(card):
                if not set in card_base[card]:
                    card_base[card].append(set)
            else:
                card_base[card] = [set]
    return card_base


def check_decklists(decklist_path, card_base, legal_sets, banned):
    print "<<------------------------------------------------------>>"
    print "Decklists validation"
    for file in os.listdir(decklist_path):
        file_path = "{}/{}".format(decklist_path, file)
        if not file.endswith(".txt"):
            continue
        print file[:-4]
        with open(file_path, 'r') as f:
            if check_decklist(f.readlines(), card_base, legal_sets, banned):
                print "OK"


def check_decklist(content, card_base, legal_sets, banned):
    content = [x.strip('\n').lower() for x in content]
    intersection = legal_sets
    main_card_count = 0
    sideboard_card_count = 0
    add_to_sidebboard = False
    card_count_by_cards = {}
    isOK = True
    for i, value in enumerate(content):
        if value == "sideboard":
            add_to_sidebboard = True
        if not value[:1].isdigit():
            continue # ignore separators and empty lines
        count, name = value.split(" ", 1)
        if not name in card_base:
            print "Decklist error! Possibly, card", name.upper(), "writed incorrectly?"
            return False
        sets = card_base[name]
        intersection = set(sets).intersection(intersection)
        if intersection.__sizeof__() == 0:
            print "Decklist error! Unable to find common bounds for sets!"
            return False
        if add_to_sidebboard:
            sideboard_card_count += int(count)
        else:
            main_card_count += int(count)
        if name not in IGNORED_CARDS:
            if name in card_count_by_cards:
                card_count_by_cards[name] += int(count)
            else:
                card_count_by_cards[name] = int(count)
        if name in banned:
            print "Decklist error! Deck contains banned card", name.upper()
            isOK = False
    if main_card_count < 60:
        print "Decklist error! Deck has", main_card_count, "cards in main deck!"
        isOK = False
    if sideboard_card_count > 15:
        print "Decklist error! Deck has", sideboard_card_count, "cards in sideboard!"
        isOK = False
    for key, value in card_count_by_cards.iteritems():
        if value > 4:
            print "Decklist error! Deck contains", value, "copies of", key.upper()
            isOK = False
    return isOK



def read_config(config_path):
    config = Config()
    if os.path.exists(config_path):
        print "Reading configuration from", os.path.abspath(config_path)
        g = l = {}
        execfile(config_path, g, l)
        for name, value in g.iteritems():
            setattr(config, name, value)
    else:
        # fail only if no options were specified
        if len(sys.argv) < 2:
            print "Please create config file", os.path.abspath(CONFIG_FILE_NAME)
            sys.exit(1)
    return config


if __name__ == "__main__":
    config = read_config(CONFIG_FILE_NAME)
    enviroment = Enviroment()
    if config.predefine is not None:
        enviroment = read_formats(FORMATS_PATH.format(config.predefine))
    else:
        enviroment = config.get_enviroment()
    create_cache(CACHE_DIR, enviroment.sets)
    if not os.path.exists(config.decklists_path):
        print "Unable to find decklists folder", config.decklists_path
        print "Please, check path in config"
        sys.exit(1)
    card_base = build_card_base(enviroment.sets)
    check_decklists(config.decklists_path, card_base, enviroment.sets, enviroment.banned)
