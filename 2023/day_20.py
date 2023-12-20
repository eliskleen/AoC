from collections import defaultdict
from copy import deepcopy
import math
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
    modules = {}
    for line in raw.splitlines():
        targets = [x.replace(',', '') for x in line.split()[2:]]

        if line.split()[0] == 'broadcaster':
            modules['broadcaster'] = ('b', targets)
        else:
            type = line[0]
            name = line.split()[0][1:]
            modules[name] = (type, targets)

    missing = []
    for name in modules:
        (type, targets) = modules[name]
        for t in targets:
            if t not in modules:
                missing.append((t, []))
    for (name, targets) in missing:
        modules[name] = ('?', targets)
    return modules
    

def press_button(modules, states, stop_state = None):

    pulses = {"low": 1, "high": 0}
    q = [('broadcaster', "low", 'button')]
    while q:
        name, inp, sender = q.pop()
        if stop_state is not None and name == stop_state and inp == "low":
            return states, pulses, True

        (inps, val) = states[name]
        inps[sender] = inp
        (type, targets) = modules[name]
        if type == "%":
            if inp == "low":
                val = "low" if val == "high" else "high"
                for target in targets:
                    pulses[val] += 1
                    q.append((target, val, name))
        elif type == "&":
            if all([x == "high" for x in inps.values()]):
                val = "low"
            else:
                val = "high"
           
            for target in targets:
                pulses[val] += 1
                q.append((target, val, name))
        elif name == 'broadcaster':
            val = inp
            for target in targets:
                pulses[val] += 1
                q.append((target, val, name))

        
        states[name] = (inps, val)

    return states, pulses, False
def star1(modules):

    states = defaultdict(lambda: ({}, "low"))
    for name in modules:
        (type, targets) = modules[name]
        for t in targets:
            states[t][0][name] = "low"
    
    states['broadcaster'] = ({'button':'low'}, "low")

    seen_states = []
    pulses = {"low": 0, "high": 0}
    puls_vals = []
    pushes = 0
    foundLoop = True
    # while states not in seen_states:
    while True:
        states, np, _ = press_button(modules, states)
        pulses['low'] += np['low']
        pulses['high'] += np['high']
        # puls_vals.append((pulses['low'], pulses['high']))
        pushes += 1
        if pushes == 1000:
            foundLoop = False
            break
        

    # cycles = 1000
    # loop_start = seen_states.index(states)
    # loop_size = len(seen_states) - loop_start
    # cycles -= loop_start
    # skipped = (cycles // loop_size) -1
    # cycles %= loop_size

    
    
    # plow_start = puls_vals[loop_start-1][0]
    # phigh_start = puls_vals[loop_start-1][1]
    # plow_end = puls_vals[-1][0]
    # phigh_end = puls_vals[-1][1]
    # plow_diff = plow_end - plow_start
    # phigh_diff = phigh_end - phigh_start
    # pulses['low'] += plow_diff * skipped
    # pulses['high'] += phigh_diff * skipped
    # print(puls_vals)
    # print("loop_start", loop_start)
    # print("plow_start", plow_start)
    # print("phigh_start", phigh_start)
    # print("plow_end", plow_end)
    # print("phigh_end", phigh_end)
    # print("plow_diff", plow_diff)
    # print("phigh_diff", phigh_diff)
   

    # print("skipped", skipped)



    # print("loop_size", loop_size)

    # for i in range(cycles):
    #     states, np = press_button(modules, states)
    #     pulses['low'] += np['low']
    #     pulses['high'] += np['high']
    
    return pulses['low']*pulses['high']
    


        
    

        
        

def create_states(modules):
    states = defaultdict(lambda: ({}, "low"))
    for name in modules:
        (type, targets) = modules[name]
        for t in targets:
            states[t][0][name] = "low"
    return states
def star2(modules):
    states = create_states(modules)
    states['broadcaster'] = ({'button':'low'}, "low")
    inpsrx = states['rx'][0]
    inp_name = list(inpsrx.keys())[0]
    useful = list(states[inp_name][0].keys())
    freqs = {n: None for n in useful}

    presses = 0
    while True:
        if all(val is not None for val in freqs.values()):
            print("freqs", freqs)
            return math.lcm(*list(freqs.values()))

        q = [('broadcaster', "low", 'button')]
        presses += 1
        while q:
            name, inp, sender = q.pop(0)
            if name in freqs and inp == "low" and freqs[name] is None:
                print("Debug", presses, name, freqs[name])
                freqs[name] = presses
            (inps, val) = states[name]
            inps[sender] = inp
            (type, targets) = modules[name]
            if type == "%":
                if inp == "low":
                    val = "low" if val == "high" else "high"
                    for target in targets:
                        q.append((target, val, name))
            elif type == "&":
                if all([x == "high" for x in inps.values()]):
                    val = "low"
                else:
                    val = "high"
                for target in targets:
                    q.append((target, val, name))
            elif name == 'broadcaster':
                val = inp
                for target in targets:
                    q.append((target, val, name))
            states[name] = (inps, val)

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