"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/8/input"


UNIQUE_LENGTHS = (2, 4, 3, 7)
def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.replace("|", "").strip().split("\n"), columns=["entry"])
    code_df = entry_df["entry"].str.split(expand=True)
    digit_df = code_df.loc[:, 10:].stack().reset_index(drop=True)
    print(digit_df.str.len().isin(UNIQUE_LENGTHS).sum())


def puzzle2(answer=None):
    """
    The logic is clear, however, the manipulation of dataframe is complicated.
    There should be a more "dataframic" way to solve.
    """
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.replace("|", "").strip().split("\n"), columns=["entry"])
    code_df = entry_df["entry"].str.split(expand=True)

    def _decode_digits(row):
        code_map = {}
        code_map[1] = set(list(row.loc[row.str.len()==2].values[0]))
        code_map[4] = set(list(row.loc[row.str.len()==4].values[0]))
        code_map[7] = set(list(row.loc[row.str.len()==3].values[0]))
        code_map[8] = set(list(row.loc[row.str.len()==7].values[0]))
        len_5s = row.loc[row.str.len()==5].values
        for code in len_5s:  # 3, 5, 2 have 5 segments
            code_set = set(list(code))
            if code_map[1].issubset(code_set):  # 3 is superset of 1
                code_map[3] = code_set
            elif (code_map[4] - code_map[1]).issubset(code_set):  # 5 is superset of (difference of 4 and 1)
                code_map[5] = code_set
            else:
                code_map[2] = code_set
        len_6s = row.loc[row.str.len()==6].values
        for code in len_6s:  # 9, 6, 0 have 6 segments
            code_set = set(list(code))
            if code_map[4].issubset(code_set):  # 9 is superset of 4
                code_map[9] = code_set
            elif (code_map[8] - code_map[7]).issubset(code_set):  # 6 is superset of (difference of 8 and 7)
                code_map[6] = code_set
            else:
                code_map[0] = code_set
        return {"".join(sorted(v)): k for k, v in code_map.items()}

    value_cols = [10, 11, 12, 13]
    code_df[value_cols] = code_df[value_cols].applymap(lambda e: "".join(sorted(e)))
    for _, row in code_df.iterrows():
        code_map = _decode_digits(row)
        for i in value_cols:
            row[i] = code_map[row[i]] * 10**(value_cols[-1] - i)
    print(code_df[value_cols].sum().sum())


if __name__ == "__main__":
    puzzle1(330)
    puzzle2(1010472)
