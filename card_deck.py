from pydantic import BaseModel

# get the deck_id from the API to use during each round
class Deck(BaseModel):
    deck_id: str
    def __str__(self):
        return f"{self.deck_id}"

# each card's suit and value is saved from the API's generated card 
class Card(BaseModel):
    suit : str
    value : str

    def __str__(self):
        return f"{self.suit} | {self.value}"

#Given Card is a list of Card ^
class Given_Card(BaseModel):
    cards : list[Card]


    
