import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

import pandas as pd
import glob

extension = 'csv'
files = glob.glob('*.{}'.format(extension))

winrates = []
scores = []
winRateStdDevs = []
names = []
xAxes = []


for i in range(len(files)):
    file = files[i]
    df = pd.read_csv(file, header=None)
    combinedName = file.split(".")[0]
    splitName = reversed(combinedName.split("VS"))
    name = " vs ".join(splitName)
    means = df.mean()
    stds = df.std()

    winrates.append(means[0])
    winRateStdDevs = np.sqrt(means[0] * (1 - means[0]) / df.shape[0])
    xAxes.append(i)
    scores.append(means[1])
    names.append(name)

ax = plt.gca()
ax.set_ylim([0, 1])

plt.scatter(xAxes, winrates)

plt.errorbar(xAxes, winrates, yerr = winRateStdDevs, capsize=5)

ax.xaxis.set_major_locator(ticker.FixedLocator(xAxes))

ax.set_xticklabels(names)

plt.savefig("winrates.png")

plt.clf()

plt.boxplot(df[1], labels=names)

plt.savefig("scores.png")