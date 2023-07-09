from snntorch import surrogate
import torch.nn as nn
import numpy as np
import torch


class Net(nn.Module):
    def __init__(self,num_inputs,num_hidden,num_outputs,num_steps,beta):
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden 
        self.num_outputs = num_outputs 
        self.num_steps = num_steps
        self.beta = self.beta
        super().__init__()

        self.fc1 = nn.Linear(self.num_inputs, self.num_hidden)
        self.lif1 = nn.Leaky(beta = self.beta)
        self.fc2 = nn.Linear(self.num_hidden,self.num_outputs)
        self.lif2 = nn.Leaky(beta=self.beta)
    
    def forward(self,x):
        mem1 = self.lif1.init_leaky()
        mem2 = self.lif2.init_leaky()

        spk2_rec = []
        mem2_rec = []

        for step in range(self.num_steps):
            cur1 = self.fc1(x.flatten(1))
            spk1,mem1 = self.lif1(cur1,mem1)
            cur2 = self.fc2(spk1)
            spk2,mem2 = self.lif2(cur2,mem2)

            spk2_rec.append(spk2)
            mem2_rec.append(mem2)
        return torch.stack(spk2_rec,dim=0),torch.stack(mem2_rec,dim=0)
    