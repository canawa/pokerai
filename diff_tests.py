import torch
import torch.nn as nn
import torch.nn.functional as F

# Поработаем с градиентами, у нас будет функция y=a^2 , с известной точкой a=2.5, надо найти производную в этой точке
cords = torch.tensor([1.5, 2], requires_grad=True)

lr = 0.1 # learning rate

for _ in range(50):
    f = cords[0]**2 + cords[1]**2 + 11 # выдумали функцию
    f.backward() # считаем градиенты
    with torch.no_grad():
        cords -= lr*cords.grad # обновляем координаты 
        
    cords.grad = None
    print(f)
print(f'X: {cords[0]}, Y: {cords[1]}, f: {f}')




