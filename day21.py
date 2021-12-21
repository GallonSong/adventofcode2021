"""
"""
from itertools import product
import re
from numpy.core.numeric import roll
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/21/input"


def puzzle1(answer=None):
    if answer:
        return answer
    pd.set_option('display.max_rows', 200)
    raw_input = get_input(INPUT_URL)
    starts = list(map(int, re.findall(r"position: (\d+)", raw_input)))
    dice_df = pd.DataFrame(np.array(list(range(1, 101))*3).reshape(50, 6))
    winner = None
    while True:
        dice_df["p1"], dice_df["p2"] = dice_df[0] + dice_df[1] + dice_df[2], dice_df[3] + dice_df[4] + dice_df[5]
        dice_df.p1, dice_df.p2 = (dice_df.p1.cumsum() + starts[0] - 1) % 10 + 1, (dice_df.p2.cumsum() + starts[1] - 1) % 10 + 1
        if dice_df.p1.sum() >= 1000:
            winner = "p1"
            break
        elif dice_df.p2.sum() >= 1000:
            winner = "p2"
            break
        else:
            dice_df = dice_df.append(dice_df).reset_index(drop=True)
    dice_df["p1_cum"], dice_df["p2_cum"] = dice_df.p1.cumsum(), dice_df.p2.cumsum()
    print(dice_df.loc[dice_df[f"{winner}_cum"] > 989].iloc[:3])  # the game ends at the exact point when any player hit 1000
    

def roll_and_count(df, distribution, step):
    df[step] = ",".join(map(str, distribution.keys()))
    df[step] = df[step].str.split(",")
    df = df.explode(step).astype(int).reset_index(drop=True)
    df["path_amount"] *= df[step].map(distribution)
    df[step] = (df[step] + df[str(int(step)-1)] - 1) % 10 + 1
    df["path_sum"] += df[step]
    return df


def puzzle2(answer=None):
    if answer:
        return answer
    pd.set_option('display.max_rows', 500)
    raw_input = get_input(INPUT_URL)
    starts = list(map(int, re.findall(r"position: (\d+)", raw_input)))
    dice_df = pd.DataFrame(product((1,2,3), repeat=3))
    dice_df["score"] = dice_df[0] + dice_df[1] + dice_df[2]
    score_distribution = dice_df.groupby("score").size().to_dict()
    path_df = pd.DataFrame(product(score_distribution.keys(), repeat=2)).rename(columns={0: "0", 1: "1"})
    p1_path_df = (path_df.cumsum(axis=1) + starts[0] - 1) % 10 + 1
    p1_path_df["path_sum"] = p1_path_df["0"] + p1_path_df["1"]
    p1_path_df["path_amount"] = path_df["0"].map(score_distribution) * path_df["1"].map(score_distribution)
    p2_path_df = (path_df.cumsum(axis=1) + starts[1] - 1) % 10 + 1
    p2_path_df["path_sum"] = p2_path_df["0"] + p2_path_df["1"]
    p2_path_df["path_amount"] = path_df["0"].map(score_distribution) * path_df["1"].map(score_distribution)
    step = "2"  # no one can win before 3 rollings
    p1_win, p2_win = 0, 0
    while (p1_path_df.path_sum < 21).any():
        p1_path_df = roll_and_count(p1_path_df, score_distribution, step)
        p2_pre_fail = p2_path_df.loc[p2_path_df.path_sum < 21, "path_amount"].sum()
        p1_win += p1_path_df.loc[p1_path_df.path_sum >= 21, "path_amount"].sum() * p2_pre_fail

        p2_path_df = roll_and_count(p2_path_df, score_distribution, step)
        p2_win += p1_path_df.loc[p1_path_df.path_sum < 21, "path_amount"].sum() * p2_path_df.loc[p2_path_df.path_sum >= 21, "path_amount"].sum()
        
        step = str(int(step)+1)
        p1_path_df = p1_path_df.loc[p1_path_df.path_sum < 21]
        p2_path_df = p2_path_df.loc[p2_path_df.path_sum < 21]
    print(p1_win, p2_win)


if __name__ == "__main__":
    puzzle1(671580)
    puzzle2(912857726749764)
