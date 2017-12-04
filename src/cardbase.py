#!usr/bin/python

import os

from src.cache import Cache
from src.enviroment import Standard


class CardBase:
    cards   :   map = {}
    
    def __init__(self, cache:Cache) -> None:
        for set in cache.loaded_sets:
            set_path = cache.get_set_path(set)

            if not os.path.exists(set_path):
                raise ValueError("No {} file in cache", set)
            
            with open(set_path, "r") as file:
                content = file.readlines()
                content = [x.strip('\n').lower() for x in content]

                self.cards[ set ] = content
    

    def is_card_in_base(self, scope:list, card:str) -> bool:
        for set in scope:
            if card in self.cards[set]:
                return True
            
        return False