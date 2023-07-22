## Introduction to Spike Encoding:

The brain trades in the global currency of the spike.   
the goal is to build a spiking neural network, it makes sense to use spikes at the input too. Although it is quite common to use non-spiking inputs, while encoding things to remember: Spikes, Sparsity and Static suppression.

Encoding algorithms for spike generation can be classified according to two main categories:
* Rate coding
* Temporal coding

1. Spikes: Biological neurons process and communicate via spikes, which are electrical impulses of approximately 100 mV in amplitude. Many computational models of neurons simplify this voltage burst to a discrete, single-bit event a 1 or a 0. This is far simpler to represent in hardware than a high precision value.
2. Sparsity: Neurons spend most of their time at rest, silencing most activations to zero at any given time. Not only are sparse vectors/tensors cheap to store, but say we need to multiply sparse activations with synaptic weights. If most values are multiplied by 0, then we dont need to read many of the network parameters from memory. This means neuromorphic hardware can be extremely efficient.
3. Static-suppression: The sensory periphery only processes information when there is new information to process. Each pixel of information responds to change in different properties. Conventional signal processing requires all channels/pixels to adhere to global sampling/shutter rate. 
   

![](https://github.com/jeshraghian/snntorch/blob/master/docs/_static/img/examples/tutorial1/3s.png?raw=true)

SNNs are made to exploit the time-varying data. There are two options for using a dataset with SNNs:
1. Repeatedly pass the same training sample to the network at each time step. This is like converting the dataset into a static unchanged video. Each element of X can take a high precision value normalized between 0 and 1.
2. Convert the input into a spike train of sequence length N, where each feature takes on a discrete value (0,1). In this case, the data is converted into a time-varying sequence of spikes that features a relation to the original data.

**Some Spike Encoding techniques:**
1. Rate coding: uses input features to determine spiking frequency.
2. Latency coding: uses input features to determine spike timing.
3. Delta modulation: uses the temporal change of input features to generate spikes.

The Data is repeated along the first dimension for rate coding, ie, time-first before spike encoding.

In Rate Coding, the input features are used to parameterize a binomial distribution, which is then sampled from to determine whether or not a spike occurs.

In Latency Coding, each feature corresponds to a single spike. The intensity of the feature determines how fast the spike occurs. Options for linear or logarithmic firing times are available.

### Rate coding
Widely adopted for ANNs due to its ease and robustness, rate coding employs a mechanism for information representation based on the number of spikes per unit time.     
**Poisson Rate:** 
$$Pn(Δt)=((rΔt)n/n!) e−rΔt$$
The algorithm can be performed through the following steps:
1. Definition of the time interval del t in which to generate the spike train.
2. Generation of a sequence of random numbers between 0 and 1.
3. From t =0, definition of the spike times $ti$ as:
   $$ti=ti−1+ISIi  fori≥1$$
   where
   $$ISIi=−log(1−xi)/r$$
4. Generation of a spike at each time $ti$ until $ti > del t$

### Delta Modulation:
There are theories that the retina is adaptive: it will only process information when there is something new to process. If there is no change in your field of view, then your photoreceptor cells are less prone to firing.   
Delta modulation is based on event-driven spiking.






### Summary:

The idea of rate coding is actually quite controversial. Although we are fairly confident rate coding takes place at our sensory periphery, we are not convinced that the cortex globally encodes information as spike rates. Reasons:
1. Power consumption
2. Reaction response times

Rate coding is almost certainly working in conjunction with other encoding schemes in the brain. 
