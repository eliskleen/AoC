from copy import deepcopy
import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools

from shapely.geometry import Point, Polygon
import numpy as np

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


class Node:
    def __init__(self, symbol, x, y):
        self.symbol = symbol
        self.x = x
        self.y = y
        self.neighbors = set()
        self.visited = False
        self.distance = 0
        self.is_start = False

    def add_neighbor(self, node):
        if node.is_start:
            node.add_neighbor(self)
        self.neighbors.append(node)
    
    def add_neighbor(self, node):
        self.neighbors.add(node)

    def __eq__(self, __value: object) -> bool:
        return self.x == __value.x and self.y == __value.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

class Ground:
    def __init__(self, x, y, sizeX, sizeY):
        self.x = x
        self.y = y
        self.checked = False
        self.inside = False
        self.extended = False
        if x == 0 or y == 0 or x == sizeX - 1 or y == sizeY - 1:
            self.inside = False

        

north = (0, -1)
northEast = (1, -1)
northWest = (-1, -1)
south = (0, 1)
southEast = (1, 1)
southWest = (-1, 1)
east = (1, 0)
west = (-1, 0)

dirsFromSym = {
    '|' : [north, south],
    '-' : [east, west],
    'L' : [north, east],
    'J' : [north, west],
    '7' : [south, west],
    'F': [south, east],
}
sizeX = 0
sizeY = 0
def format_data(raw):
    nodes = {}
    start = None
    ground = {}
    global sizeX
    global sizeY
    sizeX = len(raw.split('\n')[0])
    sizeY = len(raw.split('\n'))
    for y in range(len(raw.split('\n'))):
        for x in range(len(raw.split('\n')[y])):
            sym = raw.split('\n')[y][x]
            if sym == '.':
                ground[(x, y)] = Ground(x, y, sizeX, sizeY)
                continue
            node = Node(sym, x, y)
            if sym == "S":
                node.is_start = True
                start = node
            nodes[(x, y)] = node

    nodes, start = parse_neighbors(nodes, start)
   


    
    return nodes, start, ground
    
def parse_neighbors(nodes, start):
    for node in nodes.values():
        node = Node(node.symbol, node.x, node.y)

    for node in nodes.values():
        if node.is_start:
            continue
        for dir in dirsFromSym[node.symbol]:
            if (node.x + dir[0], node.y + dir[1]) in nodes:
                neighbor = nodes[(node.x + dir[0], node.y + dir[1])]
                node.add_neighbor(neighbor)

    for dir in [north, south, east, west]:
        if (start.x + dir[0], start.y + dir[1]) in nodes:
            neighbor = nodes[(start.x + dir[0], start.y + dir[1])]
            if start in neighbor.neighbors:
                start.add_neighbor(neighbor)

    n1 = list(start.neighbors)[0]
    n2 = list(start.neighbors)[1]
    dx1 = n1.x - start.x
    dy1 = n1.y - start.y
    dir1 = (dx1, dy1)
    dx2 = n2.x - start.x
    dy2 = n2.y - start.y
    dir2 = (dx2, dy2)
    if dir1 == north and dir2 == east:
        start.symbol = 'L'
    elif dir1 == north and dir2 == west:
        start.symbol = 'J'
    elif dir1 == south and dir2 == west:
        start.symbol = '7'
    elif dir1 == south and dir2 == east:
        start.symbol = 'F'

    return nodes, start


def getLoop(start):
    start.visited = True
    next = list(start.neighbors)[0]
    next.distance = 1
    loop = []
    loop.append(start)
    while all([x.visited for x in next.neighbors]) == False:
        next.visited = True
        pnext = next
        next = [x for x in list(next.neighbors) if x.visited == False][0]
        next.distance = pnext.distance + 1
        loop.append(next)
    

    return loop
    

def star1(data):
    _, start, _ = data

    loop = getLoop(start) 
    # print(loop[(2,0)].symbol, loop[(2,0)].distance)
    return max([x.distance for x in loop])



    
    

def star2(data):
    nodes, start, ground = data
    for n in nodes.values():
        n.visited = False
    nodes, start = parse_neighbors(nodes, start)
    loop = getLoop(start)
    loopDict = {x.x : x for x in loop}
    for n in nodes.values():
        if (n.x, n.y) not in loopDict:
            ground[(n.x, n.y)] = Ground(n.x, n.y, sizeX, sizeY)
    points = [(x.x, x.y) for x in loop]
    poly = Polygon(points)
    contained = 0

    
    for g in ground.values():
        if poly.contains(Point(g.x, g.y)):
            g.inside = True
            contained += 1
            print(g.x, g.y)
        else:
            g.inside = False
    return contained

    #leqavng this here... it passes all the tests but is wrong somehow
    corners = ['L', 'J', '7', 'F']
    cornerX = {'L' : '7', 'F': 'J'}
    cornerY = {'7' : 'L', 'F': 'J'}

    # for g in [ground[(2,6)]]:
    for g in ground.values():
        crossings = [0,0,0,0]
        x0 = g.x
        y0 = g.y
        x = 0
        y = y0
        while 0 <= x < sizeX:
            num = 0 if x < x0 else 1
            if (x, y) in loop and loop[(x, y)].symbol in corners:
                sym = loop[(x, y)].symbol
                
                x += 1
                while (x, y) in loop:
                    if loop[(x, y)].symbol in corners:
                        if sym in cornerX and loop[(x, y)].symbol == cornerX[sym]:
                            crossings[num] += 1
                        break
                    x += 1

            if (x, y) in loop and loop[(x, y)].symbol in ['|']:
                crossings[num] += 1
            x += 1
        x = x0
        y = 0
        while 0 <= y < sizeY:
            num = 2 if y < y0 else 3
            if (x, y) in loop and loop[(x, y)].symbol in corners:
                sym = loop[(x, y)].symbol
                
                y += 1
                while (x, y) in loop:
                    if loop[(x, y)].symbol in corners:
                        if sym in cornerY and loop[(x, y)].symbol == cornerY[sym]:
                            crossings[num] += 1
                        break
                    y += 1
            elif (x, y) in loop and loop[(x, y)].symbol in ['-']:
                crossings[num] += 1
            y += 1
        g.inside = all([x % 2 == 1 for x in crossings]) 
        
    
    return len([x for x in ground.values() if x.inside == True]) 




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