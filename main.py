import os
from pprint import pprint
import re

import PIL.Image
import PIL.ImageDraw
import toolz.functoolz as tzf


def _desc_path():
    return './data/part-1-initial/prob-001.desc'


def _read_desc(path):
    with open(path) as f:
        contents = f.read()
    mine_map_str, worker_pos_str, obstacles_str, boosters_str = contents.split('#')

    point_pattern = r'\((\d+),(\d+)\)'
    mine_points = tzf.thread_last(re.findall(point_pattern, mine_map_str),
                                  (map, lambda p: tuple(int(x) for x in p)),
                                  list)
    worker_pos = tzf.thread_last(re.match(point_pattern, worker_pos_str).groups(),
                                 (map, int),
                                 tuple)

    return {'mine_map': mine_points,
            'worker_pos': worker_pos,
            'obstacles_str': obstacles_str,
            'boosters_str': boosters_str}


def main():
    # data_size = (64, 64)
    # im = PIL.Image.new('RGB', data_size, color='red')
    # d = PIL.ImageDraw.Draw(im)
    # d.text((10, 10), 'Hello, world')

    # im = im.resize([s * 10 for s in data_size])
    # im.save('data/output/sample.png')

    pprint(_read_desc(_desc_path()))


if __name__ == '__main__':
    main()
