"""
"""
from itertools import product
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/20/input"


def extend(df, padding):
    extend_pixel = []
    p_min, p_max = df.x.min()-1, df.x.max()+1
    extend_pixel += product([p_min, p_max], range(p_min, p_max+1))
    extend_pixel += product(range(p_min+1, p_max), [p_min, p_max])
    extend_df = pd.DataFrame(extend_pixel, columns=["x", "y"])
    extend_df["light"] = padding
    return extend_df


def show(df):
    df = df.reset_index()
    for _, row in df.replace("0", " ").pivot(index="x", columns="y", values="light").iterrows():
        print("".join(row.values))


def puzzle1(answer=None):
    if answer:
        return answer
    pd.set_option('display.max_rows', 200)
    raw_input = get_input(INPUT_URL)
    # watch out: the first enhancement element is #, which means the infinite paddings will become 1 after the first enhancement
    enhancement = raw_input.split()[0].replace(".", "0").replace("#", "1")
    entry_df = pd.DataFrame(raw_input.strip().split("\n\n")[-1].split("\n"), columns=["entry"])
    image_df = pd.DataFrame(entry_df.entry.apply(list).tolist()).stack().reset_index().rename(columns={"level_0": "x", "level_1": "y", 0: "light"})
    image_df = image_df.replace({".": "0", "#": "1"})
    
    #show(image_df)
    for step in range(2):
        padding = "0" if step % 2 == 0 else "1"
        image_df = image_df.append(extend(image_df, padding))
        image_df = image_df.sort_values(["x","y"]).reset_index(drop=True)
        image_df["l_y_-1"] = image_df.groupby("x")["light"].shift(1)
        image_df["l_y_+1"] = image_df.groupby("x")["light"].shift(-1)
        image_df.fillna(padding, inplace=True)
        image_df["l_y"] = image_df["l_y_-1"] + image_df["light"] + image_df["l_y_+1"]
        image_df = image_df.sort_values(["y","x"]).reset_index(drop=True)
        image_df["l_x_-1"] = image_df.groupby("y")["l_y"].shift(1)
        image_df["l_x_+1"] = image_df.groupby("y")["l_y"].shift(-1)
        image_df.fillna(padding*3, inplace=True)
        image_df["l_mask"] = image_df["l_x_-1"] + image_df["l_y"] + image_df["l_x_+1"]
        image_df["light"] = image_df["l_mask"].apply(lambda x: enhancement[int(x, 2)])
        show(image_df)
        print(image_df.groupby("light").size())

    #print(image_df)
    

def puzzle2(answer=None):
    if answer:
        return answer
    print("same as puzzle 1, change iteration from 2 to 50")

            
if __name__ == "__main__":
    puzzle1(4928)
    puzzle2(16605)
