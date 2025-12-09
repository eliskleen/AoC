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

    print(f'Load time: {load_time}')
    print(f'Star 1 time: {star1_time}')
    print(f'Star 2 time: {star2_time}')
    print(f"Total time: {load_time + star1_time + star2_time}")
    print(f'Star 1 answer: {ans1}')
    print(f'Star 2 answer: {ans2}')


def format_data(raw):
    pos = []
    for line in raw.splitlines():
        line = line.split(",")
        pos.append((int(line[0]), int(line[1])))
    return pos
    
def getArea(a, b):
    return (abs(a[0] - b[0]) +1) * (abs(a[1] - b[1]) + 1)
def star1(data):
    areas = []
    maxArea = 0
    for i in range(len(data)):
        for j in range(i, len(data)):
            area = getArea(data[i], data[j])
            maxArea = max(area, maxArea)

    return maxArea

def pointInside(edges, pos, maxCord):
    x, y = pos
    maxX, maxY = maxCord
    if pos in edges:
        return True
    crossingsX = 0
    for dx in range(x, maxX+2):
        if (dx, y) in edges:
            crossingsX += 1

    crossingsY = 0
    for dy in range(y, maxY+2):
        if (x, dy) in edges:
            crossingsY += 1
    inside = crossingsX % 2 == 1 and crossingsY % 2 == 1
    return inside
def star2(data):
    edges = set()
    xMax = 0
    xMin = 0
    yMax = 0
    yMin = 0
    for i in range(len(data)):
        j = (i + 1) % len(data)
        x1, y1 = data[i]
        x2, y2 = data[j]
        xMax = max(x1, x2, xMax)
        xMin = min(x1, x2, xMin)
        yMax = max(y1, y2, yMax)
        yMin = min(y1, y2, yMin)

        edges.add((x1, y1))
        edges.add((x2, y2))
        if(x1 != x2 and y1 != y2):
            print("WE SHOULD NOT BE HERE")
            exit()

        if(x1 == x2):
            minY = min(y1, y2)
            for dx in range(abs(y1-y2)+1):
                edges.add((x1, minY + dx))
        else:
            minX = min(x1, x2)
            for dx in range(abs(x1-x2)+1):
                edges.add((minX + dx, y1))
    minCord = (xMin, yMin)
    maxCord = (xMax, yMax)
    areas = []
    for i in range(len(data)):
        for j in range(i, len(data)):
            areas.append((getArea(data[i], data[j]), i, j))
    areas.sort(reverse=True)

    for a, i, j in areas:
        x1, y1 = data[i]
        x2, y2 = data[j]
        xMax, xMin = (x1, x2) if x1 > x2 else (x2, x1)
        yMax, yMin = (y1, y2) if y1 > y2 else (y2, y1)
        inside = True

        for dx in range(xMax - xMin):
            inside = pointInside(edges, (xMin + dx, yMin), maxCord) and pointInside(edges, (xMin + dx, yMax), maxCord)
            if not inside:
                break
        if not inside:
            continue
        for dy in range(yMax - yMin):
            inside = pointInside(edges, (xMin, yMin + dy), maxCord) and pointInside(edges, (xMax, yMin + dy), maxCord)
            if not inside:
                break
        if(inside):
            return a


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