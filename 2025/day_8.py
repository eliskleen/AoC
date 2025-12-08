import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
from collections import defaultdict
import itertools
import math
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
    data = [[int(c) for c in row.split(",")] for row in raw.splitlines()]
    #find all distances
    distances = defaultdict(int)
    seen = set()
    for i in range(len(data)):
        for j in range(i,len(data)):
            if i != j:
                a = data[i]
                b = data[j]
                distances[(i, j)] = dist(a, b)

    distances = [(d, pair) for pair, d in distances.items()]
    distances.sort()
    return data, distances

    
def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2] - b[2])**2)

def makeConnections(distances, numConnections, returnLast = False):
    cNum = 0
    #map from circuit number to indecies
    circuits = defaultdict(list)
    #map from index to circuit number
    cMap = defaultdict(int)
    last = (0,0)
    if(numConnections != -1):
        distances = distances[:numConnections]
    for d, (i, j) in distances:
        ci = cMap[i]
        cj = cMap[j]
        #i and j is not in a circuit
        if(ci == 0 and cj == 0):
            cNum += 1
            cMap[i] = cNum
            cMap[j] = cNum
            circuits[cNum].append(i)
            circuits[cNum].append(j)
            last = (i, j)
        #j his not in a circuit
        elif ci != 0 and cj == 0:
            cMap[j] = cMap[i]
            circuits[ci].append(j)
            last = (i, j)
        #i is not in a circuit
        elif cj != 0 and ci == 0:
            cMap[i] = cMap[j]
            circuits[cj].append(i)
            last = (i, j)
        elif ci != cj:
            #combine two circuits, put all in cj in ci
            mapCi = cMap[i]
            last = (i, j)
            for nj in circuits[cj]:
                circuits[mapCi].append(nj)
                cMap[nj] = mapCi
            circuits[cj] = []
    if(returnLast):
        return last
    circSizes = [len(mems) for cIdx, mems in circuits.items()]
    circSizes.sort(reverse=True)
    return circSizes[0] * circSizes[1] * circSizes[2]

def star1(data):
    return makeConnections(data[1], 1000)

def star2(data):
    data, distances = data
    i, j = makeConnections(distances, -1, True)
    return data[i][0] * data[j][0]

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