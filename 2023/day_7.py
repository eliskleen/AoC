import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
from functools import cmp_to_key

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
    return [(getHandType(x.split()[0]), x.split()[0], int(x.split()[1])) for x in raw.split('\n')]
    
def getHandType(hand):
    s = set(hand)
    if len(s) == 1:
        return 6 #five of a kind
    elif len(s) == 2: #could be four of a kind or full house
        for c in s:
            if hand.count(c) == 4:
                return 5 #four of a kind
        return 4 #full house
    elif len(s) == 3: #could be three of a kind or two pair
        for c in s:
            if hand.count(c) == 3:
                return 3 #three of a kind
        return 2 #two pair
    elif len(s) == 4: #one pair
        return 1
    else: #high card
        return 0

cardTypes = {'A': 12, 'K': 11, 'Q': 10, 'J': 9, 'T': 8, '9': 7, '8': 6, '7': 5, '6': 4, '5': 3, '4': 2, '3': 1, '2': 0}
def getCardType(c):
    return cardTypes[c]

def star1(hb):
    sorted_hands = list((sorted(hb, key=lambda x : (x[0], list(map(getCardType, x[1]))))))
    return sum([x[2]*(i+1) for i, x in enumerate(sorted_hands)])

def createBestHand(hand):
    cardTypes = {'A': 12, 'K': 11, 'Q': 10, 'T': 8, '9': 7, '8': 6, '7': 5, '6': 4, '5': 3, '4': 2, '3': 1, '2': 0}
    if not 'J' in hand[1]:
        return hand
    jokers = hand[1].count('J')
    jokerIndexes = [i for i, x in enumerate(hand[1]) if x == 'J']
    perms = list(itertools.product(cardTypes.keys(), repeat=jokers))
    maxHandValue = 0
    maxHand = hand
    for perm in perms:
        newHand = list(hand[1])
        for i in range(jokers):
            newHand[jokerIndexes[i]] = perm[i]
        val = getHandType((newHand))
        if val > maxHandValue:
            maxHandValue = val
            maxHand = (val, hand[1], hand[2])
    return maxHand 

def star2(data):
    global cardTypes
    cardTypes['J'] = -1
    return star1(map(createBestHand, data))

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    day = int(__file__.split('\\')[-1].split('_')[1].split('.')[0]) 
    stats.dump_stats(filename = f'profiling\\profiling{day}.prof')

# run with `py day_n.py -- a b` to submit both stars for day n
if __name__ == '__main__':
    main()