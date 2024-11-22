import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# data = pd.read_csv('data.csv')
# mean = data['Column1'].mean()
# std = data['Column1'].std()

#scale x-axis for plot
x_axis = np.arange(00, 200, 0.1)

mean = 100      # placeholder
std = 20        # placeholder

actual_count= 20    # placeholder

plt.plot(x_axis, norm.pdf(x_axis, loc=mean, scale=std), color='b')
plt.axvline(x=actual_count, color='k', linestyle='dashed', linewidth=1)
plt.show()
