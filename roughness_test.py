import numpy as np
from scipy import signal

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm

#Based upon the litterature here:
    #https://www.sciencedirect.com/topics/engineering/equivalent-sand-grain-roughness
    #https://www.sciencedirect.com/topics/engineering/surface-height-distribution#:~:text=Skewness%20is%20a%20measure%20of,surface%20height%20about%20the%20mean.


def get_simple_roughness(block_width, gap_width, block_height):
    d = np.linspace(0, (block_width+gap_width)*2, 500, endpoint=False)
    a = (block_height/2)*signal.square((2*np.pi * d)/(block_width+gap_width), 
                                       duty=((block_width)/(block_width+gap_width)))+(block_height/2)
    '''
    plt.plot(d, a)
    plt.ylim(0, block_height*1.01)
    plt.show()
    '''
    Rrms = np.std(a)
    Rsk = (1/(Rrms**3))*np.mean(a**3)
    ks = (4.43*Rrms)*((1 + Rsk)**1.37) #Sand grain roughness
    
    z0 = ks/32.8 #Aerodynamic roughness
    
    return np.array([ks, z0]), a

block_width = gap_width = 0.2
block_height = 0.01

roughness, sig = get_simple_roughness(block_width, gap_width, block_height)

gap_width_ratio = np.linspace(0.1, 0.9, 100)
block_height = np.linspace(0.2, 1, 100)

mesh = np.stack(np.meshgrid(gap_width_ratio, block_height), axis=2)
space = mesh.reshape(-1, 2)

def np_fun(x):
    block_width = x[0]
    gap_width = 1-x[0]
    block_height = x[1]
    
    roughness, sig = get_simple_roughness(block_width, gap_width, block_height)
    
    return roughness

results = np.apply_along_axis(np_fun, 1, space).reshape(len(block_height),
                                                        len(gap_width_ratio), 
                                                        2)
fig, ax = plt.subplots()

cmap = cm.viridis
norm = matplotlib.colors.LogNorm(np.min(results[:, :, 0]), np.max(results[:, :, 0]))


im = ax.imshow(results[:, :, 0], interpolation='bicubic', origin='lower',
                cmap=cmap, norm=norm, extent=(0.1, 0.9, 0.2, 1),
                )
cs = ax.contour(np.log(results[:, :, 0]), levels=np.log([5, 10, 20, 40, 80]),
                linewidths=1, extent=(0.1, 0.9, 0.2, 1), colors='k',)

levels = cs.levels
fmt = {}
for level in levels:
    fmt[level] = '{}'.format(np.format_float_positional(np.exp(level), precision=0))

fig.draw_without_rendering() 
ax.clabel(cs, inline=True, fontsize=15, fmt=fmt)

ax.set_xlim(0.1, 0.9)
fig.colorbar(im)