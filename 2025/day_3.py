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
    return [[int(a) for a in line] for line in raw.split("\n")]

    
def star1(data):
    tot = 0
    for line in data :
        i = 0
        maxI = 0
        maxVal = 0
        while(maxVal < 9 and i < len(line) -1):
            val = line[i]
            (maxVal, maxI) = (val ,i) if val > maxVal else (maxVal, maxI)
            i += 1
        i = maxI + 1
        maxVal2 = 0
        while(maxVal2 < 9 and i < len(line)):
            val = line[i]
            maxVal2 = val if val > maxVal2 else maxVal2
            i += 1
        #print(maxVal *10 + maxVal2)
        tot += maxVal*10 + maxVal2
    return tot  

def findBiggest(line, start, end):
    i = start
    maxI = 0
    maxVal = 0
    while(maxVal < 9 and i < len(line) - end):
        val = line[i]
        (maxVal, maxI) = (val, i) if val > maxVal else (maxVal, maxI)
        i += 1
    return (maxVal, maxI)

def star2(data):
    tot = 0
    for line in data:
        number = ""
        maxI = -1
        for i in range(12):
            (maxVal, maxI) = findBiggest(line, maxI+1, 11-i)
            number += str(maxVal)
        tot += int(number)
    return tot

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