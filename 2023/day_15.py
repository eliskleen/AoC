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
    raw.replace('\n', '')
    return raw.split(',')
    
def get_hashed(data):
    curr = 0
    for c in data:
        curr += ord(c)
        curr *= 17
        curr %= 256
    return curr


def star1(data):
    return sum(map(get_hashed, data)) 

def star2(data):
    boxes = {}

    for cs in data:
        op = "=" if "=" in cs else "-"
        label = cs.split(op)[0]
        h = get_hashed(label)
        if h not in boxes:
            boxes[h] = {}
        #boxes contain (label, focal length, pos)
        if "=" in op:
            fl = int(cs.split(op)[1])
            if label not in boxes[h]:
                labels = len(boxes[h].keys())
                boxes[h][label] = (label, fl, labels+1)
            else:
                boxes[h][label] = (label, fl, boxes[h][label][2])
        elif "-" in op:
            if label in boxes[h]:
                pos = boxes[h][label][2]
                for lens_label in boxes[h]:
                    if boxes[h][lens_label][2] > pos:
                        boxes[h][lens_label] = (boxes[h][lens_label][0], boxes[h][lens_label][1], boxes[h][lens_label][2] - 1)
                del boxes[h][label]
    focusing_power = 0
    for h in boxes:
        for lens_label in boxes[h]:
            (label, focal_length, pos) = boxes[h][lens_label]
            fp = (h+1) * pos * focal_length
            focusing_power += fp
    return focusing_power

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