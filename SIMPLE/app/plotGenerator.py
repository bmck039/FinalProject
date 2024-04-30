import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

import pandas as pd
import glob

import os.path

extension = 'csv'

path = os.path.join("./output/", '*.{}'.format(extension))
files = glob.glob(path)

winrates = []
scores = []
winRateStdDevs = []
names = []
xAxes = []

dfs = []

for i in range(len(files)):
    file = files[i]
    df = pd.read_csv(file, header=None)
    fileName = file.split("/")[2]
    combinedName = fileName.split(".")[0]
    splitName = reversed(combinedName.split("VS"))
    name = " vs ".join(splitName)
    means = df.mean()
    stds = df.std()

    winrates.append(means[0])
    winRateStdDevs.append(np.sqrt(means[0] * (1 - means[0]) / df.shape[0]))
    xAxes.append(i)
    scores.append(means[1])
    names.append(name)
    dfs.append(df[1])

plt.boxplot(dfs, labels=names)

print(names)


plt.savefig("./output/scores.png")
plt.clf()

ax = plt.gca()
ax.set_ylim([0, 1])

plt.scatter(xAxes, winrates)

plt.errorbar(xAxes, winrates, yerr = winRateStdDevs, capsize=5, fmt='none')

ax.xaxis.set_major_locator(ticker.FixedLocator(xAxes))

ax.set_xticklabels(names)

plt.savefig("./output/winrates.png")


results = zip(names, winrates)
print("winrates:", list(results))

results = zip(names, scores)
print("score difference:", list(results))