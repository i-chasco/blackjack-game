import random

'''Single player blackjack game. Dealer always hits until (s)he has at least 17 points'''


# Define the pieces of the deck

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
          'Queen':10, 'King':10, 'Ace':11}
playing = True


# Define class card

class Card:
    ''' 2 atributes: suit and rank '''
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


    def __str__(self):
        return f"{self.rank} of {self.suit}"


# Define class deck

class Deck:
    '''Definition: List of cards. Has 3 functions: shuffle, deal and string'''
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append((rank, suit))

    def __str__(self):
        return str(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        card = self.deck[0]
        self.deck.pop(0)
        return card


# Define class Hand

class Hand:
    '''
    3 atributes: List of cards, value, number of aces.
    2 functions: add_card and adjust_for ace
    '''
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self,card):
        self.cards.append((card.rank, card.suit))
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        """
        Normally counts ace value as 11
        If value of hand > 21, counts Ace value as 1 (= self.value -= 10)
        Maximum times it can do -10 = number of aces present
        """
        aces_adjusted = 0
        while aces_adjusted < self.aces:
            if self.value > 21:
                self.value -= 10
                aces_adjusted += 1
            else:
                break


# Define class Chips

class Chips:
    '''
    3 atributes: total, chips bet and chips remainig
    2 functions: win_bet and lose_bet
    '''
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        self.remaining = 100

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# Define function ask player to take a bet

def take_bet(chips):
    """
    Ask for a number to bet. Keep asking if value is not number or if value bigger
    than the total amount of chips
    """
    while True:
        try:
            intended_bet = int(input("Please enter your bet: "))
            if intended_bet <= chips.total:
                chips.bet = intended_bet
                chips.remaining = chips.total - chips.bet
                print(f"You bet {chips.bet} chips. You have {chips.remaining} left at your stack")
                break
            else:
                print("You are trying to bet more money than you have: Please introduce your bet again")
        except:
            print("Please introduce a number: ")


# Define a function for hitting (drawing from) the deck

def hit(deck,hand):
    ''' Shuflle "deck", draw a card (and erase it from "deck") and add it to "hand" '''
    deck.shuffle()
    new_card = deck.deal()
    hand.add_card(Card(new_card[0], new_card[1]))


# Define a function to prompt player to hit or stand and execute code in consequence

def hit_or_stand(deck,hand):
    '''Prompt player if he wants to hit or stand. If "hit", execute hit(player, hand)
    If stand, set playing to false and exit loop'''
    global playing  # to control an upcoming while loop
    while True:
        try:
            decision = input("Do you want to hit or stand? (H/S)")
            if decision.lower() == "h":
                hit(deck, player_hand)
                break
            elif decision.lower() == "s":
                print("Player stands, now it's the turn of the dealer")
                playing = False
                break
        except:
            print("Please introduce a valid answer!")


# Define functions to display cards and calculate the value

def show_some(player_hand,dealer_hand):
    ''' Shows all cards and hand value for player, all cards excluding one and
    no value for dealer '''
    print("\n" * 2)
    print("Your cards are: ")
    print(player_hand.cards)
    print("Your hand value is: ")
    print(player_hand.value)
    print("The dealer's cards are (one is hidden): ")
    print(dealer_hand.cards[1:])

def show_all(player_hand,dealer_hand):
    '''Show all cards and hand value for both player and dealer '''
    print("\n" * 2)
    print("Your cards are: ")
    print(player_hand.cards)
    print("Your hand value is: ")
    print(player_hand.value)
    print("The dealer's cards are: ")
    print(dealer_hand.cards)
    print("The dealer's hand's value is: ")
    print(dealer_hand.value)


# Define end of game scenarios

def player_busts(hand):
    return True if hand.value > 21 else False

def player_wins(player_hand, dealer_hand):
    return True if player_hand.value > dealer_hand.value else False

def dealer_busts(hand):
    return True if hand.value > 21 else False

def dealer_wins(player_hand, dealer_hand):
    return True if dealer_hand.value > player_hand.value else False

def tie(player_hand, dealer_hand):
    return True if dealer_hand.value == player_hand.value else False


# Define function to prompt player to play again and act in consequence

def play_again():
    ''' Restart game if user imput == "y". Stop the program if answe == "n"'''
    while True:
        try:
            decision = input("Thank you for playing, do you want to play again?(Y/N): )")
            if decision.lower() == "y":
                print("Let's go for another round!")
                return True

            elif decision.lower() == "n":
                print("See you soon!")
                return False
            else:
                print("That is not a valid answer, please introduce Y or N")
        except:
            print("Please introduce a valid answer!")


### START THE GAME !

# Set up the Player's chips
player_chips = Chips()

while True:
    # Print an opening statement
    print(f"Welcome to the blackjack game, you have {player_chips.total} chips, and each player will be dealt 2 cards")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    hit(deck, player_hand)
    hit(deck, dealer_hand)
    hit(deck, player_hand)
    hit(deck, dealer_hand)

    # Prompt the Player for their bet
    take_bet(player_chips)

    # Show cards (but keep one dealer card hidden)
    # show_some(player_hand, dealer_hand)

    playing = True

    while playing:  # recall this variable from our hit_or_stand function

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)
        player_hand.adjust_for_ace()

        # If player's hand exceeds 21, run player_busts() and break out of loop

        if player_busts(player_hand):
            playing = False


    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if not player_busts(player_hand):
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
            dealer_hand.adjust_for_ace()

    # Show all cards
    show_all(player_hand, dealer_hand)

    # Run different winning scenarios
    if player_busts(player_hand):
        print(f"You busted!! You lost {player_chips.bet} chips")
        player_chips.total = player_chips.remaining
    elif dealer_busts(dealer_hand):
        print(f"The dealer busted, you win!! You won {player_chips.bet * 1.5} chips")
        player_chips.total = player_chips.remaining + (1.5 * player_chips.bet)
    elif player_wins(player_hand, dealer_hand):
        print(f"You win!! You won {player_chips.bet * 1.5} chips")
        player_chips.total = player_chips.remaining + (1.5 * player_chips.bet)
    elif dealer_wins(player_hand, dealer_hand):
        print(f"The dealer wins!! You lost {player_chips.bet} chips")
        player_chips.total = player_chips.remaining
    elif tie(player_hand, dealer_hand):
        print(f"There is a tie!! You recover the {player_chips.bet} chips you bet")
        player_chips.total = player_chips.remaining + player_chips.bet

    # Inform Player of their chips total
    print(f"Nice game! You have a total of {player_chips.total} chips left")

    # Ask to play again
    if play_again():
          continue
    else:
          break
