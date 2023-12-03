import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools

def day_():
    year = int(os.getcwd().split('\\')[-1][:4]) 
    day = int(__file__.split('\\')[-1].split('_')[1].split('.')[0])
    puzzle = Puzzle(year=year, day=day) 
    submit_a = "a" in sys.argv
    submit_b = "b" in sys.argv
    example = "e" in sys.argv

    if (submit_a or submit_b) and example:
        print("Cannot submit examples")
        return

    raw_data = puzzle.input_data
    if example:
        print("Using example")
        #use 'aocd year day --example' to get the example data
        with open('example.txt', 'r') as f:
            raw_data = f.read()

            
    start_time = time.perf_counter()
    data = format_data(raw_data)

    time1 = time.perf_counter()

    ans1 = star1(data)
    time2 = time.perf_counter()

    ans2 = star2(data)
    time3 = time.perf_counter()

    load_time = time1 - start_time
    star1_time = time2 - time1
    star2_time = time3 - time2

    if submit_a:
        print("Submitting star 1")
        puzzle.answer_a = ans1
    if submit_b:
        print("Submitting star 2")
        puzzle.answer_b = ans2
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 time: {star1_time}')
        print(f'Star 2 time: {star2_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: {ans2}')


def format_data(raw):
    numbers = []
    lines = raw.split('\n')

    for y in range(len(lines)):
        line = lines[y]
        x = 0
        while x < len(line):
            c = line[x]
            if c.isdigit():
                start = x
                while x < len(line) and line[x].isdigit():
                    x += 1
                numbers.append((int(line[start:x]), (start, y)))
            else:
                x += 1

    return (lines, numbers)
    
def star1(data):
    (lines, numbers) = data
    ret = 0
    for (num, (x0, y0)) in numbers:
        found = False
        for (dx, dy) in directions:
            for i in range(len(str(num))):
                x = x0 + dx + i
                y = y0 + dy
                if y >= len(lines) or y < 0 or x >= len(lines[y]) or x < 0:
                    break
                if not lines[y][x].isdigit() and not lines[y][x] == '.':
                    ret += num
                    found = True
                    break
            if found:
                break
    return ret



directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
def star2(data):
    (lines, numbers) = data
    dict = {}
    for (num, (x0, y0)) in numbers:
        for i in range(len(str(num))):
            x = x0 + i
            y = y0
            dict[(x, y)] = (num, x0, y0)
    ret = 0
    for y0, line in enumerate(lines):
        for x0, c in enumerate(line):
            if c == '*':
                valid = False
                n1, n2  = None, None
                for (dx, dy) in directions:
                    x = x0 + dx
                    y = y0 + dy
                    if (x, y) in dict:
                        if n1 is None:
                            n1 = dict[(x, y)]
                        elif n1 != dict[(x, y)]:
                            n2 = dict[(x, y)]
                            valid = True
                        if valid and (n1 != dict[(x, y)] and n2 != dict[(x, y)]):
                            valid = False
                if valid:
                    ret += n1[0] * n2[0]
    return ret

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    day = int(__file__.split('\\')[-1].split('_')[1].split('.')[0]) 
    stats.dump_stats(filename = f'profiling\\profiling{day}.prof')

# run with `py day_n.py -- a b` to submit both stars for day n
if __name__ == '__main__':
    main()