from collections import defaultdict
import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from shapely.geometry import Point, Polygon

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
    inst = []
    for row in raw.split('\n'):
        row = row.split(' ')
        row[2] = row[2].removeprefix('(').removesuffix(')')
        inst.append((row[0], int(row[1]), row[2]))
    return inst
    

op_to_dir = {'R' : (1, 0), 'L' : (-1, 0), 'U' : (0, -1), 'D' : (0, 1)}
def sholace(insts):
    xs = []
    ys = []
    xs.append(0)
    ys.append(0)
    x = 0
    y = 0
    edge_volume = 0
    for (op, arg, _) in insts:
        dir = op_to_dir[op]
        x += dir[0] * arg
        y += dir[1] * arg
        edge_volume += arg
        xs.append(x)
        ys.append(y)
    xs2 = xs[1:] + [xs[0]]
    ys2 = ys[1:] + [ys[0]]
    s1 = (sum(list(map(lambda xy: xy[0]*xy[1], zip(xs, ys2)))))
    s2 = (sum(list(map(lambda xy: xy[0]*xy[1], zip(xs2, ys)))))
    s = int(abs(s1 - s2) / 2 + (edge_volume / 2)) +1
    return s

def star1(data):
    return sholace(data)

            

v_to_dir = {0 : 'R', 1 : 'D', 2 : 'L', 3 : 'U'}

def star2(data):
    # return 0
    insts = []
    for (_, _, h) in data:
        h = h.removeprefix('#')
        arg = int(h[:5], base=16)
        v = int(h[5:], base=16)
        op = v_to_dir[v]
        insts.append((op, arg, h))

    # print(len(insts))


    return sholace(insts)

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