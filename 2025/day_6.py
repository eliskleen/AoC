import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import defaultdict
import operator


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
    cols = defaultdict(list)
    for row in raw.splitlines():
        col = 0
        for c in row.split():
            cols[col].append(c)
            col += 1
    return (cols, raw)
    

def apply(strOp, xs):
    op = operator.add if strOp == "+" else operator.mul
    acc = 0 if strOp == "+" else 1
    return functools.reduce(op, xs, acc)


def star1(data):
    data, _ = data
    tot = 0
    for i in range(len(data)):
        ls = data[i]
        op = ls[-1]
        xs = [int(v) for v in ls[:-1]]
        val = apply(op, xs)
        tot += val 
    return tot
        

def format2(raw):
    cols = defaultdict(list)
    #create grid
    grid = {}
    y = 0
    for row in raw.splitlines():
        for x in range(len(row)):
            grid[(x, y)] = row[x]
        y += 1
    colNum = 0
    #move from bottom right to find each col
    x = len(raw.splitlines()[0]) - 1
    yMax = y -1
    while(x >= 0):
        #find number in col
        num = ""
        op = ""
        y = yMax
        while(y >= 0):
            c = grid[(x, y)]
            if(c == "+" or c == "*"):
                op = c
            else:
                num = c + num
            y -= 1
        num = num.strip()
        if(num != ""):
            cols[colNum].append(num)
        if(op != ""):
            cols[colNum].append(op)
            colNum += 1
        x -= 1
    return cols
def star2(data):
    _, raw = data
    data = format2(raw)
    return star1((data, ""))

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