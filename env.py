# poker_ai/env.py
# Простая среда для хедз-ап покера 10BB — префлоп push/fold
import random
import torch

class PokerEnv:
    def __init__(self): # конструктор
        self.reward = 0 # задаем значение награды (оно будет доступно в любом методе этого класса)
        self.done = False # задаем значение done (оно будет доступно в любом методе этого класса)
        self.reset()

    def reset(self): # сбрасываем стек и все остальное
        self.hand = random.randint(0,168) # выбираем случайную комбинацию из двух карт (0-168) чтоб было удобнее в тензор ведь там от 0
        self.done = False

    def get_hand(self): # вытаскиваем комбинацию
        return self.hand # возвращаем комбинацию свою

    def get_one_hot_vector(self): # просто hand, потому что описание через self дает возможность вызывать эту функцию из любого метода класса
        self.one_hot = torch.zeros(169)
        self.one_hot[self.hand] = 1
        return self.one_hot


    def step(self,action): # действие (пуш или фолд) пуш = 1 фолд = 0
        if action == 0: # фолд
            reward = -0.5 # штраф за фолд (не надо это здесь суммировать, это локально)
            self.done = True # и игра закончена
            self.opp_hand = None
            return reward, self.done, self.hand, self.opp_hand # возвращаем награду и done

        else: # если пуш
            self.opp_hand = random.randint(0,168) # выбираем случайную комбинацию из двух карт, делаем это тут чтобы заранее не знать комбинацию противника
            if self.hand > self.opp_hand: # если наша комбинация лучше то мы выигрываем
                reward = 1 # выигрыш
                
            else: # если наша комбинация хуже то мы проигрываем
                reward = -1 # проигрыш
            self.done = True # и игра закончена
            return reward, self.done, self.hand, self.opp_hand # возвращаем награду и done

env = PokerEnv()
