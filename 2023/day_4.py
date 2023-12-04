from collections import defaultdict
import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
import re

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
    return raw
    
def star1(data):
    ret = 0
    for line in data.splitlines():
        winningNums = 0
        winnings = line.split(':')[1].split(' | ')[0]
        winnings = re.findall(re.compile('\d+'), winnings)
        nums = re.findall(re.compile('\d+'), line.split(':')[1].split(' | ')[1])
        for win in winnings:
            for num in nums:
                if win == num:
                    winningNums = 1 if winningNums == 0 else winningNums * 2
        ret += winningNums



    return ret

def star2(data):
    cards = {}
    for line in data.splitlines():
        card = re.findall(re.compile('\d+'), line.split(':')[0])[0]
        winnings = line.split(':')[1].split(' | ')[0]
        winnings = re.findall(re.compile('\d+'), winnings)
        nums = re.findall(re.compile('\d+'), line.split(':')[1].split(' | ')[1])
        cards[card] = (winnings, nums, int(card))

    winningsOnCards = []
    for card in cards.values():
        winningNums = 0
        for win in card[0]:
            for num in card[1]:
                if win == num:
                    winningNums += 1
        winningsOnCards.append(winningNums)

    instances = [1 for x in range(len(winningsOnCards))]
    print(instances)
    for i, v in enumerate(winningsOnCards):
        for j in range(v):
            instances[j+ i +1] += instances[i]
    return sum(instances)

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