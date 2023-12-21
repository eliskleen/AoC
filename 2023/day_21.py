from collections import defaultdict
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
    garden = [[c for c in row] for row in raw.split('\n')]
    start = (0,0)
    for y in range(len(garden)):
        for x in range(len(garden[y])):
            if garden[y][x] == 'S':
                start = (x,y)
                break
    return garden, start

dirs = [(0,1), (1,0), (0,-1), (-1,0)]
def get_places_after_steps(garden, start, steps):
    x,y = start
    curr = set()
    curr.add((x,y))
    for _ in range(steps):
        new = set()
        for x,y in curr:
            for (dx, dy) in dirs:
                nx, ny = x+dx, y+dy
                # if(is_valid_step(garden, nx, ny)):
                if garden[ny][nx] in '.S':
                    new.add((nx,ny))
        curr = new
    return len(curr) 
def star1(data):
    garden, start = data
    poses = get_places_after_steps(garden, start, 64)
    return poses

def f(n, a):
    b0 = a[0]
    b1 = a[1] - a[0]
    b2 = a[2] - a[1]
    return b0 + b1*n + (n*(n-1)//2)*(b2-b1)

def star2(data):
    garden, start = data
    steps = 26501365
    h = len(garden)
    w = len(garden[0])
    a = []
    x,y = start
    curr = set()
    curr.add((x,y))
    for s in range(steps):
        new = set()
        for x,y in curr:
            for (dx, dy) in dirs:
                nx, ny = x+dx, y+dy
                # if(is_valid_step(garden, nx, ny)):
                if garden[ny%h][nx%w] in '.S':
                    new.add((nx,ny))
        if s % w == steps % w:
            a.append(len(curr))
        if len(a) == 3:
            break
        curr = new
    
    print(a)
    return (f(steps//w, a))




    return 0

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