from collections import defaultdict
from copy import deepcopy
import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools

from ordered_set import OrderedSet

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
    return [[c for c in l] for l in raw.split("\n")]
    


right = (1, 0)
left = (-1, 0)
up = (0, -1)
down = (0, 1)

def is_in_bounds(pos, matrix):
    return 0 <= pos[1] < len(matrix) and 0 <= pos[0] < len(matrix[0])

def get_refl_dir(pos, matrix, direction):
    if matrix[pos[1]][pos[0]] == '/':
        if direction == up:
            return right
        elif direction == down:
            return left
        elif direction == left:
            return down
        elif direction == right:
            return up
    elif matrix[pos[1]][pos[0]] == '\\':
        if direction == up:
            return left
        elif direction == down:
            return right
        elif direction == left:
            return up
        elif direction == right:
            return down
    return direction

def brute(pos, dir, data):
    energized = set()

    queue = set()
    queue.add((pos, dir))

    beamLoop = set()
    while queue:
        beam, direction = queue.pop()
        while is_in_bounds(beam, data) and (beam, direction) not in beamLoop:
            energized.add(beam)
            beamLoop.add((beam, direction))
            if data[beam[1]][beam[0]] in '/\\':
                direction = get_refl_dir(beam, data, direction)
            if data[beam[1]][beam[0]] == '-' and direction in [up, down]:
                b1 = beam[0] + right[0], beam[1] + right[1]
                queue.add((b1, right))
                b2 = beam[0] + left[0], beam[1] + left[1]
                queue.add((b2, left))
                break
            elif data[beam[1]][beam[0]] == '|' and direction in [left, right]:
                b1 = beam[0] + down[0], beam[1] + down[1]
                queue.add((b1, down))
                b2 = beam[0] + up[0], beam[1] + up[1]
                queue.add((b2, up))
                break
            beam = (beam[0] + direction[0], beam[1] + direction[1])
        
    return len(energized)
def star1(data):
    return brute((0,0), right, data)



def expolore_beam(start, direction, data, beam_to_energized, beamLoop, do_print=False):

    curr_energized = set()
    beam = deepcopy(start)
    start_dir = deepcopy(direction)
    if (beam, direction) in beam_to_energized:
        if do_print:
            print("already explored, before", beam, direction)
            print("curr_energized", len(curr_energized))
        curr_energized |= beam_to_energized[(beam, direction)]
        if do_print:
            print("energized, updated", len(curr_energized))
        return curr_energized, beam_to_energized
    
    while is_in_bounds(beam, data) and (beam, direction) not in beamLoop:
        beamLoop.add((beam, direction))
        if (beam, direction) in beam_to_energized:
            if do_print:
                print("already explored", beam, direction)
            curr_energized |= beam_to_energized[(beam, direction)]
            break
        curr_energized.add(beam)
        tile = data[beam[1]][beam[0]]
        if tile in '/\\':
            if do_print:
                print("hit reflector at pos", beam, "with direction", direction)
            direction = get_refl_dir(beam, data, direction)
        elif (tile == '|' and direction in [left, right]) or (tile == '-' and direction in [up, down]):
            if do_print:
                print("hit splitter", tile, "at pos", beam, "with direction", direction)
            bl1 = (beamLoop)
            bl2 = (beamLoop)
            d1 = right if tile == '-' else up
            d2 = left if tile == '-' else down
            e1, beam_to_energized = expolore_beam(beam, d1, data,  beam_to_energized, bl1, do_print=do_print)
            e2, beam_to_energized = expolore_beam(beam, d2, data,  beam_to_energized, bl2, do_print=do_print)
            curr_energized |= e1
            beam_to_energized[(beam, d1)] |= e1
            curr_energized |= e2
            beam_to_energized[(beam, d2)] |= e2
            break
        
        beam = (beam[0] + direction[0], beam[1] + direction[1])
    beam_to_energized[(start, start_dir)] |= curr_energized
    return curr_energized, beam_to_energized

def star2(data):

    beam_to_energized = defaultdict(set)

    splitters = []
    for y in range(len(data)):
        for x in range(len(data[0])):
            if data[y][x] in ['-', '|']:
                splitters.append((x, y))

    for (x, y) in splitters:
        dirs = [up, down] if data[y][x] == '|' else [left, right]
        for dir in dirs:
            _, beam_to_energized = expolore_beam((x, y), dir, data, beam_to_energized, set(), do_print=False)

    starts = [((i,0), down) for i in range(len(data[0]))]
    starts += [((0,i), right) for i in range(len(data))]
    starts += [((len(data[0])-1,i), left) for i in range(len(data))]
    starts += [((i,len(data)-1), up) for i in range(len(data[0]))]

    max_energized = 0
    for (beam, dir) in starts:
        curr, beam_to_energized = expolore_beam(beam, dir, data, beam_to_energized, OrderedSet(), do_print=False)
        max_energized = max(max_energized, len(curr))
    return max_energized

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