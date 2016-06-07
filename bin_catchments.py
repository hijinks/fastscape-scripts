import os
import glob

# Arg 1 = bin directory
# Arg 2 = Output directory

#bin_directory = sys.argv[0]
#output_directory = sys.argv[1]


# gdal_translate -of ENVI -ot Int16 grotto_dem8.tif grotto.bin

src_path = './catchment_clips'
dst_dir = './catchment_bins'

tif_files = glob.glob(src_path+"/*.tif")

for t in tif_files:
    tf = os.path.basename(t)
    sp = tf.split('.')
    run_name = str(sp[0])+'.bin'
    bin_path = os.path.join(dst_dir, run_name)
    os.system("gdal_translate -of ENVI -ot Int16 "+t+" "+bin_path)