import os
import matplotlib.pyplot as plt
import re
import csv

inf = os.walk('.')
dirs = [x[0] for x in inf]

flux_dirs = {}
for d in dirs:
    match = re.search(r'^\./R([0-9]{4})$', d)
    if match:
        with open(os.path.join(d,'Fluxes.txt'), 'rb') as csvfile:
            dat = csv.reader(csvfile, delimiter=' ', quotechar='|')
            t = []
            qs = []
            for row in dat:
                row = filter(None, row)
                t.append(row[0])
                qs.append(row[3])

            plt.plot(t, qs, linewidth=2.0)

            flux_dirs.update({int(match.group(1)): [t,qs]})
plt.show()