import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


#data placeholder
count = 100
data = pd.DataFrame({"Red": np.random.normal(20, 20, count), "Blue": np.random.normal(170, 20, count)})
#scale x-axis for plot
x_axis = np.arange(-60, 260, 0.1)
bins = 20

blue_mean = data["Blue"].mean()
blue_std = data["Blue"].std()
actual_blue= 170    # placeholder

red_mean = data["Red"].mean()
red_std = data["Red"].std()
actual_red= 20    # placeholder

#normal distributions
plt.plot(x_axis, norm.pdf(x_axis, loc=blue_mean, scale=blue_std), color='b')
plt.axvline(x=actual_blue, color='b', linestyle='dashed', linewidth=1)
plt.plot(x_axis, norm.pdf(x_axis, loc=red_mean, scale=red_std), color='r')
plt.axvline(x=actual_red, color='r', linestyle='dashed', linewidth=1)
plt.figure()


#histogram plot
plt.axvline(x=actual_blue, color='b', linestyle='dashed', linewidth=1)
plt.axvline(x=actual_red, color='r', linestyle='dashed', linewidth=1)
plt.hist(data["Blue"], bins=bins, color='b', alpha=0.3, edgecolor='black')
plt.hist(data["Red"], bins=bins, color='r', alpha=0.3, edgecolor='black')
plt.figure()

#combined plot
plt.hist(data["Blue"], bins=bins, color='b', density=True, alpha=0.3, edgecolor='black')
plt.hist(data["Red"], bins=bins, color='r', density=True, alpha=0.3, edgecolor='black')
plt.plot(x_axis, norm.pdf(x_axis, loc=blue_mean, scale=blue_std), color='b', linewidth=1)
plt.axvline(x=actual_blue, color='b', linestyle='dashed', linewidth=1)
plt.plot(x_axis, norm.pdf(x_axis, loc=red_mean, scale=red_std), color='r', linewidth=1)
plt.axvline(x=actual_red, color='r', linestyle='dashed', linewidth=1)
plt.show()
