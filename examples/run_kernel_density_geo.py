
def main():
    from complex_systems.spatial.kernel_density_geo import kernel_density_geo
    import scipy.stats as stats
    import pylab as plt
    from matplotlib.pyplot import imshow
    import numpy as np
    
    X_data = stats.norm.rvs(loc=3,scale=1,size=(2000,1))
    Y_data = stats.norm.rvs(loc=2,scale=1,size=(2000,1))

    coor,Z = kernel_density_geo(X_data, Y_data,bin_size_x=100, bin_size_y=100)
    plt.figure()
    plt.imshow(Z, interpolation="nearest")
    plt.show()

if __name__ == '__main__':
    main()