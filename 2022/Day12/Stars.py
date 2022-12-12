import math
import time
import collections
from cuts import *
from heapq import merge


def day_():
    path = "data.txt"
    # path = "test-data.txt"

    start_time = time.perf_counter()
    data = get_data(path)

    time1 = time.perf_counter()

    ans1 = star1(data)
    time2 = time.perf_counter()

    ans2 = star2(data)
    time3 = time.perf_counter()

    load_time = time1 - start_time
    star1_time = time2 - time1
    star2_time = time3 - time2
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 time: {star1_time}')
        print(f'Star 2 time: {star2_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: {ans2}')

def get_data(path):
    with open(path) as f:
        m = collections.defaultdict()
        rows = f.read().splitlines()
        for y in range(len(rows)):
            rows[y] = [*rows[y]]
            for x in range(len(rows[y])):
                if rows[y][x] == "S":
                    m[(x,y)] = Maze_Node(height=0, position=(x,y))
                    start = m[(x,y)]
                elif rows[y][x] == "E":
                    m[(x,y)] = Maze_Node(height=ord("z")-ord("a"), position=(x,y))
                    end = m[(x,y)]
                else:
                    m[(x,y)] = Maze_Node(height=ord(rows[y][x]) - ord("a"), position=(x,y))
        for n in m.values():
            n.end = end
            n.start = start
        return (m, start, end)

#node for A* algorith
class Maze_Node:
    def __init__(self, parent = None, position = None, end = None, height = None):
        self.position = position
        if parent is None:
            self.g = 0
            self.h = 0
            self.f = 0
        else:
            self.g = parent.g + 1
            self.h = distToGoal(self, end)
            self.f = self.g + self.h
            self.parent = parent
        if height is not None:
            self.height = height

    def get_pos(self):
        if self.position is not None: 
            return self.position
        return None
    def __eq__(self, other):
        return self.position == other.position

    def __hash__(self):
        return hash(self.position)


def distToGoal(node, end):
    pos = node.get_pos()
    x = pos[0] - end.position[0]
    y = pos[1] - end.position[1]
    return math.sqrt(abs(x)**2 + abs(y)**2)

def astar(maze, start, end):
    start_node = start
    start_node.g = start_node.f = 0
    start_node.h = distToGoal(start_node, end)
    end_node = end
    end_node.g = end_node.h = end_node.f = 0
    open_list = collections.OrderedDict()
    closed_list = collections.OrderedDict()
    open_list[start_node.position] = start_node

    while len(open_list) > 0:
        q = open_list.popitem(0)[1] #here it is sorted
        for dir in [(0,1),(0,-1),(1,0),(-1,0)]:
            new_pos = (q.position[0] + dir[0], q.position[1] + dir[1])
            if new_pos not in maze.keys():
                continue #out of bounds
            
            if maze[new_pos].height - maze[q.position].height > 1:
                continue #too high
            node = Maze_Node(parent=q, position=new_pos, end=end)
            if node in open_list.items():
                continue
            closed_node = closed_list.get(new_pos)
            if closed_node is not None and node.f >= closed_node.f:
                continue
            if new_pos == end.position:
                return Maze_Node(q, new_pos, end)
            open_list[new_pos] = node
            merge(*[(kv[1].f, kv) for kv in open_list.items()])
        closed_list[q.position] = q

def star1(data):
    (maze, start, end) = data
    q = astar(maze, start, end)
    return q.g

def star2(data):
    (maze, start, end) = data
    aa = []
    for e in maze.values():
        if e.height == 0:
            aa.append(e)
    shortest = 1000000
    longerInRow = 0
    merge(*[(distToGoal(a, end), a) for a in aa])
    for a in aa:
        print(f"shortest: {shortest}")
        q = astar(maze, a, end)
        if q is not None:
            if q.g < shortest:
                shortest = q.g
                longerInRow = 0
            else:
                longerInRow += 1
        else:
            longerInRow += 1
        if(longerInRow > 100):
            break
    return shortest

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    stats.dump_stats(filename = 'profiling.prof')

if __name__ == '__main__':
    main()