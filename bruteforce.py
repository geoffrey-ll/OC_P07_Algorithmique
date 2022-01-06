#! /usr/bin/env python3
# coding: utf-8


from itertools import combinations as itcombinations
from os import path as ospath, mkdir as osmkdir
from csv import DictReader as csvDictReader


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
    temp_best = {"Profit": 0}
    for i in range(len(data_actions) + 1):
        temp = itcombinations(data_actions, i)
        for combination in temp:
            temp_best = \
                affect_price_profit(data_actions, temp_best, combination)
    return temp_best


def affect_price_profit(data_actions, temp_best, combination):
    profit, price = 0, 0
    for action in combination:
        price_temp = int(data_actions[action]["Price"])
        profit_temp = float(data_actions[action]["Profit"])
        price += price_temp
        profit += price_temp * profit_temp
    if profit != 0:
        if price <= BUDGET and profit >= temp_best["Profit"]:
            data_combination = [profit, price, combination]
            temp_best = compare_combinations(temp_best, data_combination)
    return temp_best


def compare_combinations(temp_best, data_combination):
    condition1, condition2, condition3 = False, False, False
    if data_combination[0] > temp_best["Profit"]:
        condition1 = True
    else:
        if data_combination[1] < temp_best["Price"]:
            condition2 = True
        else:
            if len(data_combination[2]) < len(temp_best["Combination"]):
                condition3 = True
            else:
                pass
    if condition1 or condition2 or condition3 is True:
        temp_best["Profit"] = float(data_combination[0])
        temp_best["Price"] = data_combination[1]
        temp_best["Combination"] = data_combination[2]
    return temp_best


def write_file(data_actions, data):
    if ospath.exists("./results") is False:
        return osmkdir("./results")
    path, euro = "./results/result_bruteforce.txt", "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of bruteforce.py:\n\n")
        for action in data["Combination"]:
            file.write(f"{action} {data_actions[action]['Price']} {euro}\n")
        file.write(f"\nTotal price: {data['Price']} {euro}"
                   f"\nProfit: {data['Profit']:.2f} {euro}")


def main(path_file_actions):
    data_actions = read_actions_file(path_file_actions)
    print("Searching the most affordable combination")
    best_combination = find_combinations_possible(data_actions)
    write_file(data_actions, best_combination)
    print("Finished")


main(file_actions)
