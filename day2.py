import pandas as pd
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/2/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    instruction_df = pd.DataFrame(raw_input.rstrip().split("\n"), columns=["i"])['i'].str.split(' ', expand=True)
    instruction_df[1] = instruction_df[1].astype(int)
    final_df = instruction_df.groupby(instruction_df[0]).sum()
    print(final_df.loc["forward", 1] * (final_df.loc["down", 1] - final_df.loc["up", 1]))


def puzzle2(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    instruction_df = pd.DataFrame(raw_input.rstrip().split("\n"), columns=["i"])['i'].str.split(' ', expand=True)
    instruction_df[1] = instruction_df[1].astype(int)
    
    change_aim = {"forward": 0, "down": 1, "up": -1}
    instruction_df["change_aim"] = instruction_df[0].map(change_aim)
    instruction_df["aim"] = (instruction_df[1] * instruction_df["change_aim"]).cumsum()
    instruction_df["aim_lag1"] = instruction_df["aim"].shift(periods=1)
    print(instruction_df)
    movement_df = instruction_df[instruction_df[0]=="forward"]
    h_position = movement_df[1].sum()
    depth = (movement_df[1] * movement_df["aim_lag1"]).sum()
    print(h_position * depth)


if __name__ == "__main__":
    puzzle1(1882980)
    puzzle2(1971232560)
