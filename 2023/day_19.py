from collections import defaultdict
from copy import deepcopy
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
    raw = raw.split('\n\n')

    wfs = defaultdict(list)
    for line in raw[0].split('\n'):
        name = line.split('{')[0]
        rules = line.split('{')[1].split('}')[0].split(',')
        for r in rules:
            if ':' not in r: #no condition
                wfs[name].append(("", "?", 0, r))
                continue
            cond = r.split(':')[0]
            dest = r.split(':')[1]
            part = cond[0]
            wfs[name].append((part, cond[1], int(cond[2:]), dest))

    parts = []
    for line in raw[1].split('\n'):
        line = line.split('{')[1].split('}')[0]
        d = {}
        for p in line.split(','):
            d[p[0]] = int(p[2:])
        parts.append(d)


    return wfs, parts

def lt(part, part_name,  val):
    return part[part_name] < val
def gt(part, part_name,  val):
    return part[part_name] > val
    
def star1(data):
    wfs, parts = data
    accepted = []
    for part in parts:
        wf = wfs['in']
        done = False
        while not done:
            for (pn, cond, val, dest) in wf:
                if cond == '?':
                    fun_res = True
                elif cond == '>':
                    fun_res = gt(part, pn, val)
                elif cond == '<':
                    fun_res = lt(part, pn, val)
                if fun_res:
                    wf = wfs[dest]
                    if dest == 'A':
                        accepted.append(part)
                    if dest == 'R' or dest == 'A':
                        done = True
                    break
    ret = 0
    for part in accepted:
        ret += sum(part.values())
    return ret

def star2(data):
    wfs, _ = data
    accepting = []
    for wf in list(wfs.keys()):
        for i, (_, _, _, dest) in enumerate(wfs[wf]):
            if dest == 'A':
                accepting.append((wf, i))

    ranges = {'x' : (1, 4000), 'm': (1,4000), 'a': (1,4000), 's': (1,4000)}
    combinations = 0
    for start in accepting:
        rs = find_ranges(start, wfs, deepcopy(ranges))
        if rs is None:
            continue
        x = rs['x']
        m = rs['m']
        a = rs['a']
        s = rs['s']
        combinations += (x[1] - x[0] + 1) * (m[1] - m[0] + 1) * (a[1] - a[0] + 1) * (s[1] - s[0] + 1)
    
    return combinations

#assuming there is only one path to A:s
def find_ranges(start, wfs, ranges):
    (wf_name, i) = start
    wf = wfs[wf_name]
    for (pn, cond, val, _) in wf[:i]: # it needs to fail all of these
        if cond == '>':
            new_max = min(ranges[pn][1], val)
            ranges[pn] = (ranges[pn][0], new_max)
        elif cond == '<':
            new_min = max(ranges[pn][0], val)
            ranges[pn] = (new_min, ranges[pn][1])
    
    (pn, cond, val, _) = wf[i] # it needs to pass this
    if cond == '?':
        pass
    elif cond == '>':
        new_min = max(ranges[pn][0], val+1)
        ranges[pn] = (new_min, ranges[pn][1])
    elif cond == '<':
        new_max = min(ranges[pn][1], val-1)
        ranges[pn] = (ranges[pn][0], new_max)

    for rs in ranges: #check if any ranges are invalid
        if ranges[rs][0] > ranges[rs][1]:
            return None

    if wf_name == 'in':
        return ranges

    for wf in wfs:
        for i, (_, _, _, dest) in enumerate(wfs[wf]):
            if dest == wf_name:
                return find_ranges((wf, i), wfs, ranges)

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