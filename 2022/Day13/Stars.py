import collections
from functools import cmp_to_key
import time
from cuts import *

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
        pairs = f.read().split("\n\n")
        data = []
        for pair in pairs:
            pair = pair.split("\n")
            # print(f"pair: {pair}, eval(pair[0]): {eval(pair[0])}, eval(pair[1]): {eval(pair[1])}")
            data.append((eval(pair[0]), eval(pair[1])))
        # print(data)
        return data

    

def compare(l, r):
    p = False
    # print(l, r)
    if type(l) is int and type(r) is int:
        # print(l, r)
        if p: print(f"Ints, l: {l}, r: {r}")
        if l == r:
            if p: print(f"Equal: {l}, {r}")
            return "equal"
        return l < r
    if type(l) is list and type(r) is list:
        if p: print(f"Lists, l: {l}, r: {r}")
        for i in range(len(r)):
            if i >= len(l):
                if p: print("left ran out of elements")
                return True
            c = compare(l[i], r[i])
            if c == True:
                if p: print(f"left is smaller: {l[i]}, {r[i]}")
                return True
            if c == False:
                if p : print(f"right is smaller: {l[i]}, {r[i]}")
                return False
        if len(l) > len(r):
            if p: print("right ran out of elements")
            return False
    if type(l) is list and type(r) is int:
        if len(l) == 0:
            return True
        c = compare(l, [r])
        return c
    if type(l) is int and type(r) is list:
        if len(r) == 0:
            return False
        return compare([l], r)

def star1(data):
    iSum = 0
    i = 1
    for pair in data:
        c = compare(pair[0], pair[1])
        if c == True:
            iSum += i
        if c == "equal":
            print(f"Equal: {pair}")
        i += 1
    return iSum

def compSort(l, r):
    c = compare(l, r)
    if c == True:
        return -1
    if c == False:
        return 1
    return 0

def star2(data):
    div1 = [[2]]
    div2 = [[6]]
    packets = [div1, div2]
    for pair in data:
        packets.append(pair[0])
        packets.append(pair[1])
    print(packets)
    packets = sorted(packets, key=cmp_to_key(compSort))
    i1 = packets.index(div1)
    i2 = packets.index(div2)
    return (i1+1) * (i2+1)

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