"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/10/input"


CHUNK_MAP = {")": "(", "]": "[", "}": "{", ">": "<"}
INVERSE_CHUNK_MAP = {v: k for k, v in CHUNK_MAP.items()}
ILLEGAL_POINT_MAP = {")": 3, "]": 57, "}": 1197, ">": 25137}
COMPLETE_POINT_MAP = {")": 1, "]": 2, "}": 3, ">": 4}

def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    entry_df[["syntex", "error"]] = None, None
    for _, row in entry_df.iterrows():
        line_stack = []
        for c in row["entry"]:
            if c in CHUNK_MAP.values():
                line_stack.append(c)
            elif c in CHUNK_MAP:
                if CHUNK_MAP[c] != line_stack.pop():
                    row[["syntex", "error"]] = "corrupted", c
                    break
                else:
                    continue
        if line_stack and not row["syntex"]:
            row[["syntex", "error"]] = "incomplete", "".join(line_stack)

    print(entry_df.loc[entry_df.syntex=="corrupted"])
    print(entry_df.loc[entry_df.syntex=="corrupted", "error"].map(ILLEGAL_POINT_MAP).sum())


def puzzle2(answer=None):
    """
    The logic is clear, however, the manipulation of dataframe is complicated.
    There should be a more "dataframic" way to solve.
    """
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    entry_df[["syntex", "error"]] = None, None
    for _, row in entry_df.iterrows():
        line_stack = []
        for c in row["entry"]:
            if c in CHUNK_MAP.values():
                line_stack.append(c)
            elif c in CHUNK_MAP:
                if CHUNK_MAP[c] != line_stack.pop():
                    row[["syntex", "error"]] = "corrupted", c
                    break
                else:
                    continue
        if line_stack and not row["syntex"]:
            row[["syntex", "error"]] = "incomplete", "".join(line_stack)
    incomplete_df = entry_df.loc[entry_df.syntex=="incomplete"]

    def _score(line):
        stack, score = [], 0
        for s in line:
            stack.append(COMPLETE_POINT_MAP[INVERSE_CHUNK_MAP[s]])
        for p in stack[::-1]:
            score = score*5 + p
        return score
    incomplete_df["score"] = incomplete_df["error"].apply(_score)
    print(incomplete_df)
    print(incomplete_df["score"].median())

if __name__ == "__main__":
    puzzle1(278475)
    puzzle2(3015539998)
