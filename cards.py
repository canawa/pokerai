import torch
from treys import Card, Deck, Evaluator

class Draw():
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.evaluator = Evaluator()
        self.deck = Deck() # подтягиваем классы
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
        # print(self.board, self.player_hand, self.villain_hand)
        self.player_score = self.evaluator.evaluate(self.board, self.player_hand)
        self.villain_score = self.evaluator.evaluate(self.board, self.villain_hand)
        return self.player_score, self.villain_score
    
    def card_to_index(self, cards): # переводит в число (0 - 51)
        index_list = []
        # Все 52 карты и их индексы
        CARD_INDICES = { # словарь для перевода карт в индексы
        '2s': 0, '2h': 1, '2d': 2, '2c': 3,
        '3s': 4, '3h': 5, '3d': 6, '3c': 7,
        '4s': 8, '4h': 9, '4d': 10, '4c': 11,
        '5s': 12, '5h': 13, '5d': 14, '5c': 15,
        '6s': 16, '6h': 17, '6d': 18, '6c': 19,
        '7s': 20, '7h': 21, '7d': 22, '7c': 23,
        '8s': 24, '8h': 25, '8d': 26, '8c': 27,
        '9s': 28, '9h': 29, '9d': 30, '9c': 31,
        'Ts': 32, 'Th': 33, 'Td': 34, 'Tc': 35,
        'Js': 36, 'Jh': 37, 'Jd': 38, 'Jc': 39,
        'Qs': 40, 'Qh': 41, 'Qd': 42, 'Qc': 43,
        'Ks': 44, 'Kh': 45, 'Kd': 46, 'Kc': 47,
        'As': 48, 'Ah': 49, 'Ad': 50, 'Ac': 51
    }
        for card in cards: # перебираем карты
            try:
                card_str = Card.int_to_str(card)
                if card_str in CARD_INDICES: # если карта есть в словаре
                    index = CARD_INDICES[card_str] # переводим в индекс (типо индекс равен значению по ключу)
                    index_list.append(index) # добавляем в список
                    # print(f'Card {card_str} converted to index {index}')
                # else:
                    # print(f'Card {card_str} not found in CARD_INDICES')
            except Exception as e:
                print(f'Error {e}')
        return index_list
    
    def cards_to_one_hot(self, cards): # ванхот
        one_hot_vector = torch.zeros(52)
        index_list = self.card_to_index(cards)
        for index in index_list:
            one_hot_vector[index] = 1
        return one_hot_vector




