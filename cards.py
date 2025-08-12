import torch
from treys import Card, Deck, Evaluator

class Draw():
    def __init__(self):

        self.deck = Deck() # подтягиваем классы
        self.evaluator = Evaluator()

        self.board = [] # инициализируем борд и руки, чтобы не было ошибки при вызове борда до его раздачи
        self.player_hand = []
        self.villain_hand = []

    def draw_pocket_cards(self): # генерирует стартовые руки (оппа и игрока)
        self.player_hand = self.deck.draw(2) 
        self.villain_hand = self.deck.draw(2)
        return self.player_hand, self.villain_hand
    
    def draw_flop(self): # раздает флоп
        self.board.extend(self.deck.draw(3)) # добавляем флоп к борду (экстенд чтобы не было вложенности)
        return self.board
    
    def draw_turn(self):# раздает терн
        self.board.extend(self.deck.draw(1)) # добавляем терн к борду (экстенд чтобы не было вложенности)
        return self.board
    
    def draw_river(self):# раздает ривер
        self.board.extend(self.deck.draw(1)) # добавляем ривер к борду (экстенд чтобы не было вложенности)
        return self.board
    
    def get_pretty_cards(self): # чисто для вывода
        self.player_str = "Player hand: " + " ".join([Card.int_to_str(c) for c in self.player_hand])
        self.villain_str = "Villain hand: " + " ".join([Card.int_to_str(c) for c in self.villain_hand])
        self.board_str = "Board: " + " ".join([Card.int_to_str(c) for c in self.board]) 
        return self.player_str, self.villain_str, self.board_str
    
    def get_score(self): # по этой херне будем разбирать кто выиграл
        self.player_score = self.evaluator.evaluate(self.board, self.player_hand)
        self.villain_score = self.evaluator.evaluate(self.board, self.villain_hand)
        return self.player_score, self.villain_score
    
    def card_to_index(self, cards): # переводит в число (0 - 51)
        index_list = []
        for card in cards:
            rank = Card.get_rank_int(card)
            suit = Card.get_suit_int(card)
            index = (rank - 2) * 4 + suit
            index_list.append(index)
        return index_list
    
    def cards_to_one_hot(self, cards): # ванхот
        one_hot_vector = torch.zeros(52)
        index_list = self.card_to_index(cards)
        for index in index_list:
            one_hot_vector[index] = 1
        return one_hot_vector




