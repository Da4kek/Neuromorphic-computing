import torch
import torch.nn as nn 
from torch.utils.data import DataLoader
import numpy as np 
import itertools 
from Utils.MeasureAcc import measure_accuracy
from Models.SNN_leaky import FullyConnectedSNN as SNN
from torchvision import datasets,transforms

batch_size = 128 
data_path = "/data/mnist"

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

transform = transforms.Compose(
    [
        transforms.Resize((28, 28)),
        transforms.Grayscale(),
        transforms.ToTensor(),
        transforms.Normalize((0,), (1,)),
    ]
)

mnist_train = datasets.MNIST(data_path, train=True, download=True, transform=transform)
mnist_test = datasets.MNIST(data_path, train=False, download=True, transform=transform)

train_loader = DataLoader(mnist_train,batch_size=batch_size,shuffle=True,drop_last=True)
test_loader = DataLoader(mnist_test,batch_size = batch_size,shuffle=True,drop_last=True)

num_inputs = 28*28
num_hidden = 1000
num_outputs = 10

num_steps = 25 
beta = 0.95

net = SNN.Net(num_inputs,num_hidden,num_outputs,num_steps,beta).to(device)


loss = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(),lr=5e-4,betas=(0.9,0.999))

num_epoch = 1
counter = 0

for epoch in range(num_epoch):
    train_batch = iter(train_loader)

    for data, targets in train_batch:
        data = data.to(device)
        targets = targets.to(device)

        net.train()
        spk_rec, _ = net(data)

        loss_val = torch.zeros((1),dtype=torch.float,device=device)
        loss_val = loss(spk_rec.sum(0),targets)

        optimizer.zero_grad()
        loss_val.backward()
        optimizer.step()

        if counter %10 ==0:
            print(f"Iteration: {counter} \t train loss: {loss_val.item()}")
        counter +=1
        if counter ==100:
            break


print(f"Test accuracy: {measure_accuracy(net,test_loader)}")