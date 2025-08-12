# poker_ai/env.py
# Простая среда для хедз-ап покера 10BB — префлоп push/fold
import random
import torch
from cards import Draw
cards = Draw() # подтягиваем класс
class PokerEnv:
    def __init__(self): # конструктор
        self.cards = Draw() # подтягиваем класс
        self.cards.reset()
        self.reward = 0 # задаем значение награды (оно будет доступно в любом методе этого класса)
        self.done = False # задаем значение done (оно будет доступно в любом методе этого класса)
        self.reset()

    def reset(self): # сбрасываем стек и все остальное
        self.cards = Draw() # подтягиваем класс
        self.cards.reset()
        self.cards.board = [] # сбрасываем борд (надо так потому что там extend, а не перезапись, поэтому все ломается)
        self.hands = self.cards.draw_pocket_cards() # раздаем руки
        self.player_hand = self.hands[0]
        self.villain_hand = self.hands[1]
        self.reward = 0
        self.flop = []
        self.turn = []
        self.river = []
        self.score = []
        self.done = False
        self.player_hand_one_hot = self.cards.cards_to_one_hot(self.player_hand) # one hot вектор для своей руки
        self.villain_hand_one_hot = self.cards.cards_to_one_hot(self.villain_hand) # one hot вектор для руки противника
        return self.player_hand_one_hot, self.villain_hand_one_hot, self.reward, self.done

    def get_hand_one_hot(self): # вытаскиваем комбинацию
        return self.player_hand_one_hot # возвращаем комбинацию свою

    def get_pretty_cards(self):
        pretty_cards = self.cards.get_pretty_cards()
        self.player_pretty_cards = pretty_cards[0]
        self.villain_pretty_cards = pretty_cards[1]
        self.board_pretty_cards = pretty_cards[2]
        return self.player_pretty_cards, self.villain_pretty_cards, self.board_pretty_cards

    def step(self,action): # действие (пуш или фолд) пуш = 1 фолд = 0
        
        if action == 0: # фолд
            self.reward = -0.5
            self.done = True
            self.get_pretty_cards()
            return self.reward, self.done, self.player_hand_one_hot, self.villain_hand_one_hot, self.player_pretty_cards, self.villain_pretty_cards, self.board_pretty_cards
        elif action == 1: # пуш (играем тут префлоп ток)
            self.flop = self.cards.draw_flop() # заранее раздаем, но не даем эту инфу модели
            self.turn = self.cards.draw_turn() # заранее раздаем, но не даем эту инфу модели
            self.river = self.cards.draw_river() # заранее раздаем, но не даем эту инфу модели

            self.flop_one_hot = self.cards.cards_to_one_hot(self.flop) # one hot вектор для флопа
            self.turn_one_hot = self.cards.cards_to_one_hot(self.turn) # one hot вектор для терна
            self.river_one_hot = self.cards.cards_to_one_hot(self.river) # one hot вектор для ривера

            self.score = self.cards.get_score()
            if self.score[0] > self.score[1]:
                self.reward = 9.5
            elif self.score[0] < self.score[1]:
                self.reward = -10
            self.done = True
            self.get_pretty_cards()
            hands = [self.player_hand, self.villain_hand]
            board = self.river
            # cards.evaluator.hand_summary(board, hands)
            return self.reward, self.done, self.player_hand_one_hot, self.villain_hand_one_hot, self.player_pretty_cards, self.villain_pretty_cards, self.board_pretty_cards, hands, board

env = PokerEnv()





# pretty_cards = cards.get_pretty_cards() # вытщаит все карты в красивом виде (борд тоже)
# print(pretty_cards)
# score = cards.get_score()
# print(score)








