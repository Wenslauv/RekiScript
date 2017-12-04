#!usr/bin/python


import os

from src.cardbase import CardBase
from src.enviroment import Enviroment


class Decklist:
    name    :   str     = ""

    main_cards  : dict  = {}
    side_cards  : dict  = {}

    def load(self, name:str, content:list) -> bool:
        self.name = name
        
        content = [x.strip('\n').lower() for x in content]

        side_started : bool = False
        for line in content:
            if not line:
                side_started = True
                continue

            values = line.partition(" ")
            if not values[2]:
                print("\tWrong line format:", line)
                return False

            count = int(values[0])
            name = values[2]

            if side_started:
                if name not in self.side_cards:
                    self.side_cards[ name ] = count
                else:
                    self.side_cards[ name ] += count
            
            else:
                if name not in self.main_cards:
                    self.main_cards[ name ] = count
                else:
                    self.main_cards[ name ] += count

        return True




class Decklists:
    decklists   :   list    = []

    PATH = "decklists"

    UNLIMITED_CARDS = ["plains", "island", "swamp", "mountain", "forest",  "relentless rats", "dragon's approach", "persistent petitioners", "rat colony", "relentless rats"]
    

    def __init__(self) -> None:
        self.decklists = []

        for raw_list in os.listdir(Decklists.PATH):
            path = "{}/{}".format( Decklists.PATH, raw_list)
            if not path.endswith(".txt"):
                continue

            with open(path, "r") as file:
                decklist = Decklist()
                if decklist.load( raw_list, file.readlines()):
                    self.decklists.append( decklist )
                else:
                    raise ValueError("Bad list {}".format(raw_list))


    def validate(self, env:Enviroment, base:CardBase) -> None:
        for decklist in self.decklists:
            is_card_counts_valid = self.validate_cards_in_list(decklist)
            if is_card_counts_valid:
                self.validate_card_legality(decklist, env, base)


    
    def validate_cards_in_list(self, decklist:Decklist) -> bool:
        print("Checking list {}".format(decklist.name))

        cards_in_main : int = 0
        cards_in_side : int = 0
        card_copies_total : dict = {}

        for card, count in decklist.main_cards.items():
            cards_in_main += count
            if card not in card_copies_total:
                card_copies_total[card] = count
            else:
                card_copies_total[card] += count
        
        for card, count in decklist.side_cards.items():
            cards_in_side += count
            if card not in card_copies_total:
                card_copies_total[card] = count
            else:
                card_copies_total[card] += count


        something_wrong : bool = False
        
        if cards_in_main < 60:
            print("\tNot legal: {} cards in main".format(cards_in_main))
            something_wrong = True

        if cards_in_side > 15:
            print("\tNot legal: {} cards in sideboard".format(cards_in_side))
            something_wrong = True

        for card, count in card_copies_total.items():
            if card in Decklists.UNLIMITED_CARDS:
                continue 

            if count > 4:
                print("\tNot legal: More than 4 copies ({}) of card {}".format(count, card))
                something_wrong = True

        return not something_wrong


    def validate_card_legality(self, decklist:Decklist, env:Enviroment, base:CardBase) -> None:
        list_is_legal = False

        suitable_formats : list = []

        for standard in env.standards:
            list_from_this_format = True
            
            for card, count in decklist.main_cards.items():
                if card in standard.banned:
                    list_from_this_format = False
                    break

                if not base.is_card_in_base(standard.sets, card):
                    list_from_this_format = False
                    break
            
            if list_from_this_format:
                suitable_formats.append( standard.name )
                
        if suitable_formats:
            print("\tLegal in formats:", join(suitable_formats, ","))
        else:
            print("\tNot legal: no standard found")
        
