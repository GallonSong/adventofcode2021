"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/13/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    dot_df = entry_df.loc[~entry_df.entry.str.startswith("fold") & (entry_df.entry != ""), "entry"].str.split(",", expand=True)
    dot_df = dot_df.rename(columns={0: "x", 1: "y"}).astype(int)
    instruction_df = entry_df.loc[entry_df.entry.str.startswith("fold"), "entry"].str.split("=", expand=True).reset_index(drop=True)
    instruction_df[0] = instruction_df[0].str[-1]
    fold_along, fold_at = instruction_df.loc[0].values.tolist()
    dot_keep_df = dot_df.loc[dot_df[fold_along] < int(fold_at)]
    dot_fold_df = dot_df.loc[dot_df[fold_along] > int(fold_at)]
    dot_fold_df[fold_along] = int(fold_at) - (dot_fold_df[fold_along] - int(fold_at))
    print(len(dot_keep_df.append(dot_fold_df).drop_duplicates()))
    


def puzzle2(answer=None):
    """
    """
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    dot_df = entry_df.loc[~entry_df.entry.str.startswith("fold") & (entry_df.entry != ""), "entry"].str.split(",", expand=True)
    dot_df = dot_df.rename(columns={0: "x", 1: "y"}).astype(int)
    instruction_df = entry_df.loc[entry_df.entry.str.startswith("fold"), "entry"].str.split("=", expand=True).reset_index(drop=True)
    instruction_df[0] = instruction_df[0].str[-1]
    print(instruction_df.values.tolist())
    for fold_along, fold_at in instruction_df.values.tolist():
        dot_keep_df = dot_df.loc[dot_df[fold_along] < int(fold_at)]
        dot_fold_df = dot_df.loc[dot_df[fold_along] > int(fold_at)]
        dot_fold_df[fold_along] = int(fold_at) - (dot_fold_df[fold_along] - int(fold_at))
        dot_df = dot_keep_df.append(dot_fold_df).drop_duplicates()
    x_limit, y_limit = dot_df.x.max(), dot_df.y.max()
    code_array = np.ones((y_limit+1, x_limit+1))
    for x, y in dot_df.values.tolist():
        code_array[y, x] = 0
    for i in code_array:
        print(list(map(int, i)))


if __name__ == "__main__":
    puzzle1(687)
    puzzle2("FGKCKBZG")
