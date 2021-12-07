"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/7/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    crab_df = pd.DataFrame(raw_input.strip().split(","), columns=["position"], dtype=int)
    median_crab = crab_df["position"].median()
    crab_df["fuel"] = crab_df["position"] - median_crab
    print(crab_df.abs().sum())


def puzzle2(answer=None):
    """"""
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)  # "16,1,2,0,4,2,7,1,2,14" -> 5 -> 168
    crab_df = pd.DataFrame(raw_input.strip().split(","), columns=["position"], dtype=int)
    median_crab = int(crab_df["position"].median())
    avg_position = round(crab_df["position"].mean())
    print(median_crab, avg_position)
    min_fuel = 10e9
    for i in range(median_crab, avg_position+1):
        crab_df["distance"] = (crab_df["position"] - i).abs()
        crab_df["fuel"] = crab_df["distance"] * (crab_df["distance"] + 1) / 2
        print(i, crab_df["fuel"].sum())
        if crab_df["fuel"].sum() < min_fuel:
            min_fuel = crab_df["fuel"].sum()
    print(min_fuel)


if __name__ == "__main__":
    puzzle1(355764)
    puzzle2(99634572)
