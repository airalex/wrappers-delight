import os
from pprint import pprint
import re
import math

import PIL.Image
import PIL.ImageDraw
import PIL.ImagePath
import toolz.functoolz as tzf
import toolz.dicttoolz as tzd


def _desc_path():
    # return './data/part-1-examples/example-01.desc'
    return './data/part-1-initial/prob-004.desc'


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

    return {'mine_corners': _parse_map_str(mine_map_str),
            'worker_pos': _parse_worker_pos(worker_pos_str),
            'obstacles_corners': _parse_obstacles_str(obstacles_str)}


def _draw_polygon(im, pts, scale, color):
    d_ctx = PIL.ImageDraw.Draw(im)
    d_ctx.polygon([(x * scale, y * scale) for x, y in pts],
                  fill=color)


def _draw_point(im, pt, scale, color):
    x, y = pt
    _draw_polygon(im, [(x, y),
                       (x + 1, y),
                       (x + 1, y + 1),
                       (x, y + 1)],
                  scale=scale, color=color)


def _worker_reach_pts(pos, orien):
    x, y = pos
    if orien == 'r':
        return [(x, y),
                (x + 1, y - 1),
                (x + 1, y),
                (x + 1, y + 1)]
    elif orien == 'l':
        return [(x, y),
                (x - 1, y - 1),
                (x - 1, y),
                (x - 1, y + 1)]


def _draw_state(im, state, draw_opts):
    d_ctx = PIL.ImageDraw.Draw(im)

    _draw_polygon(im, state['desc']['mine_corners'], scale=draw_opts['render_scale'], color='white')

    for obs_pts in state['desc']['obstacles_corners']:
        _draw_polygon(im, obs_pts,
                      scale=draw_opts['render_scale'], color='gray')

    for pt in state['wrapped']:
        _draw_point(im, pt, scale=draw_opts['render_scale'], color='silver')

    for pt in _worker_reach_pts(state['worker']['pos'], state['worker']['orien']):
        _draw_point(im, pt,
                    scale=draw_opts['render_scale'], color='darkorange')
    _draw_point(im, state['worker']['pos'],
                scale=draw_opts['render_scale'], color='red')


def _export_im(im, path, draw_opts):
    im = im.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    im.save(path)


def _predict_action(state):
    pass


def _update_state(state, action):
    return state


def _output_image_dir(desc_path):
    desc_name = tzf.thread_last(desc_path,
                                os.path.basename,
                                os.path.splitext)[0]
    return os.path.join('./data/output', desc_name)


def _output_image_filepath(desc_path, turn, ext='.png'):
    return os.path.join(_output_image_dir(desc_path), '{}{}'.format(turn, ext))


def main():
    desc = _read_desc(_desc_path())
    pprint(desc)

    draw_opts = {'render_scale': 10}

    map_bbox = PIL.ImagePath.Path(desc['mine_corners']).getbbox()
    map_size = [math.ceil(a * draw_opts['render_scale'])
                for a in [map_bbox[2] - map_bbox[0], map_bbox[3] - map_bbox[1]]]
    im = PIL.Image.new('RGBA', map_size)

    state = {'desc': tzd.dissoc(desc, 'worker_pos'),
             'worker': {'pos': desc['worker_pos'],
                        'orien': 'r'},
             'wrapped': {(0, 4), (0, 5)}}
    _draw_state(im, state, draw_opts)

    os.makedirs(_output_image_dir(_desc_path()), exist_ok=True)
    _export_im(im, _output_image_filepath(_desc_path(), turn=0), draw_opts)


if __name__ == '__main__':
    main()
