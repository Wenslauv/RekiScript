#!usr/bin/python

import os
import json


class Standard:
    name    : str   = ""
    sets    : list  = []
    banned  : list  = []

    def __init__(self, json:json) -> None:
        if "name" in json:
            self.name = json["name"]
        else:
            raise ValueError("Standard should contain a name!")
        
        if "sets" in json:
            self.sets = json["sets"]
        else:
            raise ValueError("Standard should contain available sets!")

        if "banned" in json:
            self.banned = json["banned"]


class CardNotes:
    basics      : list  =   []
    unlimited   : list  =   []
    limited     : dict  =   {}

    SOURCE_PATH : str   = "data/notes.json"


    def load(self) -> None:
        self.basics     = []
        self.unlimited  = []
        self.limited    = {}

        if os.path.exists(CardNotes.SOURCE_PATH):
            print("Read card notes from ", os.path.abspath(CardNotes.SOURCE_PATH))

            data = json.load(open(CardNotes.SOURCE_PATH))
            self.basics     = data.get("basic lands", [])
            self.unlimited  = data.get("unlimited cards", [])
            self.limited    = data.get("limited cards", {})
        else:
            print("no 'card notes' file")




class Enviroment:
    standards : list = []

    SOURCE_PATH : str = "data/standards.json"


    def load(self) -> None:
        self.standards = []
        if os.path.exists(Enviroment.SOURCE_PATH):
            print("Read list of available standards from", 
                  os.path.abspath(Enviroment.SOURCE_PATH))
            
            f = open(Enviroment.SOURCE_PATH)
            data = json.load(f)
            for i in data['standards']:
                standard = Standard(i)
                print("track '{}'".format(standard.name))
                self.standards.append( standard )    
        else:
            print("no 'standards' file")

