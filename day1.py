import pandas as pd
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/1/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    measurement_df = pd.DataFrame(raw_input.split(), columns=["original"], dtype=int)
    
    measurement_df["lag1"] = measurement_df.shift(periods=1)
    measurement_df["increase"] = measurement_df["original"] > measurement_df["lag1"]
    print(sum(measurement_df["increase"]))
    #print(measurement_df)


def puzzle2(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    measurement_df = pd.DataFrame(raw_input.split(), columns=["original"], dtype=int)

    window_size = 3
    measurement_df["window3sum"] = measurement_df.rolling(window_size).sum()
    measurement_df["lag1"] = measurement_df["window3sum"].shift(periods=1)
    measurement_df["increase"] = measurement_df["window3sum"] > measurement_df["lag1"]
    print(sum(measurement_df["increase"]))
    #print(measurement_df)


if __name__ == "__main__":
    puzzle1(1387)
    puzzle2(1362)
