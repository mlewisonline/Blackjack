import random
import time
import os

# System call
os.system("")

# Class of different styles
class style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class Card:
    def __init__(self, suit, value, card_value):
        self.suit = suit
        self.value = value
        self.card_value = card_value

    def __str__(self):
        return f"{self.value} {self.suit}"


class Deck:
    def __init__(self):
         self.cards=[]
         self.build()

    def build(self):
        suits = ['\033[31m♥\033[37m', '\033[31m♦\033[37m', '\33[34m♣\033[37m', '\33[34m♠\033[37m']
        values = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        card_value = {"A": 11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit, value, card_value[value]))


class Dealer:
    def __init__(self):
        self.busted = False
        self.stand = False
        self.hand = []
        self.score = 0
    
    def deal(self, deck :Deck) -> Card:
        return deck.cards.pop()
    
    def shuffle(self , deck: Deck) -> None:
        for _ in range(len(deck.cards)):
            random.shuffle(deck.cards)
    
    def card_count(self) -> int:
        return len(self.hand)


class Player:
    def __init__(self):
        self.busted = False
        self.stand = False
        self.hand = []
        self.score = 0

    def card_count(self) -> int:
        return len(self.hand)


class Game:
    def __init__(self):
        self.player = Player()
        self.dealer = Dealer()
        self.deck = Deck()
        self.dealer.shuffle(self.deck)

    def print_title(self):
        print(f"""{style.YELLOW}
 ____  _            _        _            _    
|  _ \| |          | |      | |          | |   
| |_) | | __ _  ___| | __   | | __ _  ___| | __
|  _ <| |/ _` |/ __| |/ /   | |/ _` |/ __| |/ /
| |_) | | (_| | (__|   < |__| | (_| | (__|   < 
|____/|_|\__,_|\___|_|\_\____/ \__,_|\___|_|\_\
              
              By Matthew Lewis version 1.0\n{style.RESET}""")

    def clear_screen(self) -> None:
         # for windows
        if os.name == 'nt':
            _ = os.system('cls')
        # for mac and linux(here, os.name is 'posix')
        else:
            _ = os.system('clear')

    def check_two_aces(self, player):
        if isinstance(player, Player):
            if self.player.hand[0].card_value == 11 and self.player.hand[1].card_value == 11:
                self.player.hand[0].card_value = 1
                self.player.score -=10
        else:
            if self.dealer.hand[0].card_value == 11 and self.dealer.hand[1].card_value == 11:
                self.dealer.hand[0].card_value = 1
                self.dealer.score -=10

    def deal_cards(self):
        # Deal a card to the player and then the dealer
        self.player.hand.append(self.dealer.deal(self.deck))
        self.player.score += self.player.hand[0].card_value
        self.dealer.hand.append(self.dealer.deal(self.deck))
        self.dealer.score += self.dealer.hand[0].card_value
        # deal the second card to each player and then the dealer
        self.player.hand.append(self.dealer.deal(self.deck))
        self.player.score += self.player.hand[1].card_value
        self.dealer.hand.append(self.dealer.deal(self.deck))
        self.dealer.score += self.dealer.hand[1].card_value
        

        # If player dealt two aces lower the vale of one card to one
        self.check_two_aces(self.player)
        self.check_two_aces(self.dealer)




    def hit(self, player):
        card = self.dealer.deal(self.deck)
        if isinstance(player, Player):
            self.player.hand.append(card)
            self.player.score += card.card_value
            if self.player.score > 21:
                self.player.busted = True
        else:
            card = self.dealer.deal(self.deck)
            self.dealer.hand.append(card)
            self.dealer.score += card.card_value
            if self.dealer.score > 21:
                self.dealer.busted = True


def main():
    while True:  

        game = Game()
        game.deal_cards()

        while game.player.busted == False:
            game.clear_screen()
            game.print_title()
            print(f"Dealer: ?", game.dealer.hand[1])
            print(f"Player:",*game.player.hand , f"Score: {game.player.score}")

            ans = input("Hit, Stand or Quit? ")
            if ans == "hit" or ans == 'h':
                game.hit(game.player)
            elif ans == "stand" or ans == 's':
                game.player.stand = True
                break
            elif ans == "quit" or ans == 'q':
                quit()

        
        while game.dealer.busted == False:
            game.clear_screen()
            game.print_title()
            print(f"Dealer:",*game.dealer.hand, f"Score: {game.dealer.score}")
            print(f"Player:",*game.player.hand , f"Score: {game.player.score}")
            time.sleep(1)

            if game.player.busted:
                print("Standing")
                time.sleep(2)
                break
            elif game.dealer.score < 17:
                print("Hit")
                time.sleep(2)
                game.hit(game.dealer)
            elif game.dealer.score >= 17:
                game.dealer.stand = True
                print("Standing")
                time.sleep(2)
                break


        game.clear_screen()
        game.print_title()
        if game.player.busted == True:
            print(f"🏆 Dealer wins 🏆")
            print(f"Dealer:",*game.dealer.hand, f"Score: {game.dealer.score}")
            print(f"Player:",*game.player.hand , f"Score: {game.player.score}")
        elif game.dealer.score > game.player.score and game.dealer.busted == False:
            print("🏆 Dealer wins 🏆")
            print(f"Dealer:",*game.dealer.hand, f"Score: {game.dealer.score}")
            print(f"Player:",*game.player.hand, f"Score: {game.player.score}")
        elif game.player.score == 21 or game.player.score > game.dealer.score or game.dealer.busted == True:
            print("🏆 Player wins 🏆")
            print(f"Dealer:",*game.dealer.hand, f"Score: {game.dealer.score}")
            print(f"Player:",*game.player.hand , f"Score: {game.player.score}")
        else:
            print("🏆 Draw 🏆")
            print(f"Dealer:",*game.dealer.hand, f"Score: {game.dealer.score}")
            print(f"Player:",*game.player.hand , f"Score: {game.player.score}")
        
        input("\nPress any key to continue")

if __name__ == "__main__":
    main()