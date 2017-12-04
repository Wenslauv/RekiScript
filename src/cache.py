#!usr/bin/python

import os
import requests
import json

from src.enviroment import Enviroment, Standard


class Cache:
    loaded_sets : list  = []

    PATH    : str = "cache"
    URL     : str = "https://mtgjson.com/api/v5/{}.json"


    def __init__(self) -> None:
        path = Cache.PATH

        if os.path.exists(path):
            print("reading cache folder")
            for file in os.listdir(path):
                if file.endswith(".txt"):
                    file = file[:-4]
                    self.loaded_sets.append( file )
        else:
            print("make cache folder")
            os.makedirs(path)


    def update(self, enviroment:Enviroment) -> None:
        for standard in enviroment.standards:
            for set in standard.sets:
                if not set in self.loaded_sets:
                    self.__loadset(set)

    
    def get_set_path(self, set:str) -> str:
        return os.path.join(Cache.PATH, "{}.txt".format(set))


    def __loadset(self, set:str) -> None:
        url = Cache.URL.format(set.upper())
        response = requests.get(url)
        if response.status_code == 200:
            json_data = json.loads(response.content)
            if not "data" in json_data:
                raise ValueError("no 'data' in set json!")
            
            all_cards = json_data["data"]["cards"]

            set_path = self.get_set_path(set)
            lines = []
            for card in all_cards:
                lines.append(card["name"])
            
            with open(set_path, "w+") as file:
                file.write('\n'.join(lines))
            
            self.loaded_sets.append(set)
            print("stored {}".format(set))

        else:
            print("request to {} ended with error {}".format(url, response.status_code))

