import pandas as pd
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/3/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    diagnostic_df = pd.DataFrame(raw_input.split(), columns=["signal"])
    signal_df = diagnostic_df["signal"].str.split("", expand=True).drop(columns=[0, 13]).astype(int)

    gamma_df = signal_df.mode()
    epsilon_df = 1 - gamma_df
    gamma = int("".join(gamma_df.astype(str).iloc[0]), 2)
    epsilon = int("".join(epsilon_df.astype(str).iloc[0]), 2)
    print(gamma * epsilon)


def puzzle2(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    diagnostic_df = pd.DataFrame(raw_input.split(), columns=["signal"])
    signal_df = diagnostic_df["signal"].str.split("", expand=True).drop(columns=[0, 13]).astype(int)
    single_cols = signal_df.columns
    signal_df["signal"] = diagnostic_df["signal"]

    def _get_rate(count_df, rate_type):
        if count_df.max() == count_df.min():
            return "1" if rate_type == "o2" else "0"
        else:
            return str(count_df.idxmax()) if rate_type == "o2" else str(count_df.idxmin())
        
    o2_str, co2_str = "", ""
    o2_df, co2_df = signal_df.copy(), signal_df.copy()
    o2, co2 = 0, 0
    for col in single_cols:
        o2_rate = _get_rate(o2_df[col].value_counts(), "o2")
        co2_rate = _get_rate(co2_df[col].value_counts(), "co2")
        o2_str += o2_rate
        co2_str += co2_rate

        o2_df = o2_df[o2_df["signal"].str.startswith(o2_str)]
        co2_df = co2_df[co2_df["signal"].str.startswith(co2_str)]
        if o2 == 0 and len(o2_df) == 1:
            print(o2_str, o2_df)
            o2 = int(o2_df["signal"].iloc[0], 2)
        if co2 == 0 and len(co2_df) == 1:
            print(co2_str, co2_df)
            co2 = int(co2_df["signal"].iloc[0], 2)
        if o2 and co2:
            print(o2 * co2)


if __name__ == "__main__":
    puzzle1(3958484)
    puzzle2(1613181)
