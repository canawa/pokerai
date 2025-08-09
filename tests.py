import torch
import torch.nn as nn
import torch.nn.functional as F

a = torch.tensor([[2,1,0],
                  [3,1,2]])
a_softmax = F.softmax(a.float(), dim=1)
print(a_softmax)
print(a.shape)