"""
"""
import pandas as pd
import numpy as np
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/16/input"

def operate(operator, values):
    return [
        sum,
        np.prod,
        min,
        max,
        print,
        lambda x: 1 if x[0] > x[1] else 0,
        lambda x: 1 if x[0] < x[1] else 0,
        lambda x: 1 if x[0] == x[1] else 0
    ][operator](values)
    

def decode_packets_num(packets, versions=[], number=1, operator=None):
    p_start, results = 0, []
    for _ in range(number):
        p_version, p_type = int(packets[p_start:p_start+3], 2), int(packets[p_start+3:p_start+6], 2)
        versions.append(p_version)
        if p_type == 4:
            p_start += 6
            value = ""
            while packets[p_start] == "1":  # not last group
                value += packets[p_start+1:p_start+5]
                p_start += 5
            value += packets[p_start+1:p_start+5]  # last group
            p_start += 5
            results.append(int(value, 2))
        else:
            if packets[p_start+6] == "0":  # length_type_id 0: 
                length = int(packets[p_start+7:p_start+7+15], 2)
                versions, result = decode_packets_len(packets[p_start+7+15:p_start+7+15+length], versions, length, p_type)
                p_start += 7 + 15 + length
            else:  # length_type_id 1
                number = int(packets[p_start+7:p_start+7+11], 2)
                versions, p_start_move, result = decode_packets_num(packets[p_start+7+11:], versions, number, p_type)
                p_start += 7 + 11 + p_start_move
            results.append(result)
    
    return versions, p_start, operate(operator, results) if operator is not None else results


def decode_packets_len(packets, versions, p_length, operator=None):
    p_start, results = 0, []
    while p_start < p_length-1:
        p_version, p_type = int(packets[p_start:p_start+3], 2), int(packets[p_start+3:p_start+6], 2)
        versions.append(p_version)
        if p_type == 4:
            p_start += 6
            value = ""
            while packets[p_start] == "1":  # not last group
                value += packets[p_start+1:p_start+5]
                p_start += 5
            value += packets[p_start+1:p_start+5]  # last group
            p_start += 5
            results.append(int(value, 2))
        else:
            if packets[p_start+6] == "0":  # length_type_id 0: 
                length = int(packets[p_start+7:p_start+7+15], 2)
                versions, result = decode_packets_len(packets[p_start+7+15:p_start+7+15+length], versions, length, p_type)
                p_start += 7 + 15 + length
            else:  # length_type_id 1
                number = int(packets[p_start+7:p_start+7+11], 2)
                versions, p_start_move, result = decode_packets_num(packets[p_start+7+11:], versions, number, p_type)
                p_start += 7 + 11 + p_start_move
            results.append(result)
    
    return versions, operate(operator, results) if operator is not None else results



def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL).strip()
    bin_packet = bin(int(raw_input, 16))[2:].zfill(len(raw_input*4))
    versions, *_ = decode_packets_num(bin_packet)
    print(sum(map(int, versions)))
    

def puzzle2(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL).strip()
    bin_packet = bin(int(raw_input, 16))[2:].zfill(len(raw_input*4))
    *_, results = decode_packets_num(bin_packet)
    print(results)


if __name__ == "__main__":
    puzzle1(991)
    puzzle2(1264485568252)
