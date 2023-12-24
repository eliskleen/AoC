import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
import numpy as np
from z3 import Int, Solver


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
    hails = []
    for line in raw.split('\n'):
        pos = list(map(int, line.split('@')[0].strip().split(',')))
        vel = list(map(int, line.split('@')[1].strip().split(',')))
        hails.append((pos, vel))



    return hails
    

# min_x = 7
# max_x = 27
# min_y = 7
# max_y = 27
min_x = 200000000000000
max_x = 400000000000000
min_y = 200000000000000
max_y = 400000000000000

def get_enter_exit_times(hail):



    tx_min = (hail[0][0] - min_x) / (hail[1][0])
    tx_max = (hail[0][0] - max_x) / (hail[1][0])
    ty_min = (hail[0][1] - min_y) / (hail[1][1])
    ty_max = (hail[0][1] - max_y) / (hail[1][1])

        

    # print("tx_min", tx_min, "tx_max", tx_max)
    # # print("ty_min", ty_min, "ty_max", ty_max)


    t_max = max(tx_min, tx_max, ty_min, ty_max)
    t_min = max(0, min(tx_min, tx_max, ty_min, ty_max))

        
    


    return (t_min, t_max)
    # return (min(t_min, t_max), max(t_min, t_max))
def get_intersect(a1, a2, b1, b2):
    """ 
    Returns the point of intersection of the lines passing through a2,a1 and b2,b1.
    a1: [x, y] a point on the first line
    a2: [x, y] another point on the first line
    b1: [x, y] a point on the second line
    b2: [x, y] another point on the second line
    """
    s = np.vstack([a1,a2,b1,b2])        # s for stacked
    h = np.hstack((s, np.ones((4, 1)))) # h for homogeneous
    l1 = np.cross(h[0], h[1])           # get first line
    l2 = np.cross(h[2], h[3])           # get second line
    x, y, z = np.cross(l1, l2)          # point of intersection
    if z == 0:                          # lines are parallel
        return (float('inf'), float('inf'))
    return (x/z, y/z)


def intersects_1(hail1, hail2):
    t1_min, t1_max = get_enter_exit_times(hail1)
    t2_min, t2_max = get_enter_exit_times(hail2)

    t_min = max(t1_min, t2_min)
    t_max = min(t1_max, t2_max)
    # print("t_min", t_min, "t_max", t_max)

    p11x = hail1[0][0] + t_min * hail1[1][0]
    p11y = hail1[0][1] + t_min * hail1[1][1]
    p11 = (p11x, p11y)
    p12x = hail1[0][0] + t_max * hail1[1][0]
    p12y = hail1[0][1] + t_max * hail1[1][1]
    p12 = (p12x, p12y)
    p21x = hail2[0][0] + t_min * hail2[1][0]
    p21y = hail2[0][1] + t_min * hail2[1][1]
    p21 = (p21x, p21y)
    p22x = hail2[0][0] + t_max * hail2[1][0]
    p22y = hail2[0][1] + t_max * hail2[1][1]
    p22 = (p22x, p22y)
    # # print("p11", p11, "p12", p12)
    # print("p21", p21, "p22", p22)


    return get_intersect(p11, p12, p21, p22)

    

    
def get_time(hail, x, y):
    return min((x - hail[0][0]) / hail[1][0], (y - hail[0][1]) / hail[1][1])

def star1(hails):

    hails = [((x, y, 0), (vx, vy, 0)) for (x, y, z), (vx, vy, vz) in hails]
    # print(hails)
    combs = itertools.combinations(hails, 2)
    has_intersected = set()
    intesects = 0
    valid_intersects = []
    for comb in combs:
        # print(comb)
        ip = intersects_1(*comb)
        # print(ip)
        if get_time(comb[0], *ip) < 0  or  get_time(comb[1], *ip) < 0:
            # print("------")
            continue
        if min_x <= ip[0] <= max_x and min_y <= ip[1] <= max_y:
            # print("INTERSECT")
            intesects += 1


        # print("------")

    return intesects

def star2(hails):
    hails_to_solve = 3
    x, y, z, dx, dy, dz = Int('x'), Int('y'), Int('z'), Int('dx'), Int('dy'), Int('dz')
    times = [Int(f'T{i}') for i in range(hails_to_solve)]

    s = Solver()
    for i in range(hails_to_solve):
        (x_i, y_i, z_i), (dx_i, dy_i, dz_i) = hails[i]
        s.add(x + times[i] * dx - x_i - times[i] * dx_i == 0)
        s.add(y + times[i] * dy - y_i - times[i] * dy_i == 0)
        s.add(z + times[i] * dz - z_i - times[i] * dz_i == 0)

    s.check()
    model = s.model()
    return int(str(model.eval(x + y + z)))

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