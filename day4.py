import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/4/input"


def puzzle1(answer=None):
    if answer:
        return answer
    # Set-up. add col, row, and board to facilitate aggregation
    raw_input = get_input(INPUT_URL)
    sequence = raw_input.split()[0].split(",")
    board_df = pd.DataFrame(raw_input.split()[1:], columns=["number"])
    board_dim = 5
    number_of_row = int(len(board_df) / board_dim)
    number_of_board = int(len(board_df) / board_dim / board_dim)
    board_df["col"] = np.tile(np.arange(5), number_of_row)
    board_df["row"] = np.arange(number_of_row).repeat(5)
    board_df["board"] = np.arange(number_of_board).repeat(25)
    board_df["mark"] = False
    # Mark numbers. Check col/row completion
    for mark in sequence:
        board_df.loc[board_df["number"]==mark, "mark"] = True
        col_check_df = board_df.groupby(["col", "board"]).all()
        row_check_df = board_df.groupby(["row", "board"]).all()
        print(mark, len(board_df.loc[board_df["mark"]==True]))
        if col_check_df["mark"].any():
            bingo_col = col_check_df.loc[col_check_df["mark"]==True]
            bingo_board = bingo_col.index[0][1]
            print(board_df.loc[(board_df["board"] == bingo_col.index[0][1]) & (board_df["col"] == bingo_col.index[0][0])])
            break
        elif row_check_df["mark"].any():
            bingo_row = row_check_df.loc[row_check_df["mark"]==True]
            bingo_board = bingo_row.index[0][1]
            print(board_df.loc[(board_df["board"] == bingo_row.index[0][1]) & (board_df["row"] == bingo_row.index[0][0])])
            break
    print("Unmarked: ", len(board_df.loc[board_df["mark"]==False]))
    print(mark)
    print(int(mark) * sum(board_df.loc[(board_df["mark"]==False) & (board_df["board"] == bingo_board), "number"].astype(int)))


def puzzle2(answer=None):
    if answer:
        return answer
    # Set-up. add UNIT (col&row) and board to facilitate aggregation
    raw_input = get_input(INPUT_URL)
    sequence = raw_input.split()[0].split(",")
    board_df = pd.DataFrame(raw_input.split()[1:], columns=["number"])
    board_dim = 5
    number_of_row = int(len(board_df) / board_dim)
    number_of_board = int(len(board_df) / board_dim / board_dim)
    board_df["board"] = np.arange(number_of_board).repeat(25)
    board_df_row = board_df.copy()
    board_df["unit"] = np.tile(np.arange(5), number_of_row)
    board_df_row["unit"] = np.tile(np.arange(5).repeat(5), number_of_board) + 100
    unit_df = pd.concat([board_df, board_df_row]).reset_index(drop=True)  # Note: the number is doubled after this step!
    unit_df["mark"] = False
    # Mark numbers. Check unit completion => check board completion
    for mark in sequence:
        unit_df.loc[unit_df["number"]==mark, "mark"] = True
        unit_check_df = unit_df.groupby(["unit", "board"]).all()["mark"].reset_index()
        board_check_df = unit_check_df.groupby("board").any()
        if len(board_check_df.loc[board_check_df["mark"]==False]) == 1:
            last_board = board_check_df.loc[board_check_df["mark"]==False].index[0]
        elif board_check_df["mark"].all():
            print(unit_df.loc[(unit_df["board"]==last_board)])
            unmarked_sum = sum(unit_df.loc[(unit_df["board"]==last_board) & (unit_df["mark"]==False) & (unit_df["unit"] < 100), "number"].astype(int))  # Note: remove the duplicate units before aggregation
            print(last_board, mark, unmarked_sum)
            print(int(mark) * unmarked_sum)
            break


if __name__ == "__main__":
    puzzle1(89001)
    puzzle2(7296)
