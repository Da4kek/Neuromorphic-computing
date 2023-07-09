# Neuromorphic-computing

`This repo contains implementation of spiking neural network algorithms and neuromorphic computing notes.`

### Neuromorphic computers
Neuromorphic computers have the following characteristics.
* **Collocated processing and memory.** The brain-inspired neuromorphic computer chips process and store data together on each individual neuron instead of having separate areas for each. By collocating processing and memory, neural net processors and other neuromorphic processors avoid the von Neumann bottleneck and can have both high performance and low energy consumption at the same time.
* **Massively parallel.**  Neuromorphic chips, such as Intel Lab's Loihi 2, can have up to one million neurons. Each neuron operates on different functions simultaneously. In theory, this lets neuromorphic computers perform as many functions at one time as there are neurons. This type of parallel functioning mimics stochastic noise, which is the seemingly random firings of neurons in the brain. Neuromorphic computers are designed to process this stochastic noise better than traditional computers.
* **Inherently scalable.** Neuromorphic computers do not have traditional roadblocks to scalability. To run larger networks, users add more neuromorphic chips, which increases the number of active neurons.
* **High in adaptability and plasticity.** Like humans, neuromorphic computers are designed to be flexible to changing stimuli from the outside world. In the spiking neural network -- or SNN -- architecture, each synapse is assigned a voltage output and adjusts this output based on its task. SNNs are designed evolve different connections in response to potential synaptic delays and a neuron's voltage threshold. With increased plasticity, researchers hope neuromorphic computers will learn, solve novel problems and adapt to new environments quickly.
* **Fault tolerance.** Neuromorphic computers are highly fault tolerant. Like the human brain, information is held in multiple places, meaning the failure of one component does not prevent the computer from functioning.

### Spiking Neural Networks

ANNs and SNNs are different in terms of their neuron models. ANNs typically use computation units, such as sigmoid, rectified linear unit or tanh and have no memory, whereas SNNs use a non differentiable neuron model and have memory such as Leaky integrate and fire. However, simulation of large scale SNN models on classical von neumann architectures demands a large amount of time and power. Therefore, high-speed and low-power hardware implementation of SNNs is essential. Neuromorphic platforms, which are based on event-driven computation, provide an attractive solution to these problems.

![](https://mitp.silverchair-cdn.com/mitp/content_public/journal/neco/34/6/10.1162_neco_a_01499/1/m_neco_a_01499.figure.01.jpeg?Expires=1691753035&Signature=0nV2oZLk0yH1thtXtYrbWK5QV45VTqU6Mr-Vlhtfx~yEXiCg8JGIMHswRKvkNc1oZIhN3F9M6EambraBwkTyreToZ~ezQiKwpvBNtdoM5YltfJgQogMil9LQAyrVWdceI-NIIscpD~zCRs2bf~xXN2aPgPprrzf5Aghb8fE~HSh4sPS-1w3roQr0MRaBl-VAlg6-yzky3Kv82Rks6CCVU1~2TPTe0oay3d6KTbIFZ-yI5oeBwmOTZhD-EobFfq0~bjl03VrTwvxDivg4AZbCswhyI93NrZlX2wP6dK~dLqC0DMJcLkw0cYoWzKzuPtywNCcC86iUbOXFKKVwJUeeLg__&Key-Pair-Id=APKAIE5G5CRDK6RD3PGA)

#### Spiking Neuron model

A spiking neuron has a similar structure to that of an ANN neuron but shows different behavior. Different models differ not only on which biological characteristics of real neurons they can reproduce but also based on their computational complexity.

##### Hodgkin-Huxley Model

The HH model is the first biological model of a spiking neuron that describes how action potentials in the neuron are initiated and propagated. It shows the mathematical description of electric current through the membrane potential, which can be calculated as
$$I=Cdvdt+GNam3h(V−VNa)+Gkn4(V−Vk)+GL(V−VL)$$,
The HH model,the most biologically plausible spiking neuron model, accurately capture the dynamics of many real neurons. However, it is too computationally expensive due to the feedback loop initiated and the differential equations to be calculated continuously.

##### Izhikevich Model
This biologically plausible spiking neuron model. This two-dimensional model can reproduce a large variety of spiking dynamics. The model can be described mathematically as
$$dv(t)dt=0.04υ2+5υ+140−u+I(t),$$
$$du(t)dt=a(bυ−u),$$
$$υ(υ>υth)=candu(υ>υth)=u+d.$$
Izhikevich is a 2D spiking neural model that offers a good trade-off between biological plausibility and computational efficiency. It cna produce various spiking dynamics.

##### Integrate and Fire Model
Integrate-and-fire, one of the simple models, integrates input spikes to membrane potential, if it reaches the defined threshold, an output spike is generated, and membrane potential changes to a resting state. This model can be determined by
$$Cm dv/dt=I(t),ν←vrest$$ $$when$$  $$ν≥νth,$$
This model is the lowest one in terms of computational power consumption. The leaky integrate-and-fire model, an important type of IF neuron model, adds a leak to the membrane potential. This model is defined by the following equation,
$$τleakdvdt=[υ(t)−υrest]+rmI(t),υ←υrest$$ $$when$$ $$υ≥υth,$$
The LIF model is one of the widely used spiking neuron models because of its very low computational cost, its accuracy in terms of replicating the spiking behavior of biological neurons and its speed in simulating.
*There are also more complex types of IF model such as exponential integrate-and-fire, quadratic integrate-and-fire, and adaptive exponential integrate-and-fire.*

##### Spike Response Model
The spike response model is a bio-inspired spiking neuron that describes more precisely the effect of input spikes on the membrane potential. Similar to the LIF model, and SRM neuron generates spikes whenever its internal membrane potential reaches the threshold. However, in contrast to LIF, it includes a function dependent on reset and refractory periods.
Moreover, unlike the LIF model that uses differential equations for the voltage potential, the SRM is formulated using response kernels. The SRM model mathematical formulation is expressed as,
$$υ(t)=η(t−tˆ)+\int_∞^∞ κ(t−tˆ,s)I(t−s)ds,$$
The 1D spike response model is simpler than other models on the level of the spike generation mechanism. It offers low computational cost. However it provides poor biological plausibility compared with the Hodgkin and Huxley model.