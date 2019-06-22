from pprint import pprint
import re
import math

import PIL.Image
import PIL.ImageDraw
import PIL.ImagePath
import toolz.functoolz as tzf


def _desc_path():
    return './data/part-1-examples/example-01.desc'


def _point_pattern():
    return r'\((\d+),(\d+)\)'


def _parse_map_str(map_str):
    return tzf.thread_last(re.findall(_point_pattern(), map_str),
                           (map, lambda p: tuple(int(x) for x in p)),
                           list)


def _parse_worker_pos(worker_str):
    return _parse_map_str(worker_str)[0]

def _parse_obstacles_str(s):
    return tzf.thread_last(s.split(';'),
                           (map, _parse_map_str),
                           list)


def _read_desc(path):
    with open(path) as f:
        contents = f.read()
    mine_map_str, worker_pos_str, obstacles_str, boosters_str = contents.split('#')

    return {'mine_map': _parse_map_str(mine_map_str),
            'worker_pos': _parse_worker_pos(worker_pos_str),
            'obstacles_pts': _parse_obstacles_str(obstacles_str),
            'boosters_str': boosters_str}


def main():
    desc = _read_desc(_desc_path())
    pprint(desc)

    render_scale = 8
    map_bbox = PIL.ImagePath.Path(desc['mine_map']).getbbox()
    map_size = [math.ceil(a) + 1
                for a in [map_bbox[2] - map_bbox[0], map_bbox[3] - map_bbox[1]]]
    im = PIL.Image.new('RGBA', map_size)

    d_ctx = PIL.ImageDraw.Draw(im)
    d_ctx.polygon(desc['mine_map'], fill='white')
    d_ctx.point(desc['worker_pos'], fill='red')

    im = im.resize([s * render_scale for s in map_size])
    im.save('data/output/sample.png')


if __name__ == '__main__':
    main()
