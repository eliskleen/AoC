import collections
import math
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
        return list(map(lambda d : d.split(" "), f.read().splitlines()))

class Rope:
    def __init__(self, knots = 1):
        self.knots = [(0,0) for i in range(knots)]


        self.tailVisited = collections.defaultdict()
        self.tailVisited[(0,0)] = True
    

    def nextIsLast(self, k):
        return k == len(self.knots)-2
    #calc euclidian dist from head to tail
    def dist(self, k):
        return math.sqrt((self.knots[k][0] - self.knots[k+1][0])**2 + (self.knots[k][1] - self.knots[k+1][1])**2)
    def moveTail(self,k):
        if self.dist(k) <= 1:
            return 
        dx = dy = 0
        if self.knots[k][1] == self.knots[k+1][1]: # fix in x
            if self.dist(k) > 1:
                dx = -1 if self.knots[k][0] < self.knots[k+1][0] else 1
        elif self.knots[k][0] == self.knots[k+1][0]: # fix in y
            if self.dist(k) > 1:
                dy = -1 if self.knots[k][1] < self.knots[k+1][1] else 1
        else: # diagonal
            if self.dist(k) > 2:
                dx = -1 if self.knots[k][0] < self.knots[k+1][0] else 1
                dy = -1 if self.knots[k][1] < self.knots[k+1][1] else 1
        self.knots[k+1] = (self.knots[k+1][0]+dx, self.knots[k+1][1]+dy)
        if(k+1 == len(self.knots)-1):
            self.tailVisited[self.knots[k+1]] = True
        else:
            self.moveTail(k+1)       
      
    def move(self, direction, s):
        if direction == "U":
            self.moveUp(s, 0)
        if direction == "D":
            self.moveDown(s, 0)
        if direction == "L":
            self.moveLeft(s, 0)
        if direction == "R":
            self.moveRight(s, 0)
    def moveUp(self, steps, k):
        for i in range(steps):
            self.knots[k] = (self.knots[k][0], self.knots[k][1] - 1)
            self.moveTail(k)
    def moveDown(self, steps, k):
        for i in range(steps):
            self.knots[k] = (self.knots[k][0], self.knots[k][1] + 1)
            self.moveTail(k)
    def moveLeft(self, steps,k):
        for i in range(steps):
            self.knots[k] = (self.knots[k][0] - 1, self.knots[k][1])
            self.moveTail(k)
    def moveRight(self, steps,k):
        for i in range(steps):
            self.knots[k] = (self.knots[k][0] + 1, self.knots[k][1])
            self.moveTail(k)


def star1(data):
    r = Rope(2)
    for (d, s) in data:
        s = int(s)
        r.move(d, s)
    return len(r.tailVisited)

def star2(data):
    r = Rope(10)
    for (d,s) in data:
        s = int(s)
        r.move(d, s)
    return len(r.tailVisited)

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