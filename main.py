import requests
import time
from card_deck import Deck, Given_Card


player1_wins = 0
player2_wins = 0
turn = 1



#---------------------------------------------------------------------------------------
# This function creates the deck from the API, then distributes the cards based on how 
# many rounds they have won so far
# Once it is done, it moves on to start the game with play_game
def game_prep(player1_wins, player2_wins, turn):
    player1_hand = []
    player2_hand =[]
    new_deck = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"

    deck_info = requests.get(new_deck).json()
    

    deck_numbers = Deck(**deck_info)
    #-----
    #Check if a player has one
    
    
    #------------
    # none have won so player 1's cards are distributed
    if (player1_wins > 0):
        
        for i in range(10-player1_wins):
            new_card = f"https://deckofcardsapi.com/api/deck/{deck_numbers.deck_id}/draw/?count=1"

            card_info = requests.get(new_card).json()
            given_card = Given_Card(**card_info)
            
            next_card = {
                "Suit" : given_card.cards[0].suit,
                "Value" : given_card.cards[0].value, 
                "Spot" : "False"
                } 
            player1_hand.append(next_card)

    elif player1_wins == 0:
        for i in range(10):
                new_card = f"https://deckofcardsapi.com/api/deck/{deck_numbers.deck_id}/draw/?count=1"

                card_info = requests.get(new_card).json()
                given_card = Given_Card(**card_info)

                next_card = {
                    "Suit": given_card.cards[0].suit,
                    "Value": given_card.cards[0].value,
                    "Spot" : "False"
                }
                
                player1_hand.append(next_card)

    #----------------------
    # Next, player 2's cards are distributed
    if (player2_wins > 0):
        
        for i in range(10-player2_wins):
            new_card = f"https://deckofcardsapi.com/api/deck/{deck_numbers.deck_id}/draw/?count=1"

            card_info = requests.get(new_card).json()
            given_card = Given_Card(**card_info)

            next_card = {
                "Suit" : given_card.cards[0].suit,
                "Value" : given_card.cards[0].value, 
                "Spot" : "False"
                } 
            player2_hand.append(next_card)

    elif player2_wins == 0:
        for i in range(10):
            new_card = f"https://deckofcardsapi.com/api/deck/{deck_numbers.deck_id}/draw/?count=1"

            card_info = requests.get(new_card).json()
            given_card = Given_Card(**card_info)

            next_card = {
                "Suit": given_card.cards[0].suit,
                "Value": given_card.cards[0].value,
                "Spot" : "False"
            }
                
            player2_hand.append(next_card)
    #--------------
    # All cards have been dealt out and now time to start the actual game
    print("Hand has been dealt")
    play_game(player1_hand, player2_hand, player1_wins, player2_wins, deck_numbers.deck_id, turn)




#------------------------------------
#where the game is played:
# if it is a new turn it will get a card from draw_a_card
# but if it is a found card from the player's unknown hand, 
# it will use that card to keep playing their turn

def play_game(player1_hand, player2_hand, player1_wins, player2_wins,  deck_id, turn):
    
    #check if a player has won, or determine how many each player gets in their hand
    check_win(player1_hand, player2_hand,  player1_wins, player2_wins)

    #start the game by drawing a card from the API deck
    draw_a_card(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn)
        

#-------------------------
# This function is to see if a player has won the game or round
# if one player has won 10 times, then they have won the whole game and the code ends/closes
# but if a player has only won a round, the hands will be reset but the previous winner 
# has one less card to find
def check_win(player1_hand, player2_hand,  player1_wins, player2_wins):

    #restart values to make sure no incorrect values
    card1_count = 0
    card2_count = 0
    player1_count = 0
    player2_count = 0

    #if player one has won 10 rounds/ won the game, then tells so and closes the game
    if player1_wins == 10:
        print("Player One has won the whole game!")
         
        print("Closing Game")
        time.sleep(5)
        exit()
        
    #if player one has won 10 rounds/ won the game, then tells so and closes the game
    elif player2_wins == 10:
        print("Player Two has won the whole game!")
         
        
        print("Closing Game")
        time.sleep(5)
        exit()
    
    # if neither has won the game
    
    for card in player1_hand: # for each card in the hand
        card1_count += 1 # count the cards
        if player1_hand[card1_count-1]["Spot"] == "True": #count how many of those spot's are true
            player1_count += 1 # add up the "True"s
    if player1_count == 10 - player1_wins: # if all cards are true
        print("Player One has won this round!") 

        #reset round values
        turn = 1
        player1_hand = []
        player2_hand = []
        player1_wins += 1 # add a round win for player 1
        print("Starting next round...")
        
        #get new deck and hands
        game_prep(player1_wins, player2_wins, turn)

    for card in player2_hand: # for each card in the hand
        card2_count += 1 # count the cards
        if player2_hand[card2_count-1]["Spot"] == "True": #count how many of those spot's are true
            player2_count += 1 # add up the "True"s
    if player2_count == 10 - player2_wins: # if all cards are true
        print("Player Two has won this round!")
        
        #reset round values
        
        turn = 1
        player1_hand = []
        player2_hand = []
        player2_wins += 1 # add a round win for player 2
        print("Starting next round...")

        #get new deck and hands
        game_prep(player1_wins, player2_wins, turn)

#----------------------------------------------------------
# If the previous player's card isn't what the current player needs, then they will draw a card
# from the deck(retrieved from the Web API) that is then put into the form of a Card and then the format 
# used to determine if the card can be used. 
# once the card is made, it is use in the player's turn
def draw_a_card(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn):
    
    draw_card = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1" #get the card from the API deck
    draw_info = requests.get(draw_card).json() # request the information and save it to draw_info in json format
    drawn_card = Given_Card(**draw_info) #get needed values into drawn_card in Given_Card format from card_deck

    drawn_card = { #fit those values into the dictionary
                "Suit" : drawn_card.cards[0].suit,
                "Value" : drawn_card.cards[0].value, 
                "Spot" : "False"
                } 
    time.sleep(5)
    print(" ")

    #tell user who turn it is
    
    if turn == 1:
        print("It's Player One's Turn")
    
    
    #use the card in the turn
    player_turn(player1_hand, player2_hand, player1_wins, player2_wins, drawn_card, deck_id, turn)
#------------------
# This function is where the next player of a player turn, can take their opponent's discarded card 
# and use it for their own play(another man's trash is another's treasure sort of thing)
# but if they dont need it or it was a Jack/King they instead will draw a card from the deck
# queen is never discarded, because it can be used in any spot
def take_opponents(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn, take_card):
    
    print(" ")
    if turn%2 == 1:
        print("It's Player One's Turn!")
    else:
        print("It's Player Two's Turn!")
    
    # as long as the turn-ending card isn't a jack/king
    if take_card["Value"] != "KING" and take_card["Value"] != "JACK":
        if take_card["Value"] == "ACE":
            card_number = 1
        else:
            card_number = int(take_card["Value"])
        if turn%2 == 1:
            try:
                if player1_hand[card_number-1]["Spot"] == "False":
                    player_turn(player1_hand, player2_hand, player1_wins, player2_wins, take_card, deck_id, turn)
                else:
                    print(f"Player One does not need {take_card["Value"]} of {take_card["Suit"]}")
                    draw_a_card(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn)
            except IndexError:
                print(f"Player One does not need {take_card["Value"]} of {take_card["Suit"]}")
                draw_a_card(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn)
        else:
            try:
                if player2_hand[card_number-1]["Spot"] == "False":
                    player_turn(player1_hand, player2_hand, player1_wins, player2_wins, take_card, deck_id, turn)
                else:
                    print(f"Player Two does not need {take_card["Value"]} of {take_card["Suit"]}")
                    draw_a_card(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn)
            except IndexError:
                print(f"Player Two does not need {take_card["Value"]} of {take_card["Suit"]}")
                draw_a_card(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn)
    else:
        draw_a_card(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn)




#-------------------------------------
# This function is where the turn of the player happens,
# if the card is a Jack or King, the person loses their turn
# if the card is a Queen/Wild Card, they can replace any unfound card(in queen_card function)
# if the card is an Ace, it represents the 1st card and is treated as such
# for any number card, it represents that number and is put into that spot in the player's hand
# they will use the card that was previously in the card spot and continue their play with that
# however, for the Ace and Number Cards, if they're already called for, they will be set aside
# so if the other player needs that card, they can use it

def player_turn(player1_hand, player2_hand, player1_wins, player2_wins, drawn_card, deck_id, turn):
    time.sleep(5)
    check_win(player1_hand, player2_hand, player1_wins, player2_wins) # check if a player has won 10 times

    

    if drawn_card["Value"] == "JACK" or drawn_card["Value"] == "KING":
        print(f"Player has drawn the {drawn_card["Value"]} of {drawn_card["Suit"]}, next player's turn.")
        
        turn += 1
        take_opponents(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn, drawn_card)
    
    elif drawn_card["Value"] == "ACE":
        print(f"Player has drawn the {drawn_card["Value"]} of {drawn_card["Suit"]}.")
        if turn%2 == 1:
            if player1_hand[0]["Spot"] == "False":
                next_card = { #save the card that was previously in the spot
                    "Suit" : player1_hand[0]["Suit"],
                    "Value" : player1_hand[0]["Value"],
                    "Spot" : "False",
                }

                player1_hand[0] = { # replace the card in the spot with the queen card
                    "Suit" : "ACE",
                    "Value" : drawn_card["Value"],
                    "Spot" : "True"
                }
                print("Player One uses this card")
                print("Using new card...")
                print(" ")

                player_turn(player1_hand, player2_hand, player1_wins, player2_wins, next_card, deck_id, turn)
            
            else:
                print("You already have this card")
                turn += 1
                take_opponents(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn, drawn_card)
        else:
            if player2_hand[0]["Spot"] == "False":
                next_card = { #save the card that was previously in the spot
                    "Suit" : player2_hand[0]["Suit"],
                    "Value" : player2_hand[0]["Value"],
                    "Spot" : "False",
                }
                player2_hand[0] = { # replace the card in the spot with the queen card
                    "Suit" : drawn_card["Suit"],
                    "Value" : drawn_card["Value"],
                    "Spot" : "True"
                }

                print("Player Two uses this card")
                print("Using new card...")
                print(" ")
                player_turn(player1_hand, player2_hand, player1_wins, player2_wins, next_card, deck_id, turn)
            else:
                print("You already have this card")
                turn += 1
                take_opponents(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn, drawn_card)
    elif drawn_card["Value"] == "QUEEN":
        print(f"You have drawn the QUEEN of {drawn_card["Suit"]}, which place do u want this card to take?(In number format)")
        if turn%2 == 1:
            player1_hand, next_card = queen_card(player1_hand, player2_hand, player1_hand, player1_wins, player2_wins, drawn_card, deck_id)
            player_turn(player1_hand, player2_hand, player1_wins, player2_wins, next_card, deck_id, turn)
        else:
            player2_hand, next_card = queen_card(player1_hand, player2_hand, player2_hand, player1_wins, player2_wins, drawn_card, deck_id)
            player_turn(player1_hand, player2_hand, player1_wins, player2_wins, next_card, deck_id, turn)
    else:
        print(f"Player has drawn the {drawn_card["Value"]} of {drawn_card["Suit"]}.")
        card_number = int(drawn_card["Value"])
        if turn%2 == 1:
            try:
                if player1_hand[card_number-1]["Spot"] == "False":

                    print("Player One uses this card")
                    next_card = { #save the card that was previously in the spot
                    "Suit" : player1_hand[card_number-1]["Suit"],
                    "Value" : player1_hand[card_number-1]["Value"],
                    "Spot" : "False",
                    }
                    player1_hand[card_number-1] = { # replace the card in the spot with the queen card
                        "Suit" : drawn_card["Suit"],
                        "Value" : drawn_card["Value"],
                        "Spot" : "True"
                    }
                    print("Using new card...")
                    print(" ")
                    player_turn(player1_hand, player2_hand, player1_wins, player2_wins, next_card, deck_id, turn)
                else:
                    print("You already have this card")
                    turn += 1
                    take_opponents(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn, drawn_card)
            except IndexError:
                print("You don't need this card")
                turn += 1
                take_opponents(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn, drawn_card)
            


        else:
            try:
                if player2_hand[card_number-1]["Spot"] == "False":

                    print("Player Two uses this card")
                    next_card = { #save the card that was previously in the spot
                    "Suit" : player2_hand[card_number-1]["Suit"],
                    "Value" : player2_hand[card_number-1]["Value"],
                    "Spot" : "False",
                    }
                    player2_hand[card_number-1] = { # replace the card in the spot with the queen card
                        "Suit" : drawn_card["Suit"],
                        "Value" : drawn_card["Value"],
                        "Spot" : "True"
                    }
                    print("Using new card...")
                    print(" ")
                    player_turn(player1_hand, player2_hand, player1_wins, player2_wins, next_card, deck_id, turn)
                else:
                    print("You already have this card")
                    turn += 1
                    take_opponents(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn, drawn_card)
            except IndexError:
                print("You don't need this card")
                turn += 1
                take_opponents(player1_hand, player2_hand, player1_wins, player2_wins, deck_id, turn, drawn_card)
            


            
#-------------------------------------------------
# this function is to see if a card in the player's hand is not already in the right spot, 
# if not, then the Queen(Wild Card) can be used to replace it
def queen_card(player1_hand, player2_hand, player_hand, player1_wins, player2_wins, drawn_card, deck_id):
    print("Please choose a spot!")
    
    try:
        choice = int(input())
        # if the spot is already called for
        if player_hand[choice-1]["Spot"] == "False":
            # spot not called for, therefore can place the queen card here
            next_card = { #save the card that was previously in the spot
                "Suit" : player_hand[choice-1]["Suit"],
                "Value" : player_hand[choice-1]["Value"],
                "Spot" : "False",
            }
            player_hand[choice-1] = { # replace the card in the spot with the queen card
                "Suit" : drawn_card["Suit"],
                "Value" : "QUEEN",
                "Spot" : "True",
            }
            print("Card Replaced!")
            return player_hand, next_card #return these two values to player_turn so that the turn continues

        else:
            print("card already in right spot")
            # direct to player_turn with same queen_card, coming back to this function
            player_turn(player1_hand, player2_hand, player1_wins, player2_wins, drawn_card, deck_id, turn)
        
    # if the user inputs anything but a number in the player_hand index
    except IndexError:
        print("Please input a NUMBER")
        player_turn(player1_hand, player2_hand, player1_wins, player2_wins, drawn_card, deck_id, turn)

#----------------------------------------------------
#start the code off by starting the first round of the game
game_prep(player1_wins, player2_wins, turn)
