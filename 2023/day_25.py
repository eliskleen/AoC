from collections import defaultdict
import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
import networkx as nx
# import os
# os.environ["PATH"] += os.pathsep + 'D:/Program Files (x86)/Graphviz2.38/bin/'

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
    neighbours = defaultdict(set)
    edges = set()
    for line in raw.split('\n'):
        n1 = line.split(':')[0]
        ns = line.split(':')[1].split(' ')
        for n in ns:
            if n != '':
                neighbours[n1].add(n)
                neighbours[n].add(n1)
                e = tuple(sorted([n1, n]))
                edges.add(e)

    return edges, neighbours

def star1(data):
    edges, neighbours = data
    nodes = list(set(neighbours.keys()))
    number_of_nodes = len(nodes)
    

    G = nx.Graph()
    for n in nodes:
        G.add_node(n)
    for e in edges:
        G.add_edge(*e)

    res = list(nx.minimum_edge_cut(G))
    G.remove_edges_from(res)
    cc = list(nx.connected_components(G))

    return len(cc[0])*len(cc[1])
            


        




def star2(data):
    return 0

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