import torch
import torch.nn as nn
import torch.nn.functional as F

data = torch.load('wine-red.pt')
X_train = torch.load('X_train.pt')
y_train = torch.load('y_train.pt')
X_val = torch.load('X_val.pt')
y_val = torch.load('y_val.pt')

print(X_train.shape, y_train.shape, X_val.shape, y_val.shape)





 
