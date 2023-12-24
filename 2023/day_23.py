from collections import defaultdict
import heapq
from math import sqrt
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


def inside(x, y, data):
    return 0 <= x < len(data[0]) and 0 <= y < len(data)

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

tile_to_dir = {
    "^": (0, -1),
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
}
def format_data(raw):
    slopes = sum([1 for c in raw if c in "^v<>"])
    print("slopes", slopes)
    lines = raw.split('\n')
    start_x = lines[0].index(".")
    start_y = 0
    end_x = lines[-1].rindex(".")
    end_y = len(lines) - 1
    G = defaultdict(list)
    G2 = defaultdict(list)
    slopes = set()
    slopes.add((start_x, start_y))
    slopes.add((end_x, end_y))
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            tile = lines[y][x]
            if tile == '#':
                continue
            if tile == '.':
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if inside(nx, ny, lines) and lines[ny][nx] != "#":
                        G[(x, y)].append((nx, ny))
            else:
                slopes.add((x, y))
                dx, dy = tile_to_dir[tile]
                nx, ny = x + dx, y + dy
                if inside(nx, ny, lines) and lines[ny][nx] != "#":
                    G[(x, y)].append((nx, ny))
            if tile != "#":
                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if inside(nx, ny, lines) and lines[ny][nx] != "#":
                        G2[(x, y)].append((nx, ny))
    
    return (G, G2), (start_x, start_y), (end_x, end_y)

    G2 = defaultdict(list)
    start = (start_x, start_y)
    end = (end_x, end_y)
    slopes.add(start)
    slopes.add(end)
    #create G2 where each edge is a slope (including start and end), and nodes are the "roads" between them
    for slope in slopes:
        x, y = slope
        ch = lines[y][x]
        dir = tile_to_dir[ch]
        nx, ny = x + dir[0], y + dir[1]
        stack = [(nx, ny, 1)]


    
               

            

    return (G, G2), (start_x, start_y), (end_x, end_y)
    return raw
    
def DFS(G, start, end, do_print = False):
    # paths = []
    longets_path = 0
    stack = [(start, [start])]
    

    while stack:
        (vertex, path) = stack.pop()
        nextsteps = set(G[vertex]) - set(path)
        # if do_print and len(nextsteps) > 1:
            # print(f'found {len(nextsteps)} paths')
        for next in set(G[vertex]) - set(path):
            # if do_print:
                # print("moving from", vertex, "to", next)
            if next == end:
                if len(path) + 1 > longets_path:
                    print("found path of length: ", len(path) + 1)
                    longets_path = len(path) + 1
                if do_print:
                    print("found path of length: ", len(path) + 1)
                    # print("paths found: ", len(paths) + 1)
                # paths.append(path + [next])
            else:
                stack.append((next, path + [next]))
    return longets_path

def star1(data):
    # return 0
    Gs, start, end = data
    G = Gs[0]
    longest = DFS(G, start, end)
    # sorted = [len(p)-1 for p in paths]
    # sorted.sort()
    # print(sorted)
    # longest = max(paths, key=lambda x: len(x))

    return longest -1



def star2(data):
    # return 0
    print("star2")
    Gs, start, end = data
    G = Gs[1]
    longest = DFS(G, start, end)
    # longest = max(paths, key=lambda x: len(x))
    return longest -1

    Gs, start, end = data
    G = Gs[1][0]
    
    paths = DFS(G, start , end, True)

    print(start)
    print(start, Gs[1][1][start])
    

    # for g in Gs[1][1]:
    #     print(g, Gs[1][1][g])


    # sorted = [len(p)-1 for p in paths]
    # sorted.sort()
    # print(sorted)
    longest = max(paths, key=lambda x: len(x))
    # print("longest", longest)
    for g in longest:
        print(g, Gs[1][1][g])
        (x, y) = g
        print(Gs[1][2][y][x])

    g_len = Gs[1][1]
    length = 0
    for i in range(len(longest) - 1):
        curr = longest[i]
        next = longest[i+1]
        for nx, ny, l in g_len[curr]:
            if (nx, ny) == next:
                length += l
                break



    return length
    


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