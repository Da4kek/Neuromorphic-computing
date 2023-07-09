import numpy as np


class HH:
    class Gate:
        alpha, beta, state = 0, 0, 0

        def update(self, deltaT):
            alphastate = self.alpha * (1 - self.state)
            betastate = self.beta * self.state
            self.state += deltaT * (alphastate - betastate)

        def setInfstate(self):
            self.state = self.alpha / (self.alpha + self.beta)

    ENa, EK, EKleak = 115, -12, 10.6
    gNa, gK, gKleak = 120, 36, 0.3
    m, n, h = Gate(), Gate(), Gate()
    Cm = 1

    def __init__(self, startingVoltage=0):
        self.Vm = startingVoltage
        self.UpdateGateConstant(startingVoltage)
        self.m.setInfstate()
        self.n.setInfstate()
        self.n.setInfstate()

    def UpdateGateConstant(self, Vm):
        self.n.alpha = 0.01 * ((10 - Vm) / (np.exp((10 - Vm) / 10) - 1))
        self.n.beta = 0.125 * np.exp(-Vm / 80)
        self.m.alpha = 0.1 * ((25 - Vm) / (np.exp((25 - Vm) / 10) - 1))
        self.m.beta = 4 * np.exp(-Vm / 18)
        self.h.alpha = 0.07 * np.exp(-Vm / 20)
        self.h.beta = 1 / (np.exp((30 - Vm) / 10) + 1)

    def Updatecellvolt(self, stimuluscurrent, deltaT):
        self.INa = (
            np.power(self.m.state, 3) * self.gNa * self.h.state * (self.Vm - self.ENa)
        )
        self.IK = np.power(self.n.state, 4) * self.gK * (self.Vm - self.EK)
        self.IKleak = self.gKleak * (self.Vm - self.EKleak)
        Isum = stimuluscurrent - self.INa - self.IK - self.IKleak
        self.Vm += deltaT * Isum / self.Cm

    def UpdateGateState(self, deltaT):
        self.n.update(deltaT)
        self.m.update(deltaT)
        self.h.update(deltaT)

    def iterator(self, stimulusCurr, deltaT):
        self.UpdateGateConstant(self.Vm)
        self.Updatecellvolt(stimulusCurr, deltaT)
        self.UpdateGateState(deltaT)
