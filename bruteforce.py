#! /usr/bin/env python3
# coding: utf-8


from itertools import combinations as itcombinations
from os import path as ospath, mkdir as osmkdir
from csv import DictReader as csvDictReader
from operator import itemgetter as opitemgetter


what_file = "actions.csv"  # Fichier avec les 20 actions
BUDGET = 500


def read_actions_file(file):
    data_actions = {}
    with open(file, newline='') as actionsfile:
        reader = csvDictReader(actionsfile)
        for row in reader:
            data_actions[row["Action"]] = {"Price": row["price"],
                                           "Profit": row["profit"]}
    return data_actions


def find_combinations_possible(data_actions):
    combinations = []
    for i in range(len(data_actions) + 1):
        temp = itcombinations(data_actions, i)
        for elmt in temp:
            combinations.append(elmt)
    return combinations


def cost_profit(data_actions, combinations):
    print("Calculation cost/profit in progress")
    data_combinations = []
    for combination in combinations:
        data_combination = {}
        price, profit = 0, 0

        for action in combination:
            price_temp = int(data_actions[action]["Price"])
            profit_temp = float(data_actions[action]["Profit"])
            price += price_temp
            profit += price_temp * profit_temp

        data_combination["Profit"] = float(format(profit, ".2f"))
        data_combination["Price"] = price
        data_combination["Combination"] = combination

        data_combinations.append(data_combination)
    return data_combinations


def excluding_too_expensive_combinations(data_combinations):
    affordable_combinations = []
    for data_combination in data_combinations:
        if data_combination["Price"] <= BUDGET:
            affordable_combinations.append(data_combination)
    return affordable_combinations


def find_best_combination(data_combinations):
    affordable_combinations = \
        excluding_too_expensive_combinations(data_combinations)
    best_combination = max(affordable_combinations, key=opitemgetter("Profit"))
    return best_combination


def create_repo():
    if ospath.exists("./results") is False:
        return osmkdir("./results")


def write_file(data_actions, data_result):
    create_repo()
    path = "./results/result_bruteforce.txt"
    euro = "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of bruteforce.py:\n\n")
        for action in data_result["Combination"]:
            file.write(f"{action} {data_actions[action]['Price']} {euro}\n")
        file.write(f"\nTotal price: {data_result['Price']} {euro}"
                   f"\nProfit: {data_result['Profit']} {euro}")


def main():
    data_actions = read_actions_file(what_file)
    combinations = find_combinations_possible(data_actions)
    data_combinations = cost_profit(data_actions, combinations)
    best_combination = find_best_combination(data_combinations)
    write_file(data_actions, best_combination)


main()
