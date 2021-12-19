"""
"""
from itertools import combinations
import math
import re
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/19/input"


def puzzle1(answer=None):
    if answer:
        return answer
    pd.set_option('display.max_rows', 200)
    raw_input = get_input(INPUT_URL)
    scanners = re.split(r"--- scanner \d+ ---", raw_input.strip())
    scanner_num, scanner_dfs, beacon_count = 0, [], []
    for s in scanners:
        if s:
            temp_df = pd.DataFrame(s.strip().split())
            temp_df[["d1", "d2", "d3"]] = pd.DataFrame(temp_df[0].str.split(",").values.tolist())
            temp_df["scanner_num"] = scanner_num
            temp_df["beacon_num"] = temp_df.index
            scanner_num += 1
            scanner_dfs.append(temp_df.drop(columns=0).astype(int))
            beacon_count.append(temp_df.index.max() + 1)
    scanner_df = pd.concat(scanner_dfs).reset_index(drop=True)

    # find matching beacons based on their relative distances
    distance_dfs = []
    for i in range(scanner_num):
        distances = []
        for a, b in combinations(scanner_df.loc[scanner_df.scanner_num == i].values.tolist(), 2):
            d2 = (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2
            distances.append((i, a[4], b[4], d2))
        distance_dfs.append(pd.DataFrame(distances, columns=["scanner_num", "beacon_a", "beacon_b", "distance"]))
    
    base_df, total_beacon, matched, if_proceed = distance_dfs[0], beacon_count[0], [0], True
    while if_proceed:
        if_proceed = False  # become true if there is any update to the base_df
        for i in range(1, len(distance_dfs)):
            if i in matched:
                continue
            overlap_df = base_df.merge(distance_dfs[i], on="distance", how="inner")
            # remove same distance by chance
            for sc, sc_c in overlap_df.groupby("scanner_num_x").size().to_dict().items():
                if sc_c == 1:  # approach 1: single distance matching for a scanner must be by coincidance
                    overlap_df = overlap_df.loc[overlap_df.scanner_num_x != sc]
            beacons = pd.DataFrame(overlap_df[["beacon_a_y", "beacon_b_y"]].stack().values, columns=["b"]).groupby("b").size()
            overlap_number = beacons.loc[beacons > 2].size  # approach 2: same logic on the other side 
            print(i, overlap_number, len(overlap_df.drop_duplicates(subset=["distance"])))
            if overlap_number >= 12:
                if len(overlap_df.drop_duplicates(subset=["distance"])) != int(overlap_number * (overlap_number-1) / 2):
                    print(overlap_df.sort_values(["beacon_a_y", "beacon_b_y"]))
                base_df = base_df.append(distance_dfs[i]).reset_index(drop=True)
                total_beacon += beacon_count[i] - overlap_number
                matched.append(i)
                if_proceed = True
    #print(base_df)
    print(total_beacon)


def puzzle2(answer=None):
    if answer:
        return answer
    pd.set_option('display.max_rows', 200)
    raw_input = get_input(INPUT_URL)
    scanners = re.split(r"--- scanner \d+ ---", raw_input.strip())
    scanner_num, scanner_dfs, beacon_count = 0, [], []
    for s in scanners:
        if s:
            temp_df = pd.DataFrame(s.strip().split())
            temp_df[["d1", "d2", "d3"]] = pd.DataFrame(temp_df[0].str.split(",").values.tolist())
            temp_df["scanner_num"] = scanner_num
            temp_df["beacon_num"] = temp_df.index
            scanner_num += 1
            scanner_dfs.append(temp_df.drop(columns=0).astype(int))
            beacon_count.append(temp_df.index.max() + 1)
    scanner_df = pd.concat(scanner_dfs).reset_index(drop=True) 
    # print(scanner_df)

    distance_dfs = []
    for i in range(scanner_num):
        distances = []
        for a, b in combinations(scanner_df.loc[scanner_df.scanner_num == i].values.tolist(), 2):
            d2 = (a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2
            distances.append((i, a[4], b[4], d2))
        distance_dfs.append(pd.DataFrame(distances, columns=["scanner_num", "beacon_a", "beacon_b", "distance"]))
    
    base_df, total_beacon, matched, if_proceed, scanner_position_map = distance_dfs[0], beacon_count[0], [0], True, {0:[0,0,0]}
    while if_proceed:
        if_proceed = False
        for i in range(1, len(distance_dfs)):
            if i in matched:
                continue
            overlap_df = base_df.merge(distance_dfs[i], on="distance", how="inner")
            # remove same distance by chance
            for sc, sc_c in overlap_df.groupby("scanner_num_x").size().to_dict().items():
                if sc_c == 1:
                    overlap_df = overlap_df.loc[overlap_df.scanner_num_x != sc]
            beacons = pd.DataFrame(overlap_df[["beacon_a_y", "beacon_b_y"]].stack().values, columns=["b"]).groupby("b").size()
            overlap_number = beacons.loc[beacons > 2].size
            print(i, overlap_number)
            if overlap_number >= 12:
                overlap_df = overlap_df.sort_values(["scanner_num_x", "beacon_a_x"]).reset_index(drop=True)
                print(overlap_df.loc[:1])
                s1 = overlap_df.loc[1]["scanner_num_x"]
                s1_b1 = overlap_df.loc[:1, ["beacon_a_x", "beacon_b_x"]].stack().mode().values[0]
                s1_b2 = overlap_df.loc[0, ["beacon_a_x", "beacon_b_x"]].sum() - s1_b1
                s2 = overlap_df.loc[1]["scanner_num_y"]
                s2_b1 = overlap_df.loc[:1, ["beacon_a_y", "beacon_b_y"]].stack().mode().values[0]
                s2_b2 = overlap_df.loc[0, ["beacon_a_y", "beacon_b_y"]].sum() - s2_b1
                s1_b1_coord = np.array(scanner_df.loc[(scanner_df.scanner_num==s1) & (scanner_df.beacon_num==s1_b1), ["d1","d2","d3"]].values[0])
                s1_b2_coord = np.array(scanner_df.loc[(scanner_df.scanner_num==s1) & (scanner_df.beacon_num==s1_b2), ["d1","d2","d3"]].values[0])
                s2_b1_coord = np.array(scanner_df.loc[(scanner_df.scanner_num==s2) & (scanner_df.beacon_num==s2_b1), ["d1","d2","d3"]].values[0])
                s2_b2_coord = np.array(scanner_df.loc[(scanner_df.scanner_num==s2) & (scanner_df.beacon_num==s2_b2), ["d1","d2","d3"]].values[0])
                s1_coord, s2_coord = s1_b1_coord - s1_b2_coord, s2_b1_coord - s2_b2_coord
                # print(s1_coord, s2_coord)
                # print(s1_b1_coord, s2_b1_coord)
                scanner_position_base = scanner_position_map[s1].copy()
                for m, co2 in enumerate(s2_coord):
                    for j, co1 in enumerate(s1_coord):
                        if abs(co2) == abs(co1):
                            # only position difference, not considering the reference scanner position, probably not from (0,0,0)
                            if co1 == co2:
                                change = s2_b1_coord[m]
                            else:
                                change = -s2_b1_coord[m]
                            scanner_position_base[j] = s1_b1_coord[j] - change
                            # reset coordinates if not based from (0,0,0), but direction not changed. Drawing makes it easier.
                            if co1 == co2:  
                                scanner_df.loc[scanner_df.scanner_num==s2, f"d{m+1}"] += scanner_position_base[j]
                            else:
                                scanner_df.loc[scanner_df.scanner_num==s2, f"d{m+1}"] = scanner_position_base[j] - scanner_df.loc[scanner_df.scanner_num==s2, f"d{m+1}"]
                scanner_position_map[s2] = scanner_position_base
                base_df = base_df.append(distance_dfs[i]).reset_index(drop=True)
                total_beacon += beacon_count[i] - overlap_number
                matched.append(i)
                if_proceed = True
    longest_m_distance, s_pair = 0, []
    for s1, s2 in combinations(scanner_position_map.values(), 2):
        m_dis = np.sum(np.absolute(np.array(s2) - np.array(s1)))
        if m_dis > longest_m_distance:
            longest_m_distance = m_dis
            s_pair = [s1, s2]
    print(longest_m_distance, s_pair)
    


if __name__ == "__main__":
    puzzle1(430)
    puzzle2() #11860
