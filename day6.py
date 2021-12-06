"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/6/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)  # "3,4,3,1,2" -> 5934
    fish_df = pd.DataFrame(raw_input.strip().split(","), columns=["count_down"], dtype=int)
    for _ in range(80):
        fish_df["count_down"] -= 1
        new_fish_num = fish_df.loc[fish_df["count_down"]==-1].size
        if new_fish_num:
            fish_df.loc[fish_df["count_down"]==-1, "count_down"] = 6
            fish_df = fish_df.append(pd.DataFrame([8] * new_fish_num, columns=["count_down"], dtype=int))
        #print(fish_df["count_down"].tolist())
    print(fish_df.size)


def puzzle2(answer=None):
    """Have to work out how to avoid exponential growth of computation"""
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)  # "3,4,3,1,2" -> 26984457539
    fish_df = pd.DataFrame(raw_input.strip().split(","), columns=["count_down"], dtype=int)

    fish_gen_df = fish_df.groupby("count_down", as_index=False).size()
    for _ in range(256):
        fish_gen_df["count_down"] -= 1
        new_fish_num = fish_gen_df.loc[fish_gen_df["count_down"]==-1, "size"].tolist()
        if new_fish_num:
            fish_gen_df.loc[fish_gen_df["count_down"]==-1, "count_down"] = 6
            fish_gen_df = fish_gen_df.append(pd.DataFrame([(8, new_fish_num[0])], columns=["count_down", "size"], dtype=int))
        # Aggregation needed to avoid exponential growth
        fish_gen_df = fish_gen_df.groupby(["count_down"], as_index=False).sum("size")
    print(fish_gen_df["size"].sum())


if __name__ == "__main__":
    puzzle1(349549)
    puzzle2(1589590444365)
