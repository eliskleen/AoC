from copy import deepcopy
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
    matrix = ([[*line] for line in raw.split('\n') if line])
    return matrix
        
    

def roll_rock_north(matrix, x, y):
    matrix[y][x] = '.'
    while matrix[y][x] == '.' and y > -1:
        y -= 1
    matrix[y+1][x] = 'O'
    return matrix, y+1


def star1(data):
    # tilt matrix to the north and all round rocks (O) will roll uintill they hit a rock (O,#)
    matrix = deepcopy(data)
    res = 0
    south_max = len(matrix)
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if(matrix[y][x] == 'O'):
                matrix, y_res = roll_rock_north(matrix, x, y)
                res += south_max - y_res
    return res


def roll_north(matrix, x0, y0):
    y = y0
    x = x0
    rollers = 0
    while y < len(matrix) and matrix[y][x] in '.O':
        if matrix[y][x] == 'O':
            rollers += 1
        matrix[y][x] = '.'
        y += 1
    for y1 in range(rollers):
        matrix[y0+y1][x] = 'O'
    if y != len(matrix):
        matrix = roll_north(matrix, x, y+1)
    if x0 < len(matrix[0]) -1 and y0 == 0:
        matrix = roll_north(matrix, x0+1, y0)
    return matrix

def roll_west(matrix, x0, y0):
    x = x0
    y = y0
    rollers = 0
    while x < len(matrix[y]) and matrix[y][x] in '.O':
        if matrix[y][x] == 'O':
            rollers += 1
        matrix[y][x] = '.'
        x += 1
    
    for x1 in range(rollers):
        matrix[y0][x0+x1] = 'O'
    
    if x != len(matrix[y]):
        matrix = roll_west(matrix, x+1, y)

    if x0 == 0 and y0 < len(matrix) -1:
        matrix = roll_west(matrix, x0, y0+1)
    
    return matrix
def roll_south(matrix, x0, y0):
    x = x0
    y = y0
    rollers = 0
    while y > -1 and matrix[y][x] in '.O':
        if matrix[y][x] == 'O':
            rollers += 1
        matrix[y][x] = '.'
        y -= 1
    for y1 in range(rollers):
        matrix[y0-y1][x] = 'O'
    if y != -1:
        matrix = roll_south(matrix, x, y-1)        
    
    if x0 < len(matrix[0]) -1 and y0 == len(matrix) -1:
        matrix = roll_south(matrix, x0+1, y0)
    
    return matrix
def roll_east(matrix, x0, y0):
    x = x0
    y = y0
    rollers = 0
    while x > -1 and matrix[y][x] in '.O':
        if matrix[y][x] == 'O':
            rollers += 1
        matrix[y][x] = '.'
        x -= 1
    for x1 in range(rollers):
        matrix[y0][x0-x1] = 'O'
    if x != -1:
        matrix = roll_east(matrix, x-1, y)

    if x0 == len(matrix[0]) -1 and y0 < len(matrix) -1:
        matrix = roll_east(matrix, x0, y0+1)
    
    return matrix

def star2(data):
    matrix = deepcopy(data)
    matricies = []
    while matrix not in matricies:
        matricies.append(deepcopy(matrix))
        matrix = roll_north(matrix, 0, 0)
        matrix = roll_west(matrix, 0, 0)
        matrix = roll_south(matrix, 0, len(matrix)-1)
        matrix = roll_east(matrix, len(matrix[0])-1, 0)

    cycles = 1000000000
    loop_start = matricies.index(matrix)
    loop_size = len(matricies) - matricies.index(matrix)
    cycles -= loop_start
    cycles %= loop_size
    
    print("len matricies", len(matricies))
    print("matricied.index(matrix): ", matricies.index(matrix))
    print("loop size: ", loop_size)
    print("cycles: ", cycles)

    for _ in range(cycles):
        matrix = roll_north(matrix, 0, 0)
        matrix = roll_west(matrix, 0, 0)
        matrix = roll_south(matrix, 0, len(matrix)-1)
        matrix = roll_east(matrix, len(matrix[0])-1, 0)
        
    
    res = 0
    south_max = len(matrix)
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if(matrix[y][x] == 'O'):
                res += south_max - y
    
    return res

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