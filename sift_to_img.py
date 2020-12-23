import argparse
import cv2
import os
import numpy as np


def sift_to_img(in_file, out_file, t):
    f = open(in_file)

    line = f.readline()
    count = int(line.split()[0])

    coord = []
    scale = []
    orient = []

    line = f.readline()
    while line:
        if len(line.split(" ")) == 4:
            s = line.split(" ")
            coord.append([int(float(s[0])), int(float(s[1]))])
            scale.append(float(s[2]))
            orient.append(float(s[3]))
        line = f.readline()
    f.close()
    assert len(coord) == count
    assert len(scale) == count

    coord = np.array(coord)
    scale = np.array(scale)
    s_min = scale.min()
    s_max = scale.max()
    scale = ((scale - s_min) / (s_max - s_min) * 255).astype(np.uint8)
    orient = np.array(orient)
    o_min = orient.min()
    o_max = orient.max()
    orient = ((orient - o_min) / (o_max - o_min) * 255).astype(np.uint8)


    img = np.zeros((2000, 2000), dtype=np.uint8)
    for i in range(count):
        y, x = coord[i]
        if t == "s":
            img[x, y] = scale[i]
        else:
            assert t == "o"
            img[x, y] = orient[i]

    img = img[..., np.newaxis]
    cv2.imwrite(out_file, img)


def main(inp, out, t):
    if os.path.isdir(inp):
        if not os.path.exists(out):
            os.makedirs(out)
        for f in os.listdir(inp):
            f_in = inp + "/" + f
            f_out = out + "/" + f + ".jpg"
            sift_to_img(f_in, f_out, t)
    else:
        assert os.path.isfile(inp)
        sift_to_img(inp, out, t)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="input, file or dir")
    parser.add_argument("output", help="output, file or dir")
    parser.add_argument("--type", required=True, choices=["s", "o"])
    args = parser.parse_args()
    main(args.input, args.output, args.type)
