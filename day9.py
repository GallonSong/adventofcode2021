"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/9/input"


UNIQUE_LENGTHS = (2, 4, 3, 7)
def puzzle1(answer=None):
    if answer:
        return answer
    pd.set_option('display.max_rows', 10)
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    heatmap_df = pd.DataFrame(entry_df["entry"].apply(list).tolist(), dtype=int)
    coord_df = heatmap_df.stack().reset_index().astype(int).rename(columns={"level_0": "x", "level_1": "y"})
    coord_df["x_low"] = coord_df.groupby("x")[0].rolling(3, min_periods=2, center=True).min().reset_index(drop=True)
    coord_df["x_avg"] = coord_df.groupby("x")[0].rolling(3, min_periods=2, center=True).mean().reset_index(drop=True)  # avoid plateau such as 9,9,9
    coord_df["y_low"] = coord_df.groupby("y")[0].rolling(3, min_periods=2, center=True).min().reset_index().sort_values(by="level_1")[0].reset_index(drop=True)  
    coord_df["y_avg"] = coord_df.groupby("y")[0].rolling(3, min_periods=2, center=True).mean().reset_index().sort_values(by="level_1")[0].reset_index(drop=True)
    coord_df["low"] = (coord_df[0] == coord_df["x_low"]) & (coord_df[0] == coord_df["y_low"]) & (coord_df[0] != coord_df["x_avg"]) & (coord_df[0] != coord_df["y_avg"])
    print((coord_df.loc[coord_df.low, 0] + 1).sum())


def puzzle2(answer=None):
    """
    pandas usage of any on 0 return false!
    """
    if answer:
        return answer
    pd.set_option('display.max_rows', 100)
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    heatmap_df = pd.DataFrame(entry_df["entry"].apply(list).tolist(), dtype=int)
    # heatmap_df.to_csv("heatmap.csv", index=False, header=False)
    coord_df = heatmap_df.stack().reset_index().astype(int).rename(columns={"level_0": "x", "level_1": "y"})
    coord_df["x_low"] = coord_df.groupby("x")[0].rolling(3, min_periods=2, center=True).min().reset_index(drop=True)
    coord_df["x_avg"] = coord_df.groupby("x")[0].rolling(3, min_periods=2, center=True).mean().reset_index(drop=True)  # avoid plateau such as 9,9,9
    coord_df["y_low"] = coord_df.groupby("y")[0].rolling(3, min_periods=2, center=True).min().reset_index().sort_values(by="level_1")[0].reset_index(drop=True)  
    coord_df["y_avg"] = coord_df.groupby("y")[0].rolling(3, min_periods=2, center=True).mean().reset_index().sort_values(by="level_1")[0].reset_index(drop=True)
    coord_df["low"] = (coord_df[0] == coord_df["x_low"]) & (coord_df[0] == coord_df["y_low"]) & (coord_df[0] != coord_df["x_avg"]) & (coord_df[0] != coord_df["y_avg"])
    coord_df["basin"] = None
    coord_df.loc[coord_df[0] == 9, "basin"] = 0
    coord_df.loc[coord_df.low, "basin"] = range(1, len(coord_df.loc[coord_df.low])+1)
    # for _, row in coord_df.loc[coord_df.low].iterrows():
    #     basin_x, basin_y, basin_num = row["x"], row["y"], row["basin"]
    #     y_low = coord_df.loc[(coord_df.x==basin_x) & (coord_df.basin==0) & (coord_df.y<basin_y), "y"].max() + 1 if coord_df.loc[(coord_df.x==basin_x) & (coord_df.basin==0) & (coord_df.y<basin_y), "y"].size else 0
    #     y_high = coord_df.loc[(coord_df.x==basin_x) & (coord_df.basin==0) & (coord_df.y>basin_y), "y"].min() if coord_df.loc[(coord_df.x==basin_x) & (coord_df.basin==0) & (coord_df.y>basin_y), "y"].size else 99
    #     coord_df.loc[(coord_df.x==basin_x) & coord_df.y.isin(range(y_low, y_high)), "basin"] = basin_num
    #     x_low = coord_df.loc[(coord_df.y==basin_y) & (coord_df.basin==0) & (coord_df.x<basin_x), "x"].max() + 1 if coord_df.loc[(coord_df.y==basin_y) & (coord_df.basin==0) & (coord_df.x<basin_x), "x"].size else 0
    #     x_high = coord_df.loc[(coord_df.y==basin_y) & (coord_df.basin==0) & (coord_df.x>basin_x), "x"].min() if coord_df.loc[(coord_df.y==basin_y) & (coord_df.basin==0) & (coord_df.x>basin_x), "x"].size else 99
    #     coord_df.loc[(coord_df.y==basin_y) & coord_df.x.isin(range(x_low, x_high)), "basin"] = basin_num
    # print("Round_1: ", coord_df.loc[coord_df.basin.isnull(), "basin"].size)

    searched = []
    def search(x, y, basin_num, searching):
        for t_x, t_y in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0<=t_x<=99 and 0<=t_y<=99 and (t_x, t_y) not in searching:
                new_position_mark = coord_df.loc[(coord_df.x==t_x) & (coord_df.y==t_y), "basin"].values[0]
                if new_position_mark == None:
                    searching.append((t_x, t_y))
                    basin_num, searching = search(t_x, t_y, basin_num, searching)
                elif new_position_mark > 0:
                    basin_num = new_position_mark
        return basin_num, searching

    for _, row in coord_df.loc[coord_df.basin.isnull()].iterrows():
        non_x, non_y = row["x"], row["y"]
        if (non_x, non_y) in searched:
            continue
        basin_num, searching = None, [(non_x, non_y)]
        basin_num, searching = search(non_x, non_y, basin_num, searching)
        for xx, yy in searching:
            coord_df.loc[(coord_df.x==xx) & (coord_df.y==yy), "basin"] = basin_num
        searched += searching
    print("Final: ", coord_df.loc[coord_df.basin.isnull(), "basin"].size)
    print(coord_df[coord_df.basin>0].groupby("basin").size().sort_values(ascending=False))
    print(np.prod(coord_df[coord_df.basin>0].groupby("basin").size().sort_values(ascending=False).values[:3]))


if __name__ == "__main__":
    puzzle1(548)
    puzzle2() # 786048
