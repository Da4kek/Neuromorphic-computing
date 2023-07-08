import snntorch as snn
from snntorch import spikeplot as splt
import torch
import matplotlib.pyplot as plt
from IPython.display import HTML
from Utils import plot
import matplotlib

matplotlib.use("Agg")
lif = snn.Leaky(beta=0.8)

num_steps = 200
w = 0.8
x = torch.cat((torch.zeros(10), torch.ones(1) * w, torch.zeros(189)))

mem = torch.zeros(1)
spk = torch.zeros(1)

mem_rec = []
spk_rec = []

for step in range(num_steps):
    spk, mem = lif(x[step], mem)
    mem_rec.append(mem)
    spk_rec.append(spk)

mem_rec = torch.stack(mem_rec)
spk_rec = torch.stack(spk_rec)

plot.Plotcurrentspike(
    x, mem_rec, spk_rec, thr_line=1, y_lim=1.0, title="leaky neuron model"
)
plt.show()
