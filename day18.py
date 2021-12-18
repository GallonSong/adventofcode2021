"""
"""
from itertools import permutations
import math
import re
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/18/input"


def count_level(p):
    max_l, current_l = 0, 0
    for c in str(p):
        if c == "[":
            current_l += 1
        elif c == "]":
            current_l -= 1
        max_l = max(max_l, current_l)
    return max_l


def explode(p):
    p_string = str(p).replace(" ", "")
    p_string_list = list(p_string)
    left_string = p_string

    deepest_leaf, explode_index_span, depth, past_length = "", [], 0, 0
    while re.search(r"(\[\d+,\d+\])", left_string):
        lm = re.search(r"(\[\d+,\d+\])", left_string)
        leaf, left_string = lm.group(1), left_string[lm.end():]
        current_depth = p_string[:lm.start()+past_length].count("[") - p_string[:lm.start()+past_length].count("]")
        if current_depth > depth:
            depth = current_depth
            deepest_leaf, explode_index_span = leaf, [p+past_length for p in lm.span()]
        past_length += lm.end()
    print(deepest_leaf, explode_index_span, depth)
    explode_list = eval(deepest_leaf)
    p_string_list[explode_index_span[0]] = "0"
    for i in range(explode_index_span[0]+1, explode_index_span[1]):
        p_string_list[i] = ""
    l_spill_m = re.search(r"(\d+)\D+$", p_string[:explode_index_span[0]])
    if l_spill_m:
        l_number = int(l_spill_m.group(1))
        spill_index_s, spill_index_e = l_spill_m.span(1)[0], l_spill_m.span(1)[1]
        p_string_list[spill_index_s] = str(l_number + explode_list[0])
        if spill_index_e - spill_index_s > 1:
            for j in range(spill_index_s+1, spill_index_e):
                p_string_list[j] = ""

    r_spill_m = re.search(r"^\D+(\d+)", p_string[explode_index_span[1]:])
    if r_spill_m:
        r_number = int(r_spill_m.group(1))
        spill_index_s, spill_index_e = r_spill_m.span(1)[0], r_spill_m.span(1)[1]
        p_string_list[explode_index_span[1] + spill_index_s] = str(r_number + explode_list[1])
        if spill_index_e - spill_index_s > 1:
            for j in range(spill_index_s+1, spill_index_e):
                p_string_list[explode_index_span[1] + j] = ""
    return eval("".join(p_string_list))

def split(p):
    p_string = str(p).replace(" ", "")
    p_string_list = list(p_string)

    m = re.search(r"(\d\d+)", p_string)
    if m:
        big_number, split_index_span = int(m.group(1)), m.span(1)
        p_string_list[split_index_span[0]] = f"[{int(big_number/2)},{math.ceil(big_number/2)}]"
        for j in range(split_index_span[0]+1, split_index_span[1]):
                p_string_list[j] = ""
    return eval("".join(p_string_list))

def explode_and_split(p):
    while True:
        print(p)
        if count_level(p) == 5:
            p = explode(p)
            continue
        elif any(map(lambda x: len(x)>1, re.findall(r"\d+", str(p)))):
            p = split(p)
            continue
        else:
            return p


def calc_magnitude(p):
    level = count_level(p)
    if level == 0:
        return p
    return calc_magnitude(p[0])*3 + calc_magnitude(p[1])*2


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    number_all = raw_input.strip().split()
    pair_all = eval(number_all[0])
    for number in number_all[1:]:
        pair_all = explode_and_split([pair_all, eval(number)])
    print(calc_magnitude(pair_all))
    

def puzzle2(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    number_permutations = permutations(raw_input.strip().split(), 2)
    biggest = 0
    for permtt in number_permutations:
        magn = calc_magnitude(explode_and_split(list(map(eval, permtt))))
        if magn > biggest:
            biggest = magn
    print(biggest)


if __name__ == "__main__":
    puzzle1(3665)
    puzzle2(4775)
