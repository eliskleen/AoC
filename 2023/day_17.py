import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
import heapq


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
    return [[int(c) for c in l] for l in raw.split("\n")]

north = (0, -1)
south = (0, 1)
east = (1, 0)
west = (-1, 0)
dirs = [north, south, east, west]

def get_op_dir(dir):
    if dir == north:
        return south
    elif dir == south:
        return north
    elif dir == east:
        return west
    elif dir == west:
        return east

def is_in_bounds(pos, matrix):
    return 0 <= pos[1] < len(matrix) and 0 <= pos[0] < len(matrix[0])

def pathfind(maze, start, min_straight_steps, max_straight_steps, start_dirs):
    pq = []
    visited = set()
    start = (0, 0)
    end = (len(maze[0]) - 1, len(maze) - 1)
    visited.add(start)
    for dir in start_dirs:
        pq.append((0,0, 0, dir, 1)) #cost, pos, enterDir, straightSteps
    while pq:
        cost, x, y, dir, straightSteps = heapq.heappop(pq)
        if (x, y, dir, straightSteps) in visited:
            continue
        else:
            visited.add((x, y, dir, straightSteps))
        
        if (x,y) == end and straightSteps >= min_straight_steps and straightSteps <= max_straight_steps:
            break
        
        valid_dirs = [d for d in dirs if d != get_op_dir(dir)]
        if straightSteps < min_straight_steps:
            valid_dirs = [dir]
        
        for d in valid_dirs:
            if (d[0] + dir[0] == 0 and d[1]+ dir[1] == 0):
                continue
            nx = x + d[0]
            ny = y + d[1]
            newStraightSteps = straightSteps + 1 if dir == d else 1
            if newStraightSteps > max_straight_steps or not is_in_bounds((nx, ny), maze):
                continue
            newCost = cost + int(maze[ny][nx])
            newNode = (newCost, nx, ny, d, newStraightSteps)
            heapq.heappush(pq, newNode)
               

    return cost

def star1(data):
    return pathfind(data, (0, 0), 1, 3, [south, east])
def star2(data): 
    return pathfind(data, (0, 0), 4, 10, [south,east])

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