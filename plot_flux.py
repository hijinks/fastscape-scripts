import os
import numpy
import matplotlib.pyplot as plt
import re
import csv
import time

inf = os.walk('.')
dirs = [x[0] for x in inf]

flux_dirs = {}

x_sample = 5
plot = 0
data_dir = './data'

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

            if plot:
                plt.plot(t, qs, linewidth=2.0)

            flux_dirs.update({int(match.group(1)): [t,qs]})

new_csv = str(time.time())+'_flux.csv'
new_csv_path = os.path.join(data_dir, new_csv)
f = open(new_csv_path, 'wt')
writer = csv.writer(f)
writer.writerow(['Catchment', 'Flux_(m^3/yr)'])


for fd in flux_dirs:
    qs = flux_dirs[fd][1]
    qs_sample = map(float, qs[-x_sample:])
    mean_qs = numpy.mean(qs_sample[-x_sample:])
    writer.writerow([fd, mean_qs])

f.close()

if plot:
    plt.show()