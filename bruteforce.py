#! /usr/bin/env python3
# coding: utf-8


from itertools import combinations as itcombinations
from os import path as ospath, mkdir as osmkdir
from csv import DictReader as csvDictReader


BUDGET = 500
file_actions = "actions.csv"  # Fichier avec les 20 actions


def read_actions_file(path, size=-1):
    data_actions = {}
    with open(path, newline='') as actionsfile:
        # counter_actions = 0
        reader = csvDictReader(actionsfile)
        # with counter_actions <
        for row in reader:
            data_actions[row["Action"]] = {"Price": row["price"],
                                           "Profit": float(row["profit"])}
            # counter_actions += 1
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
            profit_price_comb = [profit, price, combination]
            temp_best = compare_combinations(temp_best, profit_price_comb)
    return temp_best


def compare_combinations(temp_best, profit_price_comb):
    condition1, condition2 = False, False
    if profit_price_comb[0] > temp_best["Profit"]:
        condition1 = True
    else:
        if profit_price_comb[1] < temp_best["Price"]:
            print("je suis ici")
            condition2 = True
    if condition1 or condition2 is True:
        temp_best["Profit"] = float(profit_price_comb[0])
        temp_best["Price"] = profit_price_comb[1]
        temp_best["Combination"] = profit_price_comb[2]
    return temp_best


def write_file(data_actions, data):
    if ospath.exists("./results") is False:
        osmkdir("./results")
    path, euro = "./results/result_bruteforce.txt", "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of bruteforce.py:\n\n")
        file.write(f"{'name':^10} {'price':>7} {euro} {'profit':>7} %\n\n")

        for action in data["Combination"]:
            file.write(
                f"{action:<10}"
                f" {data_actions[action]['Price']:>7} {euro}"
                f" {data_actions[action]['Profit']:>7.4f} %\n")

        file.write(f"\nTotal price: {data['Price']} {euro}"
                   f"\nProfit: {data['Profit']:.2f} {euro}")


def main_bruteforce(path_file_actions, size=-1):
    data_actions = read_actions_file(path_file_actions, size)
    print("Searching the most affordable combination")
    best_combination = find_combinations_possible(data_actions)
    write_file(data_actions, best_combination)
    print("Finished")


if __name__ == "__main__":
    main_bruteforce(file_actions)
