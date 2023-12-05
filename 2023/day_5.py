import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools

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
    inp = [l.strip().split('\n')[1:] for l in raw.split('\n\n')]
    seeds = [int(i) for i in raw.split('\n')[0].split(':')[1].split()]
    maps = []
    for sect in inp[1:]:
        dic = []
        for line in sect:
            nums = [int(n) for n in line.split(' ')]
            dest, start, ns = nums[0], nums[1], nums[2]
            dic.append((start, dest, ns))
            
        maps.append(dic)
    return (maps, seeds)
    
def star1(ms):
    (maps, seeds) = ms
    locs = []
    for seed in seeds:
        curr = seed
        for m in maps:
            for (start, dest, ns) in m:
                if (start <= curr <= start + ns - 1):
                    offset = curr - start
                    curr = dest + offset
                    break


                    
               
        locs.append(curr)
    return min(locs)

def star2(ms):
    (maps, seeds) = ms
    minLoc = int(1e20)
    i = 0
    newSeeds = []
    while i < len(seeds):
        start = seeds[i]
        ren = seeds[i+1]
        newSeeds.append((start, start + ren -1))
        i += 2
    seeds = newSeeds
    for (start, stop) in seeds:
        currRanges = [(start, stop)]
        for m in maps:
            #queue holds all non transformed ranges, while currRanges holds all transformed ranges
            queue = list(currRanges)
            currRanges = []
            while len(queue) > 0:
                (currStart, currStop) = queue.pop(0)
                matched = False
                for (start, dest, ns) in m:
                    # add to currange the new remapped range, split if needed
                    if (start <= currStart <= start + ns - 1):
                        print('here')
                        maxStop = start + ns - 1
                        # if the range is split, add the new range to the queue
                        if (currStop > maxStop): 
                            #add nontransformed range to queue
                            queue.append((maxStop+1, currStop))
                            currStop = maxStop
                        offset = currStart - start
                        currStop = dest + offset + (currStop - currStart)
                        currStart = dest + offset
                        #add transformed range to currRanges
                        currRanges.append((currStart, currStop))
                        matched = True
                        break
                    # we know currStart is not in this range, but currStop might be, so we might need to split
                    elif (start <= currStop <= start + ns - 1):
                        #add nontransformed range to queue
                        queue.append((currStart, start-1))
                        #add transformed range to currRanges
                        currRanges.append((dest, dest + (currStop - start)))
                        matched = True
                        break
                # if we didn't match, add the range to currRanges
                if not matched:
                    #add nontransformed, but valid range to currRanges
                    currRanges.append((currStart, currStop))


        for (start, stop) in currRanges:
            minLoc = min(minLoc, start)
            

                        
                

    return minLoc 



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