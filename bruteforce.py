#! /usr/bin/env python3
# coding: utf-8


from itertools import combinations as itcombinations
from os import path as ospath, mkdir as osmkdir
from csv import DictReader as csvDictReader
from operator import itemgetter as opitemgetter


BUDGET = 500
file_actions = "actions.csv"  # Fichier avec les 20 actions


def read_actions_file(path):
    data_actions = {}
    with open(path, newline='') as actionsfile:
        reader = csvDictReader(actionsfile)
        for row in reader:
            data_actions[row["Action"]] = {"Price": row["price"],
                                           "Profit": row["profit"]}
    return data_actions


def find_combinations_possible(data_actions):
    combinations = []
    for i in range(len(data_actions) + 1):
        temp = itcombinations(data_actions, i)
        for combination in temp:
            combinations.append(combination)
    return combinations


def affect_price_profit(data_actions, combinations):
    print("Searching the most affordable combination")
    best_combinations = []
    temp_best_profit = float(0)
    for combination in combinations:

        price, profit = 0, 0
        for action in combination:
            price_temp = int(data_actions[action]["Price"])
            profit_temp = float(data_actions[action]["Profit"])
            price += price_temp
            profit += price_temp * profit_temp

        if price <= BUDGET and profit >= temp_best_profit:
            data_combination = {}
            data_combination["Profit"] = float(format(profit, ".2f"))
            data_combination["Price"] = price
            data_combination["Combination"] = combination
            if profit != temp_best_profit:
                best_combinations = [data_combination]
            else:
                best_combinations.append(data_combination)
            temp_best_profit = profit
    return find_best_combination(best_combinations)


def find_best_combination(best_combinations):
    if len(best_combinations) == 1:
        return best_combinations[0]
    else:
        best_combination = min(best_combinations, key=opitemgetter("Price"))
        return best_combination


def create_repo_results():
    if ospath.exists("./results") is False:
        return osmkdir("./results")


def write_file(data_actions, data_result):
    create_repo_results()
    path = "./results/result_bruteforce.txt"
    euro = "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of bruteforce.py:\n\n")
        for action in data_result["Combination"]:
            file.write(f"{action} {data_actions[action]['Price']} {euro}\n")
        file.write(f"\nTotal price: {data_result['Price']} {euro}"
                   f"\nProfit: {data_result['Profit']} {euro}")


def main(path_file_actions):
    data_actions = read_actions_file(path_file_actions)
    combinations = find_combinations_possible(data_actions)
    best_combination = affect_price_profit(data_actions, combinations)

    write_file(data_actions, best_combination)
    print("Finished")


main(file_actions)


