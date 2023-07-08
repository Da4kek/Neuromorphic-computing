import matplotlib
import matplotlib.pyplot as plt
from snntorch import spikeplot as splt


def Plotcurrentspike(
    cur, mem, spk, thr_line=False, vline=False, title=False, y_lim=1.25, y_lim2=1.25
):
    fig, ax = plt.subplots(
        3, figsize=(8, 6), sharex=True, gridspec_kw={"height_ratios": [1, 1, 0.4]}
    )

    ax[0].plot(cur, c="tab:orange")
    ax[0].set_ylim([0, y_lim])
    ax[0].set_xlim([0, 200])
    ax[0].set_ylabel("Input current")
    if title:
        ax[0].set_title(title)

    ax[1].plot(mem)
    ax[1].set_ylim([0, y_lim2])
    ax[1].set_ylabel("Membrane potential")
    if thr_line:
        ax[1].axhline(
            y=thr_line, alpha=0.25, linestyle="dashed", c="black", linewidth=2
        )
    plt.xlabel("Time step")

    splt.raster(spk, ax[2], s=400, c="black", marker="|")
    if vline:
        ax[2].axvline(
            x=vline,
            ymin=0,
            ymax=6.7,
            alpha=0.15,
            linestyle="dashed",
            c="black",
            linewidth=2,
            zorder=0,
        )
    plt.ylabel("output spikes")
    plt.yticks([])
    plt.show()


def PlotSNNspikes(spk_in, spk1_rec, spk2_rec, title, num_steps):
    fig, ax = plt.subplots(
        3, figsize=(8, 7), sharex=True, gridspec_kw={"height_ratios": [1, 1, 0.4]}
    )

    splt.raster(spk_in[:, 0], ax[0], s=0.03, c="black")
    ax[0].set_ylabel("Input Spikes")
    ax[0].set_title(title)

    splt.raster(spk1_rec.reshape(num_steps, -1), ax[1], s=0.05, c="black")
    ax[1].set_ylabel("Hidden Layer")

    splt.raster(spk2_rec.reshape(num_steps, -1), ax[2], c="black", marker="|")
    ax[2].set_ylabel("Output Spikes")
    ax[2].set_ylim([0, 10])

    plt.show()


def SpikeAnimate(spike_data):
    fig, ax = plt.subplots()
    anim = splt.animator((spike_data[:, 0] + spike_data[:, 1]), fig, ax)
    return anim
