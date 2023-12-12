from copy import deepcopy
import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
import re

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
    return[(x.split(' ')[0], list(map(int, x.split(' ')[1].split(',')))) for x in raw.split('\n')]

is_hash = re.compile(r'#+')

def is_valid(springs, nums):
    matches = re.findall(is_hash, springs)
    corrLens = 0
    if len(matches) != len(nums):
        return False

    corrLens = len([])

    for i, m in enumerate(matches):
        if len(m) != nums[i]:
            return False
        corrLens += 1
    return corrLens == len(nums)

def star1(data):
    
    arr = 0
    for (s, n) in data:
        arr += count_replacements(s, n)
    return arr 




                
   

def count_replacements(springs, nums):

    @functools.cache
    def dp(pos, groupNum, r=0):
        if pos >= len(springs): return groupNum == len(nums)
        if groupNum >= len(nums): return False

        # pos is a . or we replace a ? with a .
        if springs[pos] in '.?': r += dp(pos+1, groupNum)
        
        if pos == 6:
            print()
            print("pos", pos, "groupNum", groupNum, "r", r, "nums[groupNum]", nums[groupNum],  "springs", springs, "len(springs)", len(springs), "pos+nums[groupNum]", pos+nums[groupNum])
            print()
            print()

        # print("pos", pos, "groupNum", groupNum, "r", r, "nums[groupNum]", nums[groupNum],  "springs", springs, "len(springs)", len(springs), "pos+nums[groupNum]", pos+nums[groupNum])
        # pos is a # or we replace a ? with a #
        if  springs[pos] in '#?' \
            and pos+nums[groupNum] <= len(springs)\
            and all([springs[pos+i] in '#?' for i in range(1, nums[groupNum])]) \
            and (pos+nums[groupNum] >= len(springs) or springs[pos+nums[groupNum]+1] in '.?'):

            print("pos", pos, "groupNum", groupNum, "r", r, "nums[groupNum]", nums[groupNum],  "springs", springs, "len(springs)", len(springs), "pos+nums[groupNum]", pos+nums[groupNum])
            nr = dp(pos+nums[groupNum]+1, groupNum+1)
            print("nr", nr, "r", r)
            r += nr
            # r += dp(pos+1, groupNum)

        # print("springs", springs, "r", r, "pos", pos)
        return r
    res = dp(0, 0)
    # print("springs[10]", springs[10:])
    return res

def star2(data):
    arr = 0
    for (s, n) in data:
        arr += count_replacements(s, n)
    return arr 

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