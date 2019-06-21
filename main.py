import os
from pprint import pprint
import re

import PIL.Image
import PIL.ImageDraw
import PIL.ImagePath
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
    desc = _read_desc(_desc_path())
    pprint(desc)

    data_size = (10, 10)
    render_scale = 20
    im = PIL.Image.new('RGB', data_size, color='red')

    # path = PIL.ImagePath.Path(desc['mine_map'])
    d_ctx = PIL.ImageDraw.Draw(im)
    d_ctx.polygon(desc['mine_map'], fill='white')
    im = im.resize([s * render_scale for s in data_size])
    im.save('data/output/sample.png')


if __name__ == '__main__':
    main()
