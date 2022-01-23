import random


kolory = ("Serce","Pik","Karo","Trefl")

ranks=("2","3","4","5","6","7","8","9","10","Jop","Dama","Król","As")

values={"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"Jopek":10,"Dama":10,"Król":10,"As":11,}


play = True

class Card():

    def __init__(self,kolor,ranks):
        self.kolor=kolor
        self.ranks=ranks

    def __str__(self):
        return self.ranks +" "+ self.kolor


class Deck:
    def __init__(self):
        self.deck = []  # start with an empty list
        for kolor in kolory:
            for rank in ranks:
                self.deck.append(Card(kolor,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp = deck_comp + '\n' + card.__str__()
        return "The deck has: " +deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card

##### Co mam na ręku ####
class Hand:

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0  # start with zero value
        self.aces = 0  # add an attribute to keep track of aces

    def add_card(self, card):
        pass

    def adjust_for_ace(self):
        pass


### Żetony ###
class Chips:
    def __init__(self):
        self.total= 100
        self.bet=0

    def win_bet(self):
        self.total=self.total+self.bet
        pass

    def lose_bet(self):
        self.total = self.total-self.bet
        pass


