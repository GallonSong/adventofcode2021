"""
"""
from collections import defaultdict
from itertools import product
import math
import re
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/17/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    ranges = re.search(r"^target area: x=(\d.*)\.\.(\d.*), y=(-\d.*)\.\.(-\d.*)", raw_input)
    x_s, x_e, y_s, y_e = map(int, ranges.groups())
    print((y_s)*(y_s+1)/2)
    

def puzzle2(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL).strip()
    ranges = re.search(r"^target area: x=(\d.*)\.\.(\d.*), y=(-\d.*)\.\.(-\d.*)", raw_input)
    x_s, x_e, y_l, y_h = map(int, ranges.groups())
    print(x_s, x_e, y_l, y_h)
    v_x_min, v_x_max = math.ceil(math.sqrt(x_s*2)-0.5), x_e
    v_y_min, v_y_max = y_l, abs(y_l) - 1
    initial_v, possible_v_x, possible_v_y = [], defaultdict(list), defaultdict(list)
    for v_x in range(v_x_min, v_x_max+1):
        distance, v_x_new, step = 0, v_x, 0
        while distance <= x_e:
            step += 1
            distance += v_x_new
            v_x_new -= 1 if v_x_new > 0 else 0
            if x_s <= distance <= x_e:
                possible_v_x[step].append(v_x)
                if v_x_new == 0:
                    possible_v_x[f"h_stop-{step}"].append(v_x)
                    break
    for v_y in range(v_y_min, v_y_max+1):
        distance, v_y_new, step = 0, v_y, 0
        while distance >= y_l:
            step += 1
            distance += v_y_new
            v_y_new -= 1
            if y_l <= distance <= y_h:
                possible_v_y[step].append(v_y)
    # print({k: len(v) for k, v in possible_v_x.items()})
    # print({k: len(v) for k, v in possible_v_y.items()})

    for step, speeds in possible_v_x.items():
        if step in possible_v_y:
            initial_v += list(product(speeds, possible_v_y[step]))
        elif str(step).startswith("h_stop"):
            step_l = int(step.split("-")[1])
            for step_y, speeds_y in possible_v_y.items():
                if step_y >= step_l:
                    initial_v += list(product(speeds, speeds_y))
    # print(sorted(set(initial_v)))
    print(len(sorted(set(initial_v))))

if __name__ == "__main__":
    puzzle1(11781)
    puzzle2(4531)
