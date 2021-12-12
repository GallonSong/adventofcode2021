"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/12/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    entry_df[["starts", "ends"]] = entry_df["entry"].str.split("-", expand=True)
    edge_df = entry_df.append(entry_df.rename(columns={"starts": "ends", "ends": "starts"}))
    edge_df = edge_df.loc[(edge_df.starts != "end") & (edge_df.ends != "start"), ["starts", "ends"]].drop_duplicates().reset_index(drop=True)
    paths = edge_df.loc[edge_df.starts == "start", "ends"].values.tolist()
    print(paths, edge_df)
    finished_paths = []
    while paths:
        new_paths = []
        for p in paths:      
            for node in edge_df.loc[edge_df.starts == p.split(",")[-1], "ends"].values:
                if node == "end":
                    finished_paths.append(p)
                elif node.islower() and node in p:
                    continue
                else:
                    new_paths.append(p + "," + node)
        paths = new_paths
    print(len(finished_paths))


def puzzle2(answer=None):
    """
    """
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    entry_df[["starts", "ends"]] = entry_df["entry"].str.split("-", expand=True)
    edge_df = entry_df.append(entry_df.rename(columns={"starts": "ends", "ends": "starts"}))
    edge_df = edge_df.loc[(edge_df.starts != "end") & (edge_df.ends != "start"), ["starts", "ends"]].drop_duplicates().reset_index(drop=True)
    paths = edge_df.loc[edge_df.starts == "start", "ends"].values.tolist()
    print(edge_df)
    finished_paths = []
    def _double_visited(path):
        small_caves = list(filter(lambda n: n.islower(), path.split(",")))
        return len(set(small_caves)) < len(small_caves)
    while paths:
        new_paths = []
        for p in paths:      
            for node in edge_df.loc[edge_df.starts == p.split(",")[-1], "ends"].values:
                if node == "end":
                    finished_paths.append(p)
                elif node.islower() and node in p and _double_visited(p):
                    continue
                else:
                    new_paths.append(p + "," + node)
        paths = new_paths
    print(len(finished_paths))


if __name__ == "__main__":
    puzzle1(5228)
    puzzle2(131228)
