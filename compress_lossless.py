import argparse
import os
import sys
import time


def safe_call(command):
    exit_code = os.system(command)
    if exit_code > 0:
        sys.exit(exit_code)

def compress(args):
    safe_call("mkdir -p {}".format(args.output_dir))
    time_start = time.time()
    img_count = 0
    for f in os.listdir(args.input_dir):
        img_count += 1
        filename, file_extension = os.path.splitext(f)
        file_in = args.input_dir + "/" + filename + file_extension
        file_out = args.output_dir + "/" + filename + "." + args.compress

        command = "gdal_translate " + file_in + " -co COMPRESS={}".format(args.compress)

        if args.predictor:
            file_out += ".predictor{}".format(args.predictor)
            command += " -co PREDICTOR={}".format(args.predictor)

        if args.zlevel:
            assert args.compress == "DEFLATE", "zlevel only in DEFLATE"
            file_out += ".zlevel_{}".format(args.zlevel)
            command += " -co zlevel={}".format(args.zlevel)

        if args.zstd_level:
            assert args.compress == "ZSTD", "zstf_level only in ZSTD"
            file_out += ".zstd_level_{}".format(args.zstd_level)
            command += " -co zstd_level={}".format(args.zstd_level)

        file_out += file_extension
        command += " {}".format(file_out)
        print(command)
        safe_call(command)

    time_end = time.time()
    print("time: {}", (time_end - time_start) * 1000 / img_count)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir")
    parser.add_argument("output_dir")
    parser.add_argument("--compress", required=True, choices=["LZW", "DEFLATE", "ZSTD"])
    parser.add_argument("--predictor", type=int, choices=[2])
    parser.add_argument("--zlevel", type=int, choices=range(1, 10))
    parser.add_argument("--zstd_level", type=int, choices=range(1, 23))
    args = parser.parse_args()
    compress(args)

