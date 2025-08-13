import torch
from numpy import*
import torch.nn as nn
import torch.nn.functional as F
from env import PokerEnv, env
from tqdm import tqdm

# Автоматическое определение устройства (GPU CUDA или CPU)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f'Используется устройство: {device}')

class PolicyNetwork(nn.Module): # наследуем класс nn.Module
    def __init__(self,in_features,out_features): # конструктор 
        super().__init__() # вызываем конструктор родителя и передаем из него аргументы
        self.fc1 = nn.Linear(in_features,out_features) # входные данные и выходные данные, сюда передаются данные из конструктора (слой)
    def forward(self,x):
        y=self.fc1(x) # передаем аргумент в слой
        return y # возвращаем результат

model = PolicyNetwork(52,2) # создаем модель, а функции вызываем потом (объект класса PolicyNetwork)
model = model.to(device) # перемещаем модель на нужное устройство

optimizer = torch.optim.Adam(model.parameters()) # задаем оптимизатор

commands = input('retrain - С нуля подбирать веса, download - Подгрузить веса из model.pt: \n ')
if commands == 'download':
    print('Используем старые веса. Подгружаем...')
    state_dict = torch.load('model.pt', map_location=device) # сам процесс подгрузки с указанием устройства
    model.load_state_dict(state_dict) # подгружаем веса в виде словаря
    print(list(model.parameters())) # это генератор (объект), поэтому просто его вызвать не получится, но через list получится увидеть то что внутри
else:
    print('Начинаем обучение с нуля. Старые данные будут утеряны.')

commands = input('train or validation: ')
if commands == 'train':
    loss_list = []
    for _ in tqdm(range(100000)):
        env.reset() # сбрасываем его состояние
        state = env.get_hand_one_hot() # state это состояние среды, ну ключевая инфа, в моем случае это ключ инфа (one_hot_vector)
        state = state.to(device) # перемещаем состояние на нужное устройство
        output = model.forward(state.float()) # вернет два значения нейрона
        probabilities = F.softmax(output,dim=0) # переводим в проценты
        math_correct_decision = torch.argmax(probabilities).item() # вернет индекс максимального (в прод, но не для обучения)
        multinominal_decision = torch.multinomial(probabilities,1).item() # случайно выбирает действие пропорционально вероятности (для обучения), вернет либо 0 либо 1 (возвращает индексы)
        # индекс 1 - пуш, индекс 0 - фолд. То есть в тензоре вероятностей первое значение это вероятность фолда, второе - пуша.
        round_results = env.step(multinominal_decision) # записываем результаты и инфу по раунду игры (env.py)
        reward = round_results[0]
        # POLICY GRADIENT LOSS #
        loss = -torch.log(probabilities[multinominal_decision]) * reward # пока просто запомнить (!!!ПОТОМ ОБЯЗАТЕЛЬНО ПОНЯТЬ ПОЧЕМУ ТАК) выбирает решение мультиноминал пропорционально вероятности
        # loss = -loss
        optimizer.zero_grad() # сброс старых градиентов (чтобы не складывались)
        loss.backward() # автодиф  (найдет производные от каждого веса и запишет их в градиенты)
        optimizer.step() # обновление весов градиентным спуском
        loss_list.append(abs(loss.item()))
        # print('Выход:', output.detach().numpy(), 'Вероятность:', probabilities.detach().numpy(),'Решение:', multinominal_decision, '(PUSH)' if multinominal_decision==1 else '(FOLD)')
        # print('Награда:', round_results[0], '; Раунд окончен:', round_results[1],'; Your Hand:', round_results[4], '; Op`s Hand:', round_results[5])
        # print('Loss:', loss.item())
        # print('============================================================================================')
        if _ % 1000 == 0 and _ != 0:
            print('Step:', _, 'Loss:', sum(loss_list) / len(loss_list)) # среднее значение потерь
            loss_list = []
        if _ % 10000 == 0 and _ != 0:
            torch.save(model.state_dict(), 'model.pt') # сохраняем веса каждые 10000 шагов
            print('model saved')
    print('training done')
elif commands == 'validation':
    for _ in range(10):
        env.reset() # обновляем среду
        state = env.get_hand_one_hot() # запрашиваем нашу руку
        state = state.to(device) # перемещаем состояние на нужное устройство
        output = model.forward(state.float())
        probabilities = F.softmax(output, dim=0)
        math_correct_decision = torch.argmax(probabilities).item() # вернет индекс максимального (в прод, но не для обучения)
        multinominal_decision = torch.multinomial(probabilities,1).item() # случайно выбирает действие пропорционально вероятности (для обучения), вернет либо 0 либо 1 (возвращает индексы)
        round_results = env.step(math_correct_decision)
        # print('Выход:', output.detach().cpu().numpy(), 'Вероятность:', probabilities.detach().cpu().numpy(),'Решение:', math_correct_decision, '(PUSH)' if math_correct_decision==1 else '(FOLD)')
        # print('Награда:', round_results[0], '; Раунд окончен:', round_results[1],'; Your Hand:', round_results[4], '; Op`s Hand:', round_results[5], '; Board:', round_results[6])
        # print('Результат:', 
        # 'Победа' if round_results[0] == 10 else 
        # 'Не вскрывались' if round_results[0] == -0.5 else 
        # 'Поражение')
        # print('==========================================================================')



