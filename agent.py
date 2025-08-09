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
# print(model) # посмотреть слои
print(list(model.parameters())) # это генератор (объект), поэтому просто его вызвать не получится, но через list получится увидеть то что внутри
for _ in range(10):
    env.reset() # сбрасываем его состояние
    state = env.get_one_hot_vector() # state это состояние среды, ну ключевая инфа, в моем случае это ключ инфа (one_hot_vector)
    output = model.forward(state.float()) # вернет два значения нейрона
    probabilities = F.softmax(output,dim=0) # переводим в проценты
    print('Выход:', output.detach().numpy(), 'Вероятность:', probabilities.detach().numpy())