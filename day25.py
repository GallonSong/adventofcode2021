"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/25/input"


def move_cucumber(coord_df, herd, range_mapping):
    herd_coord, herd_direction, herd_value = {"east": ("x", "y", 1), "south": ("y", "x", 4)}[herd]  # (groupby, extend_direction, unique_number)
    direction_range = range_mapping[herd_direction]
    # extend on both ends to facilitate currents movement
    currents_behind_df, currents_front_df = coord_df.loc[coord_df[herd_direction] == direction_range], coord_df.loc[coord_df[herd_direction] == 0]
    currents_behind_df.loc[:,herd_direction] = -1
    currents_front_df.loc[:,herd_direction] = direction_range + 1
    coord_df = coord_df.append(currents_behind_df).append(currents_front_df).sort_values(["x", "y"]).reset_index(drop=True)

    coord_df["front_cucu"] = coord_df.groupby(herd_coord)["cucumber"].shift(-1)  # facilitate update old position
    coord_df["behind_cucu"] = coord_df.groupby(herd_coord)["cucumber"].shift(1)
    coord_df["cum_cucu"] = coord_df["cucumber"] + coord_df["behind_cucu"]
    
    old_positions = (coord_df.front_cucu == 0) & (coord_df.cucumber == herd_value)
    new_positions = (coord_df.cum_cucu == herd_value) & (coord_df.cucumber == 0)
    coord_df.loc[old_positions, "cucumber"] = 0
    coord_df.loc[new_positions, "cucumber"] = herd_value
    
    map_range = (coord_df.x >= 0) & (coord_df.x <= range_mapping["x"]) & (coord_df.y >= 0) & (coord_df.y <= range_mapping["y"])
    return coord_df.loc[map_range, ["x", "y", "cucumber"]].reset_index(drop=True), len(coord_df.loc[new_positions]) > 0


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    heatmap_df = pd.DataFrame(entry_df["entry"].apply(list).tolist(), dtype=int).replace({"v": 4, ">": 1, ".": 0})
    range_mapping = {"x": heatmap_df.index.max(), "y": heatmap_df.columns.max()}
    coord_df = heatmap_df.stack().reset_index().rename(columns={"level_0": "x", "level_1": "y", 0: "cucumber"})
    print(coord_df.pivot(index="x", columns="y", values="cucumber"))
    step = 1
    while True:
        coord_df, east_moved = move_cucumber(coord_df, "east", range_mapping)
        coord_df, south_moved = move_cucumber(coord_df, "south", range_mapping)
        if not (east_moved and south_moved):
            break
        step += 1
    print(step)
    

if __name__ == "__main__":
    puzzle1(557)
