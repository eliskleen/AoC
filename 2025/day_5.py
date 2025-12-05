import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from functools import cmp_to_key


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
    lines = raw.splitlines()
    empty = lines.index("")
    rangeLines = lines[:empty]
    idLines = lines[empty+1:]
    ranges = []
    for line in rangeLines:
        ranges.append((int(line.split("-")[0]), int(line.split("-")[1]))) 
    
    ids = [int(line) for line in idLines]
    return (ranges, ids)

    
def star1(data):
    (ranges, ids) = data 
    fresh = 0
    for id in ids:
        for (a, b) in ranges:
            if(id >= a and id <= b):
                fresh += 1
                break
    return fresh

def compare(r1, r2):
    id = 0
    if(r1[id] < r2[id]):
        return -1
    elif(r1[id] > r2[id]):
        return 1
    else:
        return 0

def star2(data):
    (ranges, ids) = data
    ranges.sort()
    fresRanges = [ranges[0]]
    for r in ranges[1:]:
        fr = fresRanges[-1]
        #starts after last ends, create new
        if(r[0] > fr[1]):
            fresRanges.append(r)
            continue
        #ends outside, extend last range
        if(r[1] > fr[1]): 
            fresRanges[-1] = (fr[0], r[1])

    fresh = 0
    for fr in fresRanges:
        fresh += fr[1] - fr[0] +1


    return fresh
   
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