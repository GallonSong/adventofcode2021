"""
There are 2 patterns for z on each digit: 1) multiply by 26, 2) divide by 26.
Given that x works as 0/1 conditions to decide which pattern, 
to achieve z13 = 0, there must be 7 multiplications and 7 divisions,
so all x conditions must be fulfilled.

Not pandas at all, brute force does not work due to complexity,
find heuristic rules instead, solved almost by hand, code helps with verification though.
"""
from operator import add, mul, floordiv, mod, eq
from misc import get_input

INPUT_URL = "https://adventofcode.com/2021/day/24/input"


OPERATION_MAPPING = {
    "add": add,
    "mul": mul,
    "div": floordiv,
    "mod": mod,
    "eql": lambda a,b: int(eq(a,b))
}


def update_digit(digits, desc=True):
    added, new_d = (-1, "9") if desc else (1, "1")
    new_digits_r = list(str(int(digits)+added))[::-1]
    for i, d in enumerate(new_digits_r):
        if d == "0":
            if i < 13:
                new_digits_r[i] = new_d
                new_digits_r[i+1] = str(int(new_digits_r[i+1])+added)
            else:
                return False
    return "".join(new_digits_r[::-1])


def operate(instruction, mem):
    operator, a, b = instruction.split(" ")
    a_value = mem[a]
    b_value = mem[b] if b in mem else int(b)
    mem[a] = OPERATION_MAPPING[operator](a_value, b_value)
    return mem
    

def check(alu, memory):
    """
    >>>>>>>>>>> heuristic, got by ALU interpretation and hand calculation:
    z0 = w0 + 8
    z1 = 26*z0 + w1 + 13
    z2 = 26*z1 + w2 + 8
    z3 = 26*z2 + w3 + 10
    -----====== start dividing
    z4 = z2 (w3 - 1 = w4)
    z5 = z1 (w2 - 5 = w5)
    z6 = 26*z5 + w6 + 13
    z7 = 26*z6 + w7 + 5
    z8 = z6 (w7 + 3 = 28)
    z9 = z5 (w6 + 7 = w9)
    z10 = 26*z9 + w10 + 2
    z11 = z9 (w10 + 2 = w11)
    z12 = z5 // 26 (w12 = z1 % 26 - 15)
    z13 = (z5 // 26) // 26 (w0 + 4 = w13)
    <<<<<<<<<<
    """
    for instruction in alu.split("\n"):
        if instruction:
            memory = operate(instruction, memory)
    return memory


def puzzle1(answer=None):
    """
    z1 = z5 = z9 = z11
    w3 - 1 = w4
    w2 - 5 = w5
    w0 + 4 = w13
    w7 + 3 = w8
    w6 + 7 = w9
    w10 + 2 = w11
    w12 = z1 % 26 - 15
    """
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    monad_chunks = raw_input.strip().split("inp w\n")[1:]
    fourteen_digits = "59998426997999"
    while fourteen_digits:
        memory = {"x": 0, "y": 0, "z": 0, "w": 0}
        for i in range(14):
            memory["w"] = int(str(fourteen_digits[i]))
            memory = check(monad_chunks[i], memory)
            # print(i, memory)
        print(fourteen_digits, memory)
        if memory["z"] == 0:
            print("Found!")
            break
        fourteen_digits = update_digit(fourteen_digits, desc=True)


def puzzle2(answer=None):
    """
    z1 = z5 = z9 = z11
    w3 - 1 = w4
    w2 - 5 = w5
    w0 + 4 = w13
    w7 + 3 = w8
    w6 + 7 = w9
    w10 + 2 = w11
    w12 = z1 % 26 - 15
    """
    if answer:
        return answer
    raw_input = get_input(INPUT_URL)
    monad_chunks = raw_input.strip().split("inp w\n")[1:]
    fourteen_digits = "13621111481311"  # watch out the necessary condition for w12
    while fourteen_digits:
        memory = {"x": 0, "y": 0, "z": 0, "w": 0}
        for i in range(14):
            memory["w"] = int(str(fourteen_digits[i]))
            memory = check(monad_chunks[i], memory)
            # print(i, memory)
        print(fourteen_digits, memory)
        if memory["z"] == 0:
            print("Found!")
            break
        fourteen_digits = update_digit(fourteen_digits, desc=False)


if __name__ == "__main__":
    puzzle1(59998426997979)
    puzzle2(13621111481315)
