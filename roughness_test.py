import numpy as np
from scipy import signal, stats
import matplotlib.pyplot as plt

#Based upon the litterature here:
    #https://www.sciencedirect.com/topics/engineering/equivalent-sand-grain-roughness

equal_space = 10
height = 30

d = np.linspace(0, equal_space*4, 2000, endpoint=False)
a = (height/2)*signal.square((np.pi * d)/equal_space)+(height/2)
plt.plot(d, a)
plt.ylim(-0.1, height*1.01)

rms = np.sqrt(np.mean(a**2))
skew = stats.skew(a)

sk = skew/(rms**3)
ks = 4.43*rms*(1 + sk)**1.37 #Sand grain roughness
z0 = ks/32.8 #Aerodynamic roughness