import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools

def day_():
    year = int(os.getcwd().split('\\')[-1][-4:]) 
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
    patterns = []
    for pattern in raw.split('\n\n'):
        patterns.append([[*line] for line in pattern.split('\n') if line])
        
    return patterns
    
def count_flaws_in_rows(idx1, idx2, p):
    flaws = 0
    for i in range(len(p[idx1])):
        if p[idx1][i] != p[idx2][i]:
            flaws += 1
    return flaws

def count_flaws_in_cols(idx1, idx2, p):
    flaws = 0
    for i in range(len(p)):
        if p[i][idx1] != p[i][idx2]:
            flaws += 1
    return flaws

def count_reflection_flaws(p, row = None, col = None):
    flaws = 0
    if row is not None:
        y1 = row
        y2 = row+1
        while 0 <= y1 and y2 < len(p):
            flaws += count_flaws_in_rows(y1, y2, p)
            y1 -= 1
            y2 += 1
        return flaws
    elif col is not None:
        x1 = col
        x2 = col+1
        while 0 <= x1 and x2 < len(p[0]):
            flaws += count_flaws_in_cols(x1, x2, p)
            x1 -= 1
            x2 += 1
        return flaws

def get_reflection_val(p, allowed_flaws = 0):
    for row in range(len(p)-1):
        if count_reflection_flaws(p, row = row) == allowed_flaws:
            return (row+1)*100
    for col in range(len(p[0])-1):
        if count_reflection_flaws(p, col = col) == allowed_flaws:
            return col+1

def star1(patterns):
    return sum(get_reflection_val(p) for p in patterns)

def star2(patterns):
    return sum(get_reflection_val(p, allowed_flaws = 1) for p in patterns)
    

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