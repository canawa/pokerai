# poker_ai/env.py
# Простая среда для хедз-ап покера 10BB — префлоп push/fold
import random
import torch
from cards import Draw
cards = Draw() # подтягиваем класс
class PokerEnv:
    def __init__(self): # конструктор
        self.reward = 0 # задаем значение награды (оно будет доступно в любом методе этого класса)
        self.done = False # задаем значение done (оно будет доступно в любом методе этого класса)
        self.reset()

    def reset(self): # сбрасываем стек и все остальное
        self.player_hand = cards.draw_pocket_cards()[0]
        self.villain_hand = cards.draw_pocket_cards()[1]
        self.done = False
        return self.player_hand, self.villain_hand

    def get_hand(self): # вытаскиваем комбинацию
        return self.hand # возвращаем комбинацию свою

    def to_one_hot(self,card): # сюда подается целая комба (например стартовая рука или борд)
        one_hot_vector = cards.cards_to_one_hot(card) # вернет ретерном ванхот вектор
        return one_hot_vector
    


    # def step(self,action): # действие (пуш или фолд) пуш = 1 фолд = 0
    #     if action == 0: # фолд
    #         reward = -0.5 # штраф за фолд (не надо это здесь суммировать, это локально)
    #         self.done = True # и игра закончена
    #         self.opp_hand = None
    #         return reward, self.done, self.hand, self.opp_hand # возвращаем награду и done

    #     else: # если пуш
    #         self.opp_hand = random.randint(0,168) # выбираем случайную комбинацию из двух карт, делаем это тут чтобы заранее не знать комбинацию противника
    #         if self.hand > self.opp_hand: # если наша комбинация лучше то мы выигрываем
    #             reward = 10 # выигрыш
                
    #         else: # если наша комбинация хуже то мы проигрываем
    #             reward = -10 # проигрыш
    #         self.done = True # и игра закончена
    #         return reward, self.done, self.hand, self.opp_hand # возвращаем награду и done

env = PokerEnv()
draw = env.reset()
player_hand = draw[0]
villain_hand = draw[1]
player_hand_one_hot = cards.cards_to_one_hot(player_hand) # one hot вектор для своей руки
villain_hand_one_hot = cards.cards_to_one_hot(villain_hand) # one hot вектор для руки противника

flop = cards.draw_flop() # заранее раздаем, но не даем эту инфу модели
turn = cards.draw_turn() # заранее раздаем, но не даем эту инфу модели
river = cards.draw_river() # заранее раздаем, но не даем эту инфу модели

flop_one_hot = cards.cards_to_one_hot(flop) # one hot вектор для флопа
turn_one_hot = cards.cards_to_one_hot(turn) # one hot вектор для терна
river_one_hot = cards.cards_to_one_hot(river) # one hot вектор для ривера

pretty_cards = cards.get_pretty_cards() # вытщаит все карты в красивом виде (борд тоже)
print(pretty_cards)









