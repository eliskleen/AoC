import collections
from copy import deepcopy
import time

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
        rows = f.read().splitlines()
        map = collections.defaultdict(lambda: '.')
        coords = []
        maxY = 0
        for r in rows:
            coords = [(int(c.split(',')[0]), int(c.split(',')[1])) for c in r.split(' -> ')]
            for i in range(len(coords)-1):
                if coords[i][0] == coords[i+1][0]:
                    start = min(int(coords[i][1]), int(coords[i+1][1]))
                    end = max(int(coords[i][1]), int(coords[i+1][1]))
                    for j in range(start, end+1):
                        map[(coords[i][0], j)] = '#'
                        maxY = max(maxY, j)
                else:
                    start = min(int(coords[i][0]), int(coords[i+1][0]))
                    end = max(int(coords[i][0]), int(coords[i+1][0]))
                    for j in range(start, end+1):
                        map[(j, coords[i][1])] = '#'
                        maxY = max(maxY, int(coords[i][1]))
        print(map)
        return (map, maxY)
    
class Cave:
    def __init__(self, data):
        self.map = data[0]
        self.maxY = data[1]
        self.walls = len(data[0])
    
    def dropSand(self, x,y):
        dirs = [(0, 1), (-1, 1), (1, 1)]
        canMove = True
        notFilled = True
        madeStep = False
        (x0, y0) = (x, y)
        while notFilled:
            canMove = True
            (x, y) = (x0, y0)
            while canMove:
                madeStep = False
                for (dx, dy) in dirs:
                    if (x+dx, y+dy) in self.map:
                            continue
                    # print(f"{(x+dx, y+dy)} in map: {(x+dx, y+dy) in self.map}")
                    madeStep = True
                    break
                if madeStep:
                    # print(f"({x+dx}, {y+dy}), madeStep")
                    (x, y) = (x+dx, y+dy)
                else:
                    canMove = False
                    self.map[(x, y)] = 'o'
                    # print(f"({x+dx}, {y+dy}), o")
                    break
                if y > self.maxY:
                    # print(f"({x+dx}, {y+dy}), break")
                    notFilled = False
                    break
    def dropSand2(self):
        dirs = [(0, -1), (-1, -1), (1, -1)]
        # for y in range(self.maxY-1, 0-1, -1):
        self.map[(500, 0)] = 'o'
        for y in range(1, self.maxY):
            w = ((y+1)*2)-1
            for x in range(500-(w//2), 500+(w//2)+1): #kanske +1
                if self.map[(x, y)] == '#':
                    continue
                for (dx, dy) in dirs:
                    if x + dx < 500-w//2 or x + dx > 500+w//2:
                        continue
                    if self.map[(x+dx, y+dy)] == 'o':
                        self.map[(x, y)] = 'o'
                        break

def star1(data):
    walls = len(data[0])
    map = deepcopy(data[0])
    cave = Cave((map, data[1]))
    cave.dropSand(500, 0)
    return len(cave.map) - walls

def star2(data):
    print("Star 2")
    cave = Cave((data[0], data[1]+2))
    cave.dropSand2()
    sand = len([k for k, v in cave.map.items() if v == 'o'])
    return sand

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