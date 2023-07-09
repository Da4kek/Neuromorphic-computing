import torch


device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
def measure_accuracy(model,dataloader):
    with torch.no_grad():
        model.eval()
        running_length = 0
        running_acc = 0

        for data,targets in iter(dataloader):
            data = data.to(device)
            targets = targets.to(device)
            spk_rec, _ = model(data)
            spike_count = spk_rec.sum(0)
            _,max_spike = spike_count.max(1)

            num_correct = (max_spike == targets).sum()

            running_length += len(targets)
            running_acc += num_correct 
        accuracy = (running_acc / running_length)
        return accuracy.item()