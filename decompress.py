import argparse
import os
import sys
import time

def safe_call(command):
    exit_code = os.system(command)
    if exit_code > 0:
        sys.exit(exit_code)

def decompress(args):
    safe_call("mkdir -p {}".format(args.output_dir))
    time_start = time.time()
    img_count = 0
    for f in os.listdir(args.input_dir):
        img_count += 1
        filename, file_extension = os.path.splitext(f)
        file_in = args.input_dir + "/" + filename + file_extension
        file_out = args.output_dir + "/" + filename + ".decompress.tif"
        safe_call("gdal_translate {} {} -of GTIFF -co COMPRESS=NONE".format(file_in, file_out))

    time_end = time.time()
    print("time: {}", (time_end - time_start) * 1000 / img_count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    decompress(args)
