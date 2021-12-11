"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/11/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    energy_df = pd.DataFrame(entry_df["entry"].apply(list).tolist(), dtype=int)
    coord_df = energy_df.stack().reset_index().astype(int).rename(columns={"level_0": "x", "level_1": "y", 0: "energy"})
    flashes = 0
    for i in range(1000):
        coord_df["energy"] += 1
        flash_filter = coord_df.energy == 10
        flashed_filter_df = coord_df.loc[coord_df.energy == 100]
        while coord_df.loc[flash_filter].size:
            for _, row in coord_df.loc[flash_filter].iterrows():
                coord_df.loc[(coord_df.x <= row.x+1) & (coord_df.x >= row.x-1) & (coord_df.y <= row.y+1) & (coord_df.y >= row.y-1) & (coord_df.energy != 10), "energy"] += 1
                coord_df.loc[(coord_df.x == row.x) & (coord_df.y == row.y), "energy"] += 1
                flashed_filter_df.append(coord_df.loc[(coord_df.x == row.x) & (coord_df.y == row.y)])
            flash_filter = (coord_df.energy == 10) & (~coord_df.index.isin(flashed_filter_df.index.unique()))

        flashes += len(coord_df.loc[coord_df.energy > 9])   
        coord_df.loc[coord_df.energy > 9, "energy"] = 0 
        #print(coord_df.pivot(index="x", columns="y", values="energy"))
    print(flashes)


def puzzle2(answer=None):
    """
    The logic is clear, however, the manipulation of dataframe is complicated.
    There should be a more "dataframic" way to solve.
    """
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    energy_df = pd.DataFrame(entry_df["entry"].apply(list).tolist(), dtype=int)
    coord_df = energy_df.stack().reset_index().astype(int).rename(columns={"level_0": "x", "level_1": "y", 0: "energy"})
    flashes = 0
    for i in range(1000):
        coord_df["energy"] += 1
        flash_filter = coord_df.energy == 10
        flashed_filter_df = coord_df.loc[coord_df.energy == 100]
        while coord_df.loc[flash_filter].size:
            for _, row in coord_df.loc[flash_filter].iterrows():
                coord_df.loc[(coord_df.x <= row.x+1) & (coord_df.x >= row.x-1) & (coord_df.y <= row.y+1) & (coord_df.y >= row.y-1) & (coord_df.energy != 10), "energy"] += 1
                coord_df.loc[(coord_df.x == row.x) & (coord_df.y == row.y), "energy"] += 1
                flashed_filter_df.append(coord_df.loc[(coord_df.x == row.x) & (coord_df.y == row.y)])
            flash_filter = (coord_df.energy == 10) & (~coord_df.index.isin(flashed_filter_df.index.unique()))

        flashes += len(coord_df.loc[coord_df.energy > 9])   
        coord_df.loc[coord_df.energy > 9, "energy"] = 0 
        if not coord_df.energy.any():
            print(i+1)
            break


if __name__ == "__main__":
    puzzle1(1627)
    puzzle2(329)
