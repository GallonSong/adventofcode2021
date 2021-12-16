"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/15/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    heatmap_df = pd.DataFrame(entry_df["entry"].apply(list).tolist(), dtype=int)
    coord_df = heatmap_df.stack().reset_index().astype(int).rename(columns={"level_0": "x", "level_1": "y", 0: "danger"})
    coord_df["cum_danger"] = 0
    for i in range (1, len(entry_df)*2-1):
        for index, c in coord_df.loc[(coord_df.x+coord_df.y) == i].iterrows():
            left = coord_df.loc[(coord_df.x==c.x-1) & (coord_df.y==c.y), "cum_danger"].values[0] if c.x > 0 else 1000
            up = coord_df.loc[(coord_df.x==c.x) & (coord_df.y==c.y-1), "cum_danger"].values[0] if c.y > 0 else 1000
            coord_df.loc[index, "cum_danger"] = min(left, up) + coord_df.loc[index, "danger"]
    print(coord_df.pivot(index="x", columns="y", values="cum_danger"))
    

def puzzle2(answer=None):
    """Down-and-right does not work any more in puzzle2. Dijkstra's algorithm for shortest paths."""
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    heatmap_df = pd.DataFrame(entry_df["entry"].apply(list).tolist()).astype(int)
    heatmap_v_df = pd.concat([heatmap_df+i for i in range(0,5)], axis=1)
    heatmap_w_df = pd.concat([heatmap_v_df+i for i in range(0,5)], axis=0).reset_index(drop=True)
    heatmap_w_df.columns = range(len(heatmap_df)*5)
    coord_df = heatmap_w_df.stack().reset_index().astype(int).rename(columns={"level_0": "x", "level_1": "y", 0: "danger"})
    coord_df.loc[coord_df.danger>9, "danger"] -= 9
    coord_df["cum_danger"] = np.inf
    coord_df["temp_danger"] = np.inf
    coord_df["unvisited"] = True
    coord_df.loc[(coord_df.x==0) & (coord_df.y==0), "cum_danger"] = 0
    side_len = len(heatmap_w_df) - 1
    search_step = 0
    while coord_df.unvisited.any():
        current_node = coord_df.loc[coord_df.unvisited, "cum_danger"].idxmin()
        x, y = coord_df.loc[current_node, ["x", "y"]]
        if x == side_len and y == side_len:
            print(coord_df.iloc[current_node]["cum_danger"])
            break
        neighbors = ((coord_df.x==x) & (coord_df.y.isin([y-1, y+1]))) | ((coord_df.y==y) & (coord_df.x.isin([x-1, x+1])))
        coord_df.loc[neighbors & coord_df.unvisited, "temp_danger"] = coord_df.loc[neighbors & coord_df.unvisited, "danger"] + coord_df.iloc[current_node]["cum_danger"]
        coord_df.loc[neighbors & coord_df.unvisited, "cum_danger"] = coord_df.loc[neighbors & coord_df.unvisited][["cum_danger", "temp_danger"]].min(axis=1)
        coord_df.loc[current_node, "unvisited"] = False
        search_step += 1
        if search_step % 100 == 0:
            print(search_step, x, y, coord_df.iloc[current_node]["cum_danger"])
    print(coord_df.pivot(index="x", columns="y", values="cum_danger"))


if __name__ == "__main__":
    puzzle1(435)
    puzzle2(2842)
