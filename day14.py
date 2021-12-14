"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/14/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    template_df = pd.DataFrame(list(entry_df.loc[0, "entry"]), columns=["code"])
    mapping_df = entry_df.loc[2:, "entry"].str.split(" -> ", expand=True).rename(columns={0: "codes", 1: "match"}).reset_index(drop=True)
    for _ in range(10):
        template_df["code_2"] = template_df["code"] + template_df.code.shift(-1)
        for i, row in template_df.loc[~template_df.code_2.isnull()].iterrows():
            template_df.loc[i, "code_2"] = mapping_df.loc[mapping_df.codes==row.code_2, "match"].values[0]
        template_df = pd.DataFrame(template_df.stack().reset_index(drop=True), columns=["code"])
    sizes = template_df.groupby("code").size()
    print(sizes.max() - sizes.min())


def puzzle2(answer=None):
    """
    """
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    entry_df = pd.DataFrame(raw_input.strip().split("\n"), columns=["entry"])
    template_df = pd.DataFrame(list(entry_df.loc[0, "entry"]), columns=["code"])
    end_code = template_df.iloc[-1]["code"]
    code_mapping = entry_df.loc[2:, "entry"].str.split(" -> ", expand=True).set_index(0).to_dict()[1]
    template_df["code_2"] = template_df["code"] + template_df.code.shift(-1)
    agg_df = template_df.groupby("code_2").size().reset_index().rename(columns={0: "number"})
    for _ in range(40):
        agg_df["new_code"] = agg_df["code_2"].map(code_mapping)
        agg_df["code_2"] = agg_df.apply(lambda r: [r["code_2"][0]+r["new_code"], r["new_code"]+r["code_2"][1]], axis=1)
        agg_df = agg_df[["code_2", "number"]].explode("code_2").groupby("code_2").sum("number").reset_index()
    agg_df.code_2 = agg_df.code_2.str[0]
    size_df = agg_df.groupby("code_2").sum("v").reset_index()
    size_df.loc[size_df.code_2==end_code, "number"] += 1
    print(size_df)
    print(size_df.number.max() - size_df.number.min())


if __name__ == "__main__":
    puzzle1(2947)
    puzzle2(3232426226464)
