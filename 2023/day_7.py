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

def compareHands(h1, h2):
    if h1[0] == h2[0]:
        for i in range(5):
            c1 = getCardType(str(h1[1])[i])
            c2 = getCardType(str(h2[1])[i])
            if c1 < c2:
                return -1
            if c1 > c2:
                return 1
        return 1
    else:
        if h1[0] < h2[0]:
            return -1
        else:
            return 1

def star1(hb):
    cmp_key = cmp_to_key(compareHands)
    sorted_hands = list((sorted(hb, key=cmp_key)))
    ret = 0
    for i in range(len(sorted_hands)):
        ret += (i+1) * sorted_hands[i][2]
    return ret

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
    new_data = []
    for hand in data:
        handType = createBestHand(hand)[0]
        # print("hand:", hand, "best:", createBestHand(hand), "type:", handType)
        new_data.append((handType, hand[1], hand[2]))
    
    return star1(new_data)

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