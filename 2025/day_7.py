import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
from collections import defaultdict
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
    splitters = defaultdict(list)
    s = raw.splitlines()[0].index("S")
    y = 1
    for line in raw.splitlines()[1:]:
        x = 0
        for c in line:
            if c == "^":
                splitters[x].append(y)
            x += 1
        y += 1

    return s, splitters
    
def star1(data):
    s, splitters = data
    hitSplittes = set()
    beams = [(s, 0)]
    starts = set()
    while(len(beams) > 0):
        cx, cy = beams.pop(0)
        for sy in splitters[cx]:
            if(sy > cy):
                hitSplittes.add((cx, sy))
                l = (cx-1, sy)
                r = (cx+1, sy)
                if(l not in starts):
                    beams.append(l)
                    starts.add(l)
                if(r not in starts):
                    beams.append(r)
                    starts.add(r)
                break
    return len(hitSplittes)

def revSplittes(splitters):
    splittersAtLevel = defaultdict(list)
    maxY = 0
    for x, ys in splitters.items():
        for y in ys:
            splittersAtLevel[y].append(x)
            maxY = max(maxY, y)
    return splittersAtLevel, maxY


def star2(data):
    s, splitters = data
    #map y level to x cord splitters
    splittersAtLevel, y = revSplittes(splitters)
    splitterToTimeLine = defaultdict(int)
    #iterate from bottom upp, use whats already calculated
    while(y >= 0):
        ysplits = splittersAtLevel[y]
        for cx in ysplits:
            splitterToTimeLine[(cx, y)] += 1 #we are splitting for the first time
            for sy in splitters[cx-1]:
                if(sy > y):
                    splitterToTimeLine[(cx, y)] += splitterToTimeLine[(cx-1, sy)] #we hit a splitter on the left, now we "take" their timelines
                    break
            for sy in splitters[cx+1]:
                if(sy > y):
                    splitterToTimeLine[(cx, y)] += splitterToTimeLine[(cx+1, sy)]#we hit a splitter on the right, now we "take" their timelines
                    break
        y -= 1
    #find first splitter
    xs = splitters[s] 
    first = (s, xs[0])
    return splitterToTimeLine[first] + 1





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