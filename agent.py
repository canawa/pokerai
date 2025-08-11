import torch
from numpy import*
import torch.nn as nn
import torch.nn.functional as F
from env import PokerEnv, env

class PolicyNetwork(nn.Module): # наследуем класс nn.Module
    def __init__(self,in_features,out_features): # конструктор 
        super().__init__() # вызываем конструктор родителя и передаем из него аргументы
        self.fc1 = nn.Linear(in_features,out_features) # входные данные и выходные данные, сюда передаются данные из конструктора
    def forward(self,x):
        x=self.fc1(x)
        return x

model = PolicyNetwork(169,2) # создаем модель, а функции вызываем потом (объект класса PolicyNetwork)
print(list(model.parameters())) # это генератор (объект), поэтому просто его вызвать не получится, но через list получится увидеть то что внутри
optimizer = torch.optim.Adam(model.parameters()) # задаем оптимизатор

for _ in range(10):
    env.reset() # сбрасываем его состояние
    state = env.get_one_hot_vector() # state это состояние среды, ну ключевая инфа, в моем случае это ключ инфа (one_hot_vector)
    output = model.forward(state.float()) # вернет два значения нейрона
    probabilities = F.softmax(output,dim=0) # переводим в проценты
    math_correct_decision = torch.argmax(probabilities).item() # вернет индекс максимального (в прод, но не для обучения)
    multinominal_decision = torch.multinomial(probabilities,1).item() # случайно выбирает действие пропорционально вероятности (для обучения), вернет либо 0 либо 1 (возвращает индексы)
    # индекс 1 - пуш, индекс 0 - фолд. То есть в тензоре вероятностей первое значение это вероятность фолда, второе - пуша.
    round_results = env.step(multinominal_decision) # записываем результаты и инфу по раунду игры (env.py)
    reward = round_results[0]
    # POLICY GRADIENT LOSS #
    loss = -torch.log(probabilities[multinominal_decision]) * reward # пока просто запомнить (!!!ПОТОМ ОБЯЗАТЕЛЬНО ПОНЯТЬ ПОЧЕМУ ТАК)
    optimizer.zero_grad() # сброс старых градиентов
    loss.backward() # автодиф  (найдет производные от каждого веса и запишет их в градиенты)
    optimizer.step() # обновление весов
    print('Выход:', output.detach().numpy(), 'Вероятность:', probabilities.detach().numpy(),'Решение:', multinominal_decision, '(PUSH)' if multinominal_decision==1 else '(FOLD)')
    print('Награда:', round_results[0], '; Раунд окончен:', round_results[1],'; Your Hand:', round_results[2], '; Op`s Hand:', round_results[3])
    print('============================================================================================')