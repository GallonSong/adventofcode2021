"""
today's puzzles are complex and not Pandas-friendly, hence solved them by hand.
some heuristics can be helpful to solve by code, brute force in puzzle-2 seems out of the computing limit.
Heuristics:
1) the 4 end positions are disk storage, as they dont block the hall way;
2) middle 3 storable positions are memory, can only store temporarily;
3) to start, there must be a room being emptied, observe the roommates in different rooms;
4) move between room1 and room4 (A & D) requires an clear hall way (4 storage position maximum);
5) A & D can hardly be stored in hallway (B & C have better movability);
6) a room never has two "door guards" from the same species;
7) more case-specific heuristics.
"""
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/23/input"


def puzzle1(answer=None):
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    for line in raw_input.split("\n"):
        print(line)
    

def puzzle2(answer=None):
    if answer:
        return answer
    folded = ("  #D#C#B#A#", "  #D#B#A#C#")
    raw_input = get_input(INPUT_URL)
    for i, line in enumerate(raw_input.split("\n")):
        if i == 3:
            print(*folded, sep="\n")
        print(line)


if __name__ == "__main__":
    puzzle1(17120)
    puzzle2(47234)
