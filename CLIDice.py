#!/usr/bin/env python3.10

import sys
import random
import re
from pprint import pprint

from Print.help import dice_help
from Print.help2 import dice_help_two
from Print.credits import dice_credits

standard_dice = [2, 4, 6, 8, 10, 00, 12, 20, 30, 100]


def roll(dice: int, idv_mod: int, ignore_zero: bool = False):
    if dice != 00:
        diceroll = random.randrange(1, dice+1)+idv_mod
        return diceroll
    elif dice == 00:
        diceroll = random.randrange(0, 100, 10) + (1 if ignore_zero else 0)
        return diceroll


def parse_roll(query: str, ignore_zero: bool = False):
    q = query.split('d', 1)
    quant = int(q[0])
    which = q[1]
    mod = 0
    mod_each = 0
    results = []
    if "+" in which:
        t = which.split("+")
        which = t[0]
        if t[1].startswith("m"):
            mod += int(t[1].strip("m"))
        if t[1].startswith("e"):
            mod_each += int(t[1].strip("e"))
        try:
            if t[2].startswith("m"):
                mod += int(t[2].strip("m"))
            if t[2].startswith("e"):
                mod_each += int(t[2].strip("e"))
        except IndexError:
            pass

    which = int(which)
    if which not in standard_dice:
        print("An unconventional dice roll. I'll still roll it anyway...")
    total = 0
    for r in range(0, quant):
        work = roll(which, mod_each, ignore_zero)
        results.append(work)
        total += work
    total += mod
    return total, results


def parse(query: str, ignore_zero: bool):
    argument = query.split(" ")
    results = []
    roll_pattern = re.compile(r"[0-9]+d[0-9]+\+?[m,e]?-?[0-9]?\+?[m,e]?-?[0-9]?")
    mod_pattern = re.compile(r"\+t-?[0-9]?")
    for item in argument:
        if roll_pattern.match(item):
            p_roll, indv_rolls = parse_roll(item, ignore_zero)
            if len(indv_rolls) == 1:
                print(str(item) + " rolled " + str(p_roll)+"!")
            else:
                print(str(item) + " rolled " + str(p_roll) + "!")
                print("Individual results:")
                pprint(indv_rolls)
            results.append(p_roll)
        if mod_pattern.match(item):
            results.append(int(item.strip("+t")))
            print("Plus "+item.strip("+t"))
        if not (roll_pattern.match(item) or mod_pattern.match(item)):
            print("I think you might have entered something wrong. Check this one: "+item)
            print("")
            break
    if sum(results) != 0:
        print("The total of all rolls is: "+str(sum(results)))
        print("")
    else:
        print("No rolls made.")


def main():
    loop = True
    ignore_zero = False
    print("CLI Dice Roller")
    print('Type out what you want rolled. Use "help" for assistance, or "quit" when done.')
    print("")
    while loop:
        i = input(">")
        match i:
            case "help":
                dice_help()
            case "help 2":
                dice_help_two()
            case "credits":
                dice_credits()
            case "license":
                file = str(sys.path[0] + "/LICENSE")
                with open(file, "r") as f:
                    for line in f:
                        print(line)
            case "00 mode":
                ignore_zero = not ignore_zero
                match ignore_zero:
                    case True:
                        print("Adding 1 to 00 rolls.")
                        print("")
                    case False:
                        print("Not adding 1 to 00 rolls.")
                        print("")
            case "coinflip":
                flip = roll(2, 0)
                match flip:
                    case 1:
                        print("HEADS!")
                    case 2:
                        print("TAILS!")
            case "quit":
                loop = False
            case other:
                parse(other, ignore_zero)


if __name__ == '__main__':
    if sys.stdin.isatty():
        main()
