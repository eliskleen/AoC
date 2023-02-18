import collections
from copy import deepcopy
from functools import cmp_to_key
import time
from parse import parse
from queue import PriorityQueue



def day_():
    path = "data.txt"
    path = "test-data.txt"

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
        valves = {}
        rows = f.read().splitlines()
        for r in rows:
            if r.count("valves") > 0:
                p = parse("Valve {} has flow rate={}; tunnels lead to valves {}", r)
                connections = p[2].split(", ")
            else :
                p = parse("Valve {} has flow rate={}; tunnel leads to valve {}", r)
                connections = [p[2]]
            v = Valve(p[0], int(p[1]), connections, 30)
            valves.update({v.name: v})
    return valves

class Valve:
    def __init__(self, name, flow_rate, connections, timeLeft):
        self.name = name
        self.flow_rate = flow_rate
        self.connections = connections  
        self.total_flow = 0
        self.opened = flow_rate == 0
        self.timeLeft = timeLeft
    def copy(self):
        name = self.name
        flow_rate = self.flow_rate
        connections = self.connections
        total_flow = self.total_flow
        opened = self.opened
        timeLeft = self.timeLeft
        v = Valve(name, flow_rate, connections, timeLeft)
        v.total_flow = total_flow
        v.opened = opened
        return v

    def setTimeLeft(self, timeLeft):
        self.timeLeft = timeLeft
    
    def getTotalFlow(self):
        return self.total_flow if self.total_flow > 0 else self.flow_rate
        
    def open(self):
        if self.opened:
            return
        self.opened = True
        self.total_flow = self.flow_rate * self.timeLeft

    
    def __hash__(self) -> int:
        return hash(self.name) + hash(self.timeLeft)
    def __eq__(self, o: object) -> bool:
        return self.name == o.name and self.timeLeft == o.timeLeft
    def __str__(self) -> str:
        return f"Valve {self.name} has flow rate={self.flow_rate}; tunnels lead to valves {self.connections}" 

highesFlow = 0

# def findFlow(valves, start, maxCost, cost,flow, open):
#     if maxCost <= cost:
#         return
#     global highesFlow
#     # if start.name not in visited:
#         # visited.add(start.name)
#     # print("Len set path:" + str(len(set(path))))

#     if len(open) >= len(valves):
#         print("Len open:" + str(len(open)))
#         return

#     for name in valves[start.name].connections:
#         if name == start.name:
#             continue
#         child = valves[name]
#         if name in open or child.flow_rate == 0:
#             open.add(name)
#             cc = cost + 1
#             findFlow(valves, child, maxCost, cc, flow, set(deepcopy(open)))
#         else:
#             cf = flow
#             cc = cost + 2
#             if cc >= maxCost:
#                 return
#             if cf + getMaxLeft(open, valves, maxCost, cc) < highesFlow:
#                 return
#             if name not in open:
#                 open.add(name)
#                 cf += (child.flow_rate * (maxCost - cc))
#             if cf + getMaxLeft(open, valves, maxCost, cc) < highesFlow:
#                 return
#             if cf > highesFlow:
#                 highesFlow = cf
#                 print(f"New highes flow: {highesFlow} at cost: {cc}")
#             findFlow(valves, child, maxCost, cc, cf, set(deepcopy(open)))
# def getMaxLeft(open, valves, maxCost, cost):
    # maxLeft = 0
    # for v in valves.values():
    #     if v.name not in open:
    #         maxLeft += v.flow_rate * (maxCost - cost)
    # return maxLeft



visited = set()
# queue = PriorityQueue()     #Initialize a queue


def findFlow(valves, time):
    numNodes = len(valves)
    valvList = list(valves.values())
    adjList = [[0 for i in range(numNodes)] for j in range(numNodes)]
    points = []
    for v in valves.values():
        points.append(v.flow_rate)
        for c in v.connections:
            x = valvList.index(v)
            y = valvList.index(valves[c])
            adjList[x][y] = 1 if x != y else 0
    dp = [[0 for j in range(time+1)] for i in range(numNodes)]
    for i in range(numNodes):
        dp[i][0] = points[i]
   
    for t in range(1, time+1):
        timeLeft = time - (t)
        for i in range(numNodes):
            for j in range(numNodes):
                maxPoints = points[i]*timeLeft
                if adjList[i][j] == 1 and t > 1:
                    maxPoints = max(dp[i][t], dp[j][t-2] + points[i]*timeLeft)
            dp[i][t] = maxPoints




    for r in dp:
        print(r)

    print("Max flow: " + str(max(dp[0])))

    return 0




def compSort(a, b):
    if a.getTotalFlow() == b.getTotalFlow():
        return 0
    elif a.getTotalFlow() > b.getTotalFlow():
        return -1
    else:
        return 1

def star1(data):
    visited = set()
    valves = data
    start = data["AA"]
    findFlow(valves, 30)
    #find rounte that gives the most flow


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
    stats.dump_stats(filename = 'profiling.prof')

if __name__ == '__main__':
    main()