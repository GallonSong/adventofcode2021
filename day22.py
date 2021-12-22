"""
"""
from itertools import product
import re
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/22/input"


def get_region(start, end):
    start, end = int(start), int(end)
    low, high = min(start, end), max(start, end)
    r_start, r_end = max(low, -50), min(high, 50)
    return range(r_start, r_end+1)

def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    core_df = pd.DataFrame([])
    for line in raw_input.strip().split("\n"):
        m = re.search(r"^(\w+) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)", line)
        switch, x_s, x_e, y_s, y_e, z_s, z_e = m.groups()
        cuboid_df = pd.DataFrame(product(get_region(x_s, x_e), get_region(y_s, y_e), get_region(z_s, z_e)), columns=["x", "y", "z"], dtype=int)
        cuboid_df["on"] = 1 if switch == "on" else -1
        core_df = core_df.append(cuboid_df)
        core_df = core_df.groupby(["x", "y", "z"]).sum().reset_index()
        core_df = core_df.loc[core_df.on>=1]
        core_df["on"] = 1
    print(len(core_df))
    

def low_to_high(start, end):
    return min(start, end), max(start, end)


def get_overlap(cube1, cube2):
    overlap = [0, 0, 0]
    for i in range(3):  # x,y,z
        low, high = max(cube1[i][0], cube2[i][0]), min(cube1[i][1], cube2[i][1])
        if low <= high:
            overlap[i] = (low, high)
    return overlap if 0 not in overlap else None


def break_cube(cube, overlap):
    breaks = []
    for i in range(3):
        points = tuple(sorted(set(cube[i]).union(set(overlap[i]))))
        if len(points) == 1:
            breaks.append([(points[0], points[0])])
        elif len(points) == 2:
            if overlap[i][0] != overlap[i][1]:
                breaks.append([points])
            elif cube[i][0] == overlap[i][0]:  # [|--]
                breaks.append([(points[0], points[0]), (points[0]+1, points[1])])
            else:   # [--|]
                breaks.append([(points[0], points[1]-1), (points[1], points[1])])
        elif len(points) == 3:
            if cube[i][0] == overlap[i][0]:  # [[--]--]
                breaks.append([(points[0], points[1]), (points[1]+1, points[2])])
            else:  # [--[--]]
                breaks.append([(points[0], points[1]-1), (points[1], points[2])])
        elif len(points) == 4:
            breaks.append([(points[0], points[1]-1), (points[1], points[2]), (points[2]+1, points[3])])
    return [comb for comb in product(*breaks) if list(comb) != overlap]


def play_switch(switch, cube, on_cubes):
    new_on_cubes = []
    for on_cube in on_cubes:
        overlap = get_overlap(cube, on_cube)
        if overlap:  # new_cube does not change
            new_on_cubes += break_cube(on_cube, overlap)
        else:
            new_on_cubes.append(on_cube)
    if switch == "on":
        new_on_cubes.append(cube)
    return new_on_cubes


def puzzle2(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    cuboids = []
    for line in raw_input.strip().split("\n"):
        m = re.search(r"^(\w+) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)", line)
        switch, (x_s, x_e, y_s, y_e, z_s, z_e) = m.group(1), tuple(map(int, m.groups()[1:]))
        cuboids.append((switch, low_to_high(x_s, x_e), low_to_high(y_s, y_e), low_to_high(z_s, z_e)))

    on_cubes = [cuboids[0][1:]]
    for cuboid in cuboids[1:]:
        on_cubes = play_switch(cuboid[0], cuboid[1:], on_cubes)

    total_cube = 0
    for cube in on_cubes:
        cube_x = cube[0][1] - cube[0][0] + 1
        cube_y = cube[1][1] - cube[1][0] + 1
        cube_z = cube[2][1] - cube[2][0] + 1
        total_cube += cube_x * cube_y * cube_z
    print(len(on_cubes), total_cube)


if __name__ == "__main__":
    puzzle1(620241)
    puzzle2(1284561759639324)
