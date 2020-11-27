import argparse
import os
import sys

def safe_call(command):
    exit_code = os.system(command)
    if exit_code > 0:
        sys.exit(exit_code)

def to_uint16(args):
    safe_call("mkdir -p {}".format(args.output_dir))
    for f in os.listdir(args.input_dir):
        filename, file_extension = os.path.splitext(f)

        file_in = args.input_dir + "/" + filename + file_extension
        file_out = args.output_dir + "/" + filename + ".uint16" + file_extension
        safe_call("gdal_translate {} {} -ot UInt16".format(file_in, file_out))



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    to_uint16(args)

