import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
import operator

def day_():
    year = int(os.getcwd().split('\\')[-1][:4]) 
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
    return raw.splitlines()

def star1(data):
    ret = 0
    maxBalls = {"red" : 12, "green" : 13, "blue": 14}
    for line in data:
        gameId = int(line.split(':')[0].split(' ')[1])
        possible = True
        for round in line.split(':')[1].split(';'):
            for bc in round.split(','):
                col = bc.split(' ')[2]
                balls = int(bc.split(' ')[1])
                if maxBalls[col] < balls :
                    possible = False
        if possible:
            ret += gameId
    return ret

def star2(data):
    ret = 0
    for line in data:
        rounds = line.split(':')[1].split(';')
        maxBalls = {"red" : 0, "green" : 0, "blue": 0}
        for round in rounds:
            for bc in round.split(','):
                col = bc.split(' ')[2]
                balls = int(bc.split(' ')[1])
                maxBalls[col] = max(maxBalls[col], balls)
        ret += functools.reduce(operator.mul, maxBalls.values(), 1)
    return ret

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