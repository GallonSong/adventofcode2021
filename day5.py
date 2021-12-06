"""
By these 2 puzzles, it is more realized that, in data science, it is much harder to generate 
reasonable/good/accurate results than random ones. Then, how should we examine our results
without the given ultimate correct answer?
Another thing learned today is that it is so natural to build upon existing solutions,
but old hypotheses should be rethought because they might no longer stand in new situations.
(x0,x1 -> x_low,x_high)
"""
import pandas as pd
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/5/input"


def puzzle1(answer=None):
    """Get coordinates of all vents by the explode action, then aggregate"""
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    vent_df = pd.DataFrame(raw_input.rstrip().split("\n"), columns=["line"])
    vent_end_df = vent_df["line"].str.split(" -> |,", expand=True).rename(columns={0:"x0", 1:"y0", 2:"x1", 3:"y1"}).astype(int)
    # Vertical lines
    vertical_df = vent_end_df[vent_end_df["x0"]==vent_end_df["x1"]]
    vertical_df["y_start"] = vertical_df[["y0", "y1"]].min(axis=1)  # make range easier as direction does not matter
    vertical_df["y_end"] = vertical_df[["y0", "y1"]].max(axis=1)
    vertical_df["y"] = vertical_df.apply(lambda v: range(v["y_start"], v["y_end"]+1), axis=1)
    cord_v_df = vertical_df[["x0", "y"]].explode("y").rename(columns={"x0": "x"})
    # Horizontal lines
    horizontal_df = vent_end_df[vent_end_df["y0"]==vent_end_df["y1"]]
    horizontal_df["x_start"] = horizontal_df[["x0", "x1"]].min(axis=1)
    horizontal_df["x_end"] = horizontal_df[["x0", "x1"]].max(axis=1)
    horizontal_df["x"] = horizontal_df.apply(lambda v: range(v["x_start"], v["x_end"]+1), axis=1)
    cord_h_df = horizontal_df[["x", "y0"]].explode("x").rename(columns={"y0": "y"})
    cord_df = pd.concat([cord_v_df, cord_h_df]).reset_index(drop=True)

    overlap_df = cord_df.groupby(["x", "y"] ,as_index=False).size()
    print(overlap_df[overlap_df["size"] > 1].count())


def puzzle2(answer=None):
    """
    Get coordinates of all vents by the explode action, then aggregate.
    With diagonal lines, it is a matter how to populate the coordinates, which can bring some tricky mistakes.
    1) the coordinates cannot be sorted as the vertical/horizontal ones;
    2) it is less easy to take the range end (+1) into consideration than the step_size.
    Otherwise it is similar process as puzzle1.
    """
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    vent_df = pd.DataFrame(raw_input.rstrip().split("\n"), columns=["line"])
    vent_end_df = vent_df["line"].str.split(" -> |,", expand=True).rename(columns={0:"x0", 1:"y0", 2:"x1", 3:"y1"}).astype(int)
    
    vent_end_df["y_start"] = vent_end_df[["y0", "y1"]].min(axis=1)
    vent_end_df["y_end"] = vent_end_df[["y0", "y1"]].max(axis=1)
    vent_end_df["x_start"] = vent_end_df[["x0", "x1"]].min(axis=1)
    vent_end_df["x_end"] = vent_end_df[["x0", "x1"]].max(axis=1)
    # Diagonal lines
    diagonal_df = vent_end_df[vent_end_df["x_end"]-vent_end_df["x_start"] == vent_end_df["y_end"]-vent_end_df["y_start"]]
    def _get_diagonal_cord(row):
        x_step = 1 if row["x1"] >= row["x0"] else -1  # Notice: "start(low)/end(high)" no longer valid
        y_step = 1 if row["y1"] >= row["y0"] else -1
        x_cords = range(row["x0"], row["x1"]+x_step, x_step)  # Notice: the step should go with the range end, too
        y_cords = range(row["y0"], row["y1"]+y_step, y_step)
        return list(zip(x_cords, y_cords))
    diagonal_df["cord"] = diagonal_df.apply(_get_diagonal_cord, axis=1)
    cord_d_df = pd.DataFrame(diagonal_df["cord"].explode().tolist(), columns=["x", "y"])
    # Vertical lines
    vertical_df = vent_end_df[vent_end_df["x0"]==vent_end_df["x1"]]
    vertical_df["y"] = vertical_df.apply(lambda v: range(v["y_start"], v["y_end"]+1), axis=1)
    cord_v_df = vertical_df[["x0", "y"]].explode("y").rename(columns={"x0": "x"})
    # Horizontal lines
    horizontal_df = vent_end_df[vent_end_df["y0"]==vent_end_df["y1"]]
    horizontal_df["x"] = horizontal_df.apply(lambda v: range(v["x_start"], v["x_end"]+1), axis=1)
    cord_h_df = horizontal_df[["x", "y0"]].explode("x").rename(columns={"y0": "y"})
    cord_df = pd.concat([cord_d_df, cord_v_df, cord_h_df]).reset_index(drop=True)

    overlap_df = cord_df.groupby(["x", "y"] ,as_index=False).size()
    print(overlap_df[overlap_df["size"] > 1].count())


if __name__ == "__main__":
    puzzle1(6710)
    puzzle2(20121)
