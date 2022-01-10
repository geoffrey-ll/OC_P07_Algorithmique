#! /usr/bin/env python3
# coding: utf-8


from itertools import combinations as it_combinations
from os import path as ospath, mkdir as os_mkdir
from csv import DictReader as csv_DictReader


BUDGET = 500
file_actions = "actions.csv"  # Fichier avec les 20 actions


def read_actions_file(path, max_line):
    data_actions = {}
    last_line = int()
    with open(path, newline='') as actionsfile:
        reader = csv_DictReader(actionsfile)
        for row in reader:
            if max_line == -1 or reader.line_num <= max_line:
                data_actions[row["Action"]] = {"Price": row["price"],
                                               "Profit": float(row["profit"])}
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    actionsfile.close()
    return data_actions, last_line


def find_combinations_possible(data_actions):
    temp_best = {"Profit": 0}
    for i in range(len(data_actions) + 1):
        temp = it_combinations(data_actions, i)
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
        os_mkdir("./results")
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


def main_bruteforce(path_file_actions, max_line=-1):
    data_actions, line_num = read_actions_file(path_file_actions, max_line)
    print("Searching the most affordable combination")
    best_combination = find_combinations_possible(data_actions)
    write_file(data_actions, best_combination)
    print("Finished")

    for_complexity_memory = [data_actions, best_combination]
    return line_num, for_complexity_memory


if __name__ == "__main__":
    main_bruteforce(file_actions)
