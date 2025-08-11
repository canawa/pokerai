import torch
from treys import Card, Deck, Evaluator

class Draw():
    def __init__(self):
        self.deck = Deck()
        self.evaluator = Evaluator()

    def draw_pocket_cards(self):
        self.player_hand = self.deck.draw(2)
        self.villain_hand = self.deck.draw(2)
        return self.player_hand, self.villain_hand
    
    def draw_flop(self):
        self.board = self.deck.draw(3)
        return self.board
    
    def draw_turn(self):
        self.board = self.deck.draw(1)
        return self.board
    
    def draw_river(self):
        self.board = self.deck.draw(1)
        return self.board
    
    def get_pretty_cards(self):
        self.player_str = "Player hand: " + " ".join([Card.int_to_str(c) for c in self.player_hand])
        self.villain_str = "Villain hand: " + " ".join([Card.int_to_str(c) for c in self.villain_hand])
        self.board_str = "Board: " + " ".join([Card.int_to_str(c) for c in self.board])
        return self.player_str, self.villain_str, self.board_str
    
    def get_score(self):
        self.player_score = self.evaluator.evaluate(self.board, self.player_hand)
        self.villain_score = self.evaluator.evaluate(self.board, self.villain_hand)



