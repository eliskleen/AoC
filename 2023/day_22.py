from collections import defaultdict
from copy import deepcopy
import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import OrderedDict

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
    blocks = {}
    for i, line in enumerate(raw.split('\n')):
        e1 = tuple(map(int, line.split('~')[0].split(',')))
        e2 = tuple(map(int, line.split('~')[1].split(',')))
        blocks[i] = (e1, e2)
    return blocks
    

def fall(blocks):
    ordered_names = list(blocks.keys())
    ordered_names.sort(key = lambda x: min(blocks[x][0][2], blocks[x][1][2]))
    #height and what block is at that height
    ground = defaultdict(lambda: (0, None))
    #name to positions of the fallen blocks
    fallen = {}
    #name to what it is supported by
    supported_by = defaultdict(set)
    #name to what it supports
    supports = defaultdict(set)
    name_map = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    for name in ordered_names:
        e1, e2 = blocks[name]
        diff_x = e2[0] - e1[0]
        diff_y = e2[1] - e1[1]
        if diff_x != 0 and diff_y != 0:
            exit("not aligned with x or y axis")
        # print("diff_x", diff_x, "diff_y", diff_y)
        if diff_x == 0 and diff_y != 0: #aligned with y axis
            min_y = min(e1[1], e2[1])
            max_y = max(e1[1], e2[1])
            max_z = 0
            for y in range(min_y, max_y + 1):
                max_z = max(max_z, ground[(e1[0], y)][0])
            for y in range(min_y, max_y + 1):
                z, sup = ground[(e1[0], y)]
                if z == max_z and sup is not None:
                    supported_by[name].add(sup)
                    supports[sup].add(name)
            # now we know the max z value this piece will hit
            e1 = (e1[0], e1[1], max_z + 1)
            e2 = (e2[0], e2[1], max_z + 1)
            for y in range(min_y, max_y + 1):
                ground[(e1[0], y)] = (max_z + 1, name)
            fallen[name] = (e1, e2)
        elif diff_y == 0 and diff_x != 0:
            min_x = min(e1[0], e2[0])
            max_x = max(e1[0], e2[0])
            max_z = 0
            for x in range(min_x, max_x + 1):
                max_z = max(max_z, ground[(x, e1[1])][0])
            for x in range(min_x, max_x + 1):
                z, sup = ground[(x, e1[1])]
                if z == max_z and sup != None:
                    supported_by[name].add(sup)
                    supports[sup].add(name)
            # now we know the max z value this piece will hit
            e1 = (e1[0], e1[1], max_z + 1)
            e2 = (e2[0], e2[1], max_z + 1)
            for x in range(min_x, max_x + 1):
                ground[(x, e1[1])] = (max_z + 1, name)
            fallen[name] = (e1, e2)
        else: #we have a vertical piece
            x, y = e1[0], e1[1]
            ground_z, sup = ground[(x, y)]
            diff_z = abs(e2[2] - e1[2])
            if e1[2] < e2[2]:
                e1 = (x, y, ground_z + 1)
                e2 = (x , y, ground_z + 1 + diff_z)
            else:
                e1 = (x, y, ground_z + 1 + diff_z)
                e2 = (x , y, ground_z + 1)
            ground[(x, y)] = (ground_z + 1 + diff_z, name)
            if sup is not None:
                supported_by[name].add(sup)
                supports[sup].add(name)
            fallen[name] = (e1, e2)
    return fallen, supported_by, supports




def star1(blocks):
    fallen, supported_by, supports = fall(blocks)
    removable = 0
    for name in fallen:
        sups = supports[name]
        all_supported_elsewhere = True
        for sup in sups:
            if(len(supported_by[sup]) <= 1):
                all_supported_elsewhere = False
        if all_supported_elsewhere:
            removable += 1
    return removable


def falls_when_removed(fallen, supports, supported_by):
    falls = set()
    for name in fallen:
        sups = supports[name]
        for sup in sups:
            #is this supported by anything that is not fallen?
            sup_by_new = supported_by[sup].difference(fallen)
            if len(sup_by_new) == 0:
                falls.add(sup)

    #only keep track of the new falls
    falls = falls.difference(fallen)
    if(len(falls) > 0):
        falls.update(falls_when_removed(falls | fallen, supports, supported_by))
    return falls



def star2(blocks):
    fallen, supported_by, supports = fall(blocks)
    total_falls = 0
    for name in fallen:
        total_falls += len(falls_when_removed(set([name]), supports, supported_by))
    return total_falls
    # return sum(map(lambda x: len(falls_when_removed(set([x]), supports, supported_by)), ordered_names))

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