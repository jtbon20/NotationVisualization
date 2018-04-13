import os.path
from numpy import array, ma
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def visualize(x, dta, size, filename):
    fig = plt.figure(figsize=(325, 10), dpi=200)
    plt.plot(x,dta,c="black", lw=.5)
    size = ( 30*  size)**2

    plt.scatter(x,dta, c = dta , s = size)
    plt.axis('off')

    plt.savefig(os.path.basename(filename) + '.svg', bbox_inches='tight')
    plt.close();
