import os
import glob
from osgeo import gdal
import csv
import subprocess
import shutil

# Arg 1 = bin directory
# Arg 2 = Output directory

pwd_dir = '/home/sb708/Projects/fastscape_work'
data_dir = '/home/sb708/Projects/fastscape_work/catchment_clips/clip_dat.csv'

bc_hash = {}
coord_hash = {}
with open(data_dir, 'rb') as csvfile:
    dat = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(dat)
    for row in dat:
        print
        bc_hash.update({int(float(row[0])):[int(float(row[-4])),int(float(row[-3])),int(float(row[-2])),int(float(row[-1]))]})
	coord_hash.update({int(float(row[0])):[int(float(row[-8])),int(float(row[-7])),int(float(row[-6])),int(float(row[-5]))]})
src_dir = './catchment_bins'
dst_dir = './'

bin_files = glob.glob(src_dir+"/*.bin")

restart = -1


dt = 100.00
nstep = 10
nfreq = 5

num_threads = 4

law = 2
kd = 1E-2
kf = 1E-05
n = 2
m = .4
vex = 2

precipitation_n = 0
precipitation_v1 = 0.10
uplift_n = 0
uplift_v1 = 0
uplift_v2 = 0
uplift_v3 = 0
uplift_v4 = 0
plot_all = 0
plot_topo = 1
plot_sedim = 1
metric = '00001'
local_minima = 0


for b in bin_files:

    zMin_command = "gdalinfo -mm "+b+" | sed -ne 's/.*Computed Min\/Max=//p'| tr -d ' ' | cut -d ',' -f 1 | cut -d . -f 1"
    zMax_command = "gdalinfo -mm "+b+" | sed -ne 's/.*Computed Min\/Max=//p'| tr -d ' ' | cut -d ',' -f 2 | cut -d . -f 1"

    proc_min = subprocess.Popen(zMin_command, stdout=subprocess.PIPE, shell=True)
    (zMin, err) = proc_min.communicate()
    proc_max = subprocess.Popen(zMax_command, stdout=subprocess.PIPE, shell=True)
    (zMax, err) = proc_max.communicate()

    sea_level = zMin

    dataset = gdal.Open(b)
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    DEM = b

    bs = os.path.basename(DEM)
    sp = bs.split(".")
    id = int(sp[0])
    nx = cols
    ny = rows
    no = '{0:04d}'.format(id)

    bc_n = bc_hash[id]
    # Reorder bc due to weird flipping of raster
    bc_f = [bc_n[2], bc_n[1], bc_n[0], bc_n[3]]
    bc = ''.join(map(str,bc_f))
    
    xy_f = coord_hash[id]
    
    # xmin
    # xmax
    # ymax
    # ymin
    
    xl = xy_f[1] - xy_f[0]
    yl = xy_f[2] - xy_f[3]

    run_name = 'R'+str(no)
    batch_dir = os.path.join(dst_dir, run_name)
    if os.path.exists(batch_dir):
      for the_file in os.listdir(batch_dir):
        file_path = os.path.join(batch_dir, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    else:
      os.mkdir(batch_dir)
      
    config_file = os.path.join(batch_dir, 'FastScape.in')


    f = open(config_file, 'w')

    f.write('restart = ' +str(restart)+ '\n')
    f.write('DEM = ' +str(b)+ '\n')
    f.write('nx = ' +str(cols)+ '\n')
    f.write('ny = ' +str(rows)+ '\n')
    f.write('xl = ' +str(xl)+ '\n')
    f.write('yl = ' +str(yl)+ '\n')
    f.write('dt = ' +str(dt)+ '\n')
    f.write('bc = ' +str(bc)+ '\n')
    f.write('nstep = ' +str(nstep)+ '\n')
    f.write('nfreq = ' +str(nfreq)+ '\n')
    f.write('law = ' +str(law)+ '\n')
    f.write('m = ' +str(m)+ '\n')
    f.write('kf = ' +str(kf)+ '\n')
    f.write('precipitation_n = ' +str(precipitation_n)+ '\n')
    f.write('precipitation_v1 = ' +str(precipitation_v1)+ '\n')
    f.write('local_minima = ' +str(local_minima)+ '\n')
    f.write('sea_level = ' +str(sea_level)+ '\n')
    f.write('uplift_n = ' +str(uplift_n)+ '\n')
    f.write('uplift_v1 = ' +str(uplift_v1)+ '\n')
    f.write('uplift_v2 = ' +str(uplift_v2)+ '\n')
    f.write('uplift_v3 = ' +str(uplift_v3)+ '\n')
    f.write('uplift_v4 = ' +str(uplift_v4)+ '\n')
    f.write('plot_all = ' +str(plot_all)+ '\n')
    f.write('plot_topo = ' +str(plot_topo)+ '\n')
    f.write('plot_sedim = ' +str(plot_sedim)+ '\n')
    f.write('vex = ' +str(vex)+ '\n')
    f.write('metric = ' +str(metric)+ '\n')

    f.close()

    os.system("bash "+pwd_dir+"/FastScape.sh "+run_name)
    os.system("R -q -f Metric.R > R-report.txt")

