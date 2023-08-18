import random
import time

class Card:
    def __init__(self, suit, value, card_value):
        self.suit = suit
        self.value = value
        self.card_value = card_value

    def __str__(self):
        return f"{self.value} {self.suit}"


class Deck():
    def __init__(self):
         self.cards=[]
         self.build()

    def build(self):
        suits = ['♥', '♦', '♣', '♠']
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
    def __init__(self , name):
        self.busted = False
        self.stand = False
        self.hand = []
        self.name = name
        self.score = 0

    def card_count(self) -> int:
        return len(self.hand)


class Game:
    def __init__(self):
        self.player = Player("Player")
        self.dealer = Dealer()
        self.deck = Deck()
        self.dealer.shuffle(self.deck)

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
        if self.player.card_count() == 2:
            if self.player.hand[0].card_value == 11 and self.player.hand[1].card_value == 11:
                self.player.hand[0].card_value = 1
                self.player.score -=10


    def hit(self):
        card = self.dealer.deal(self.deck)
        self.player.hand.append(card)
        self.player.score += card.card_value
        if self.player.score > 21:
            self.player.busted = True

    def dealer_hit(self):
        card = self.dealer.deal(self.deck)
        self.dealer.hand.append(card)
        self.dealer.score += card.card_value
        if self.dealer.score > 21:
            self.dealer.busted = True

while True:
    game = Game()
    print("\033c", end="")
    game.deal_cards()

    while game.player.busted == False:

        print(f"Dealer: ?", game.dealer.hand[1])
        print(f"{game.player.name}:",*game.player.hand , f"Score: {game.player.score}")
        ans = input("stand or hit or quit? ")
        if ans == 'hit':
            game.hit()
        elif ans =='stand':
            game.player.stand = True
            break
        else:
            quit()

    print("\033c", end="")
    while game.dealer.busted == False:
        print(f"Dealer:",*game.dealer.hand, f"Score: {game.dealer.score}")
        print(f"{game.player.name}:",*game.player.hand , f"Score: {game.player.score}")
        time.sleep(1)
        print("Thinking: ")
        time.sleep(2)
        if game.player.busted:
            print("Standing")
            break
        elif game.dealer.score < 17:
            print("Hit")
            game.dealer_hit()
        elif game.dealer.score >= 17:
            game.dealer.stand = True
            print("Standing")
            break


    print("\033c", end="")
    if game.player.busted == True:
        print(f"Dealer wins!")
        print(f"Dealer:",*game.dealer.hand, f"Score: {game.dealer.score}")
        print(f"{game.player.name}:",*game.player.hand , f"Score: {game.player.score}")
    elif game.dealer.score > game.player.score and game.dealer.busted == False:
        print("Dealer wins!")
        print(f"Dealer:",*game.dealer.hand, f"Score: {game.dealer.score}")
        print(f"{game.player.name}:",*game.player.hand, f"Score: {game.player.score}")
    elif game.player.score == 21 or game.player.score > game.dealer.score or game.dealer.busted == True:
        print(f"{game.player.name} wins!")
        print(f"Dealer:",*game.dealer.hand, f"Score: {game.dealer.score}")
        print(f"{game.player.name}:",*game.player.hand , f"Score: {game.player.score}")
    
    time.sleep(5)