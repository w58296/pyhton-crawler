import numpy as np
import matplotlib.pyplot as plt
import math
import matplotlib;
matplotlib.use('TkAgg')

#课上实验
def getTenured(data):
    rank = data['rank']
    years = data['years']

    if rank == 'professor' and years > 1:
        data['tenured'] = 'yes'
    elif rank == 'associate prof' or rank == 'assistant prof':
        if years > 6:
            data['tenured'] = 'yes'
    else:
        data['tenured'] = 'no'

#正态分布
def normal_distribution(u, sigma):
    sig = math.sqrt(sigma)
    x = np.linspace(u-3*sig, u+3*sig, 50)
    y_sig = np.exp(-(x-u)**2/(2*sig**2))/(math.sqrt(2*math.pi)*sig)
    print(x)
    print('='*20)
    print(y_sig)
    plt.figure()
    plt.plot(x, y_sig, 'r-', linewidth=2)
    plt.grid(True)
    plt.show()

def poisson_distribution():
    x = np.random.poisson(lam=5, size=10000)
    pillar = 15
    plt.figure('lalala', figsize=(7, 7), dpi=100, facecolor='y', edgecolor='r')
    #x为数据，pillar为条形数
    a = plt.hist(x, pillar, color='g')
    print(x)
    print(a)
    plt.plot(a[1][0:pillar], a[0], 'r')
    plt.grid(True)
    plt.show()


def possion_distribution_2(lam):
    x = np.arange(0, 100, 1)
    y = [math.pow(lam, i)/math.factorial(i)*math.exp(-lam) for i in x]
    plt.plot(x, y, 'r-', linewidth=2)
    plt.grid(True)
    plt.show()

def two_point_distribution(p):
    x = [0, 1]
    y = [p, 1-p]
    plt.plot(x, y, 'ro')
    plt.grid(True)
    plt.show()

def binomial_distribution(n, p):
    x = np.random.binomial(n, p, 10000)
    pillar = 10
    # x为数据，pillar为条形数
    a = plt.hist(x, pillar, color='g')
    print(x)
    print(a)
    plt.plot(a[1][0:pillar], a[0], 'r')
    plt.grid(True)
    plt.show()

def binomial_distribution_2(n, p):
    x = range(0, n+1)
    y = [math.factorial(n)/(math.factorial(i)*math.factorial(n-i))*math.pow(p, i)*math.pow(1-p, n-i)for i in x]
    plt.plot(x, y, 'r-', linewidth=2)
    plt.grid()
    plt.show()

def geometric_distribution(p):
    x = np.random.geometric(p, 10000)
    pillar = 10
    a = plt.hist(x, pillar, color='g')
    plt.plot(a[1][0:pillar], a[0], 'r')
    plt.grid(True)
    plt.show()

def geometric_distribution_2(p):
    x = range(1, 100)
    y = [math.pow(1-p, i-1)*p for i in x]
    plt.plot(x, y, 'r-', linewidth=2)
    plt.grid()
    plt.show()

def uniform_distribution(a, b):
    x = np.random.uniform(a, b, 100000)
    pillar = 10
    a = plt.hist(x, pillar, color='g')
    plt.plot(a[1][0:pillar], a[0], 'r')
    plt.grid(True)
    plt.show()

def uniform_distribution_2(a, b):
    x = range(a, b+1)
    y = [1/(b-a)]*len(x)
    plt.plot(x, y, 'r-', linewidth=2)
    plt.grid()
    plt.show()

def exponetial_distribution(lam):
    x = np.random.exponential(lam, 10000)


def exponetial_distribution_2(lam):
    x = range(1, 100)
    y = [lam*math.exp(-lam*i)for i in x]
    plt.plot(x, y, 'r-', linewidth=2)
    plt.grid()
    plt.show()





if __name__ == '__main__':
    print('___main___')

