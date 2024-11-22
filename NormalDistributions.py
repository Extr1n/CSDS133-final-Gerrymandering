import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# data = pd.read_csv('data.csv')
# mean = data['Column1'].mean()
# std = data['Column1'].std()

#scale x-axis for plot
x_axis = np.arange(00, 200, 0.1)

blue_mean = 50      # placeholder
blue_std = 20        # placeholder
actual_blue= 20    # placeholder

red_mean = 150      # placeholder
red_std = 20        # placeholder
actual_red= 170    # placeholder

plt.plot(x_axis, norm.pdf(x_axis, loc=blue_mean, scale=blue_std), color='b')
plt.axvline(x=actual_blue, color='b', linestyle='dashed', linewidth=1)
plt.plot(x_axis, norm.pdf(x_axis, loc=red_mean, scale=red_std), color='r')
plt.axvline(x=actual_red, color='r', linestyle='dashed', linewidth=1)
plt.show()
