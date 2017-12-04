#!usr/bin/python

import os
import sys

from src.enviroment import Enviroment
from src.cache import Cache
from src.cardbase import CardBase
from src.decklist import Decklists



if __name__ == "__main__":
    enviroment = Enviroment()
    enviroment.load()
    
    cache = Cache()
    cache.update(enviroment)
    
    cardbase = CardBase(cache)

    decklists = Decklists()
    decklists.validate(enviroment, cardbase)


