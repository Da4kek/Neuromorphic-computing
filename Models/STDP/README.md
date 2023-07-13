## Unsupervised learning of digit recognition using Spike-Timing-dependent plasticity
 
Two things to keep in mind:
* Need to have a good understanding of the available neuronal processing units and mechanisms
* Need to gain a better understanding of how those mechanisms are combined to build functioning systems.

`A SNN for digit recognition which is based on mechanisms with increased biological plausibility. Conductance-based instead of current-based synapses, spike-timing-dependent plasticity with time-dependent weight change, layeral inhibition, and an adaptive spiking threshold.`

**Model used: Leaky integrate-and-fire model**
*The membrane voltage V is described by
$$τdV/dt=(Erest−V)Cge(Eexc−V)Cgi(Einh−V)$$

**Spike-timing-dependent plasticity**:
STDP is a biological process that adjusts the strength of connections between neurons in the brain. The process adjusts the connection strengthsbased on the relative timing of a particular neuron's output and input action potentials or spikes.
The STDP process partially explains the activity-dependent development of nervous systems, especially with regard to **Long-term Potential** and **Long-term depression**.
The term "spike timing dependent plasticity" refers to the observation that the precise timing of spikes significantly affects the sign and magnitude of synaptic plasticity.
A presynaptic spike preceding a post synaptic spike within a narrow time window leads to Long-term potential. If the order is reversed, long-term depression results.
In sense STDP has been considered as a possible first law of synaptic plasticity.
Synaptic plasticity is induced by a variety of receptor-generated second messengers, which in turn activate kinases, phosphatases and other downstream targets.

#### Points to ponder:
* STDP refers to a form of associative psynaptic plasticity in which the termporal order of the presynaptic and postsynaptic action potentials determines the direction of plasticity.
* Long term potential is induced if the presynaptic spike precedes the postsynaptic spike (pre -> post).
* If the postsynaptic spike happens before the presynaptic spike long term depression is induced (post -> pre).
* Short intervals produce maximal plasticity, while longer intervals produce little or no change in synaptic strength.
* The psychologist Donald Hebb postulated that if a presynaptic neuron "repeatedly or presistently takes part in firing" a postsynaptic  neuron the synapse between them would be potentiated.
* Not all Synapses seem to undergo STDP in response to the pairing of single pre and post synaptic action potentials.
* The shape of the STDP function is highly variable.The peak or total area of the LTP and LTD windows are dependent not only on the types of synapses being examined