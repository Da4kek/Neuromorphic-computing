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
* STDP is sensitive to the interspike interval (ISI)
* STDP refers to a form of associative psynaptic plasticity in which the termporal order of the presynaptic and postsynaptic action potentials determines the direction of plasticity.
* Long term potential is induced if the presynaptic spike precedes the postsynaptic spike (pre -> post).
* If the postsynaptic spike happens before the presynaptic spike long term depression is induced (post -> pre).
* Short intervals produce maximal plasticity, while longer intervals produce little or no change in synaptic strength.
* The psychologist Donald Hebb postulated that if a presynaptic neuron "repeatedly or presistently takes part in firing" a postsynaptic  neuron the synapse between them would be potentiated.
* Not all Synapses seem to undergo STDP in response to the pairing of single pre and post synaptic action potentials.
* The shape of the STDP function is highly variable.The peak or total area of the LTP and LTD windows are dependent not only on the types of synapses being examined, but on the exact induction protocol, pre and postsynaptic cell type and even on the position of the synapse along the dendritic arbor.
* The standard STDP function is based on isolated single pre- and postsynaptic spikes, and does not necessarily describe synaptic plasticity in response to more complex patterns of activity.

#### Linearity of STDP:

If, for instance, LTP was observed, STDP would be nonlinear and LTP would be dominant.under experimental conditions, it is possible to constrain the spike pattens to single isolated spikes, however in vivo data show that bursts of spikes or complex ongoing temporal patterns of spikes are commonly elicited in response to a given stimuli.Thus, in order to understand the computational role of STDP in vivo, it is necessary to address the issue of linearity or nonlinearity of STDP. It is clear that STDP is not strictly linear.

#### Mechanisms:

Two critical features of STDP must be accounted for at the mechanistic level:
1. **Order**. How can a synapse detect differences of a few milliseconds regarding the temporal order of presynaptci and postsynaptic spikes and account for the sharp discontinuity observed at approximately 0 ms ISIs?
1. **Interval**. Independently of the issue of temporal order, what are the mechanisms that allow synapses to be sensitive to the pre->post and post->pre intervals?

The mechanisms responsible for the interval sensitivityof the LTP component of STDP are generally accepted as being the same as those underlying associative LTP.

#### Timing

STDP is highly sensitive to the interval between the pre and postsynaptic spikes, however, the role of STDP in generating timed responses remains unclear. The original temporal interval used in the training is not effectively reproduced.As a result, STDP maintains the order of activation and favors early responses, but the patterns produced after STDP do not capture the temporal structure of the training stimuli.