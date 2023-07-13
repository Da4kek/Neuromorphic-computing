from bindsnet.datasets import MNIST
from bindsnet.encoding import PoissonEncoder
from bindsnet.evaluation import all_activity, assign_labels, proportion_weighting
from bindsnet.models.models import DiehlAndCook2015
from bindsnet.network.monitors import Monitor
from bindsnet.utils import get_square_assignments, get_square_weights
import torch
import os
import numpy as np
from torchvision import transforms
from time import time as t
from tqdm import tqdm
from bindsnet.analysis.plotting import (
    plot_assignments,
    plot_input,
    plot_performance,
    plot_spikes,
    plot_voltages,
    plot_weights,
)
import matplotlib.pyplot as plt


def CompAcc(accuracy_var, label_tensor, all_activity_pred, proportion_pred):
    accuracy_var["all"].append(
        100
        * torch.sum(label_tensor.long() == all_activity_pred).item()
        / len(label_tensor)
    )
    accuracy_var["proportion"].append(
        100
        * torch.sum(label_tensor.long() == proportion_pred).item()
        / len(label_tensor)
    )
    print(
        "\nAll activity Acc: %.2f (last), %.2f (average), %.2f (best)"
        % (
            accuracy_var["all"][-1],
            np.mean(accuracy_var["all"]),
            np.max(accuracy_var["all"]),
        )
    )
    print(
        "Proportion weighting Acc: %.2f (last), %.2f (average), %.2f (best)\n"
        % (
            accuracy_var["proportion"][-1],
            np.mean(accuracy_var["proportion"]),
            np.max(accuracy_var["proportion"]),
        )
    )


class Stdp:
    def __init__(
        self,
        seed: int = 0,
        n_neurons: int = 100,
        n_epochs: int = 1,
        n_test: int = 10000,
        n_train: int = 60000,
        n_workers: int = -1,
        exc: float = 22.5,
        inh: float = 120,
        theta_plus: float = 0.05,
        time: int = 250,
        dt: int = 1.0,
        intensity: int = 128,
        progress_interval: int = 250,
        update_interval: int = 250,
        train: bool = True,
        test: bool = False,
        plot: bool = True,
        gpu: bool = True,
    ):
        self.seed = seed
        self.n_neurons = n_neurons
        self.n_epochs = n_epochs
        self.n_test = n_test
        self.n_train = n_train
        self.n_workers = n_workers
        self.exc = exc
        self.inh = inh
        self.theta_plus = theta_plus
        self.time = time
        self.dt = dt
        self.intensity = intensity
        self.progress_interval = progress_interval
        self.update_interval = update_interval
        self.train = train
        self.test = test
        self.plot = plot
        self.gpu = gpu

    def _gpu_init(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if self.gpu and torch.cuda.is_available():
            torch.cuda.manual_seed_all(self.seed)
        else:
            torch.manual_seed(self.seed)
            device = "cpu"
            if self.gpu:
                self.gpu = False
        torch.set_num_threads(os.cpu_count() - 1)
        print("Running on device= ", device)
        return device

    def _workers_init(self):
        if self.n_workers == -1:
            self.n_workers = 0
        return self.n_workers

    def _train_init(self):
        if not self.train:
            self.update_interval = self.n_test
        return self.update_interval

    def _intensity_init(self):
        start_intensity = self.intensity
        return start_intensity

    def Network(self):
        n_sqrt = int(np.ceil(np.sqrt(self.n_neurons)))
        network = DiehlAndCook2015(
            n_inpt=784,
            n_neurons=self.n_neurons,
            exc=self.exc,
            inh=self.inh,
            dt=self.dt,
            norm=78.4,
            theta_plus=self.theta_plus,
            inpt_shape=(1, 28, 28),
        )
        device = self._gpu_init()
        if self.gpu:
            network.to("cuda")
        train_dataset = MNIST(
            PoissonEncoder(time=self.time, dt=self.dt),
            None,
            root=os.path.join("..", "..", "data", "MNIST"),
            download=True,
            train=True,
            transform=transforms.Compose(
                [
                    transforms.ToTensor(),
                    transforms.Lambda(lambda x: x * self._intensity_init()),
                ]
            ),
        )
        spike_record = torch.zeros(
            (self._train_init(), int(self.time / self.dt), self.n_neurons),
            device=device,
        )
        n_classes = 10
        assignments = -torch.ones(self.n_neurons, device=self._gpu_init())
        proportions = torch.zeros((self.n_neurons, n_classes), device=device)
        rates = torch.zeros((self.n_neurons, n_classes), device=device)
        accuracy = {"all": [], "proportion": []}
        exc_voltage_monitor = Monitor(
            network.layers["Ae"], ["v"], time=int(self.time / self.dt), device=device
        )
        inh_voltage_monitor = Monitor(
            network.layers["Ai"], ["v"], time=int(self.time / self.dt), device=device
        )
        network.add_monitor(exc_voltage_monitor, name="exc_voltage")
        network.add_monitor(inh_voltage_monitor, name="inh_voltage")
        spikes = {}
        for layer in set(network.layers):
            spikes[layer] = Monitor(
                network.layers[layer],
                state_vars=["s"],
                time=int(self.time / self.dt),
                device=device,
            )
            network.add_monitor(spikes[layer], name="%s_spikes" % layer)

        voltages = {}
        for layer in set(network.layers) - {"X"}:
            voltages[layer] = Monitor(
                network.layers[layer],
                state_vars=["v"],
                time=int(self.time / self.dt),
                device=device,
            )
            network.add_monitor(voltages[layer], name="%s_voltages" % layer)

        inpt_ims, inpt_axes = None, None
        spike_ims, spike_axes = None, None
        weigths_im = None
        assigns_im = None
        perf_ax = None
        voltage_axes, voltage_ims = None, None
        print("\nBegin training.\n")
        start = t()
        for epoch in range(self.n_epochs):
            labels = []

            if epoch % self.progress_interval == 0:
                print(
                    "Progress: %d / %d (%.4f seconds)"
                    % (epoch, self.n_epochs, t() - start)
                )
                start = t()

            dataloader = torch.utils.data.DataLoader(
                train_dataset,
                batch_size=1,
                shuffle=True,
                num_workers=self._workers_init(),
                pin_memory=self._gpu_init(),
            )
            for step, batch in enumerate(tqdm(dataloader)):
                if step > self.n_train:
                    break
                inputs = {
                    "X": batch["encoded_image"].view(
                        int(self.time / self.dt), 1, 1, 28, 28
                    )
                }
                if self.gpu:
                    inputs = {k: v.cuda() for k, v in inputs.item()}
                if step % self.update_interval == 0 and step > 0:
                    label_tensor = torch.tensor(labels, device=device)

                    all_activity_pred = all_activity(
                        spikes=spike_record,
                        assignments=assignments,
                        n_labels=n_classes,
                    )
                    proportion_pred = proportion_weighting(
                        spikes=spike_record,
                        assignments=assignments,
                        proportions=proportions,
                        n_labels=n_classes,
                    )

                    CompAcc(accuracy, label_tensor, all_activity_pred, proportion_pred)

                    assignments, proportions, rates = assign_labels(
                        spikes=spike_record,
                        labels=label_tensor,
                        n_labels=n_classes,
                        rates=rates,
                    )
                    labels = []
                labels.append(batch["label"])
                network.run(inputs=inputs, time=self.time)

                exc_voltages = exc_voltage_monitor.get("v")
                inh_voltages = inh_voltage_monitor.get("v")

                spike_record[step % self._train_init()] = (
                    spikes["Ae"].get("s").squeeze()
                )

                if self.plot:
                    image = batch["image"].view(28, 28)
                    inpt = inputs["X"].view(self.time, 784).sum(0).view(28, 28)
                    input_exc_weights = network.connections[("X", "Ae")].w
                    square_weights = get_square_weights(
                        input_exc_weights.view(784, self.n_neurons),
                        n_sqrt,
                        28,
                    )
                    square_assignments = get_square_assignments(assignments, n_sqrt)
                    spikes_ = {layer: spikes[layer].get("s") for layer in spikes}
                    voltages = {"Ae": exc_voltages, "Ai": inh_voltages}
                    inpt_axes, inpt_ims = plot_input(
                        image, inpt, label=batch["label"], axes=inpt_axes, ims=inpt_ims
                    )
                    spike_ims, spike_axes = plot_spikes(
                        spikes_, ims=spike_ims, axes=spike_axes
                    )
                    weights_im = plot_weights(square_weights, im=weights_im)
                    assigns_im = plot_assignments(square_assignments, im=assigns_im)
                    perf_ax = plot_performance(
                        accuracy, x_scale=self.update_interval, ax=perf_ax
                    )
                    voltage_ims, voltage_axes = plot_voltages(
                        voltages, ims=voltage_ims, axes=voltage_axes, plot_type="line"
                    )
                    plt.pause(1e-8)
                network.reset_state_variables()
        print(
            "Progress: %d / %d (%.4f seconds)" % (epoch + 1, self.n_epochs, t() - start)
        )
        print("Training complete.\n")

        test_dataset = MNIST(
            PoissonEncoder(time=self.time, dt=self.dt),
            None,
            root=os.path.join("..", "..", "data", "MNIST"),
            download=True,
            train=False,
            transform=transforms.Compose(
                [transforms.ToTensor(), transforms.Lambda(lambda x: x * self.intensity)]
            ),
        )
        accuracy = {"all": 0, "proportion": 0}
        spike_record = torch.zeros(
            (1, int(self.time / self.dt), self.n_neurons), device=device
        )
        print("\nBegin Testing\n")
        network.train(mode=False)
        start = t()

        pbar = tqdm(total=self.n_test)
        for step, batch in enumerate(test_dataset):
            if step >= self.n_test:
                break
            inputs = {
                "X": batch["encoded_image"].view(int(self.time / self.dt), 1, 1, 28, 28)
            }
            if self.gpu:
                inputs = {k: v.cuda() for k, v in inputs.items()}

            network.run(inputs=inputs, time=self.time)
            spike_record[0] = spikes["Ae"].get("s").squeeze()

            label_tensor = torch.tensor(batch["label"], device=device)

            all_activity_pred = all_activity(
                spikes=spike_record, assignments=assignments, n_labels=n_classes
            )
            proportion_pred = proportion_weighting(
                spikes=spike_record,
                assignments=assignments,
                porportions=proportions,
                n_labels=n_classes,
            )
            accuracy["all"] += float(
                torch.sum(label_tensor.long() == all_activity_pred).item()
            )
            accuracy["proportion"] += float(
                torch.sum(label_tensor.long() == proportion_pred).item()
            )
            network.reset_state_variables()
            pbar.set_description_str("Testing progress: ")
            pbar.update()
        print("\nAll activity accuracy: %.2f" % (accuracy["all"] / self.n_test))
        print(
            "Proportion weighting accuracy: %.2f \n"
            % (accuracy["proportion"] / self.n_test)
        )

        print(
            "Progress: %d / %d (%.4f seconds)" % (epoch + 1, self.n_epochs, t() - start)
        )
        print("Testing complete.\n")
