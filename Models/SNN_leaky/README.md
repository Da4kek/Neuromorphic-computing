## Basics of Leaky-integrate and fire neuronal model

Spiking neural networks are brain-inspired machine learning algorithms with merits such as biological plausibility and unsupervised learning capability.

*SNN uses spiking neurons primarily of the leaky-integrate and fire type, which exchange information via spikes.*

### The gap between ANN and SNN:
we want to establish a connection between ANN and SNN, in terms of the sources of inspiration for artificial intelligence, which is Brain science and cognitive neuroscience. we believe that ANN, the most powerful AI in real applications and SNN, the most biologically plausible technology, can learn from each other.     
The biological neural model's complex dynamics and non-differentiable operations make SNN lack scalable training algorithms. We have to focus on the mechanism of transferring trained weights of DNN into SNN. 

### Single-compartment model
If a neuron is "electrotonically compact", it may be treated as a single "compartment". Such a compartment is characterized by a single membrane potential, membrane capacity and membrane resistance.


**Membrane resistance and equilibrium potential:**
* The input current determines the equilibrium potential.
* the equilibrium potential is the potential needed to drive an outward resistance current equal to the inward input current.
* it therefore depends on the membrane resistance.
* the membrane potential moves towards the equilibrium potential.
* the membrane potential may not reach the equilibrium potential, because the input current may not remain constant for long enough.
* If reached, the membrane potential is  "at equilibrium".

**Membrane capacitance and membrane time-constant:**
* The membrane cacpacitance determins how much current is needed to change the membrane potential.
* If large, a given input current changes the membrane potential only slowly.
* If small, a given input current changes the membrane potential quickly.
* the membrane time-constant is the time it takes the membrane to move approximately 1/3 of the way towards to equilibrium potential.
* the membrane time-constant is proportional to membrane resistance and membrane capacitance 
 $$τm = Rm Cm$$

**SCM generalization:**
* The single-compartment model can be solved iteratively for arbitrary input currents.eg:electrode or synaptic currents.
* To do so, we divive time into short intervals, so that input current may be considered piecewise constant.
* we can now understand the "leaky" and "integrator" parts of the leak-integrate and fire model.
* it *Integrates* because the membrane voltage sums over input currents.
* its *leaky* because of leak conductance $gL =1/rm$ dissipates the membrane potential over time.

### Spike mechanism of LIF model:
To complete the transition from SCM to LIF model, we add a mechanism for generating spikes or action potentials. This mechanism is artificial and ignores the biophysical basis of action potentials. It still offers a useful approximation of neuronal activity.
Computational neuroscience has provided a new idea for unsupervised learning mechanisms. Spiking time dependent plasticity is a temporally asymmetric form of hebbian learning and is the most widely used unsupervised learning mechanism is SNNs. In the temporal dimension, the relation between the presynaptic action potential, and the postsynaptic action potential regulates the neuron's weights, which is a feature unique to SNNs.

### LIF neuron model:
**LIF neuron's dynamic properties:**
1. The lapicque model is considered the earliest form of the LIF model and it becomes the LIF model after adding an attenuation term. The LIF model is one the most popularly used models for analyzing the nervous system's behavior. Unlike the neuron models used for computing, some neuron models have also been created and applied to simulate nreal neuron propagation potentials. The HH model was proposed by analyzing the electric current flow through the surface membrane. We call it a simulation-oriented neuron model. The Izhikevich model is a simplifications of the HH model based on the theory of dynamic systems.
2. The LIF model can be modeled as a circuit composed of resistor and a capacitor in parallel, which respectively respresent the leakage and capacitance of the membrane. The integrate and fire neuron model is described by the dynamics of the neuron's membrane potential (MP), V(t),
$$Cm dV (t)/dt + (V (t) − V0 )/Rm = Iinj ,$$ 

**Linear Leaky-integrate-and-fire model:**
Once the membrane potential reaches the spiking threshold, an action potential will be exceeded. Then the membrane potential will be reset: "Reset-to-Zero" used.
```V (t) = {
H(t) · (1 − S(t))
H(t) · (1 − S(t)) + (H(t) − Vreset) · S(t) }
```
The LIF neuron model with "Linear reset" is named Linear LIF model.
