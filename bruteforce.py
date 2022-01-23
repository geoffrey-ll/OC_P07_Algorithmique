#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from os import path as ospath, mkdir as os_mkdir
from itertools import combinations as it_combinations
from csv import DictReader as csv_DictReader


BUDGET = 500
user_args = sys_argv

def read_actions_file(path, max_line):
    data_actions = {}
    last_line = int()
    with open(path, newline='') as actionsfile:
        reader = csv_DictReader(actionsfile)
        for row in reader:
            profit = round((float(row["profit"]) / 100), 2)
            price = round(float(row["price"]), 2)
            if max_line == -1 or reader.line_num <= max_line:
                data_actions[row["name"]] = {"price": price,
                                             "profit": profit}
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    actionsfile.close()
    return data_actions, last_line


def find_combinations_possible(data_actions, budget):
    temp_best = {"profit": 0}
    for i in range(len(data_actions) + 1):
        temp = it_combinations(data_actions, i)
        for combination in temp:
            temp_best = \
                affect_price_profit(data_actions, temp_best, combination,
                                    budget)
    return temp_best


def affect_price_profit(data_actions, temp_best, combination, budget):
    profit, price = 0, 0
    for name_action in combination:
        price_temp = data_actions[name_action]["price"]
        profit_temp = data_actions[name_action]["profit"]
        price += price_temp
        profit += price_temp * profit_temp
    if profit != 0:
        if price <= budget and profit >= temp_best["profit"]:
            profit_price_comb = [profit, price, combination]
            temp_best = compare_combinations(temp_best, profit_price_comb)
    return temp_best


def compare_combinations(temp_best, profit_price_comb):
    condition1, condition2 = False, False
    if profit_price_comb[0] > temp_best["profit"]:
        condition1 = True
    else:
        if profit_price_comb[1] < temp_best["price"]:
            condition2 = True
    if condition1 or condition2 is True:
        temp_best["profit"] = float(profit_price_comb[0])
        temp_best["price"] = profit_price_comb[1]
        temp_best["combination"] = profit_price_comb[2]
    return temp_best


def write_file(data_actions, data):
    if ospath.exists("./results") is False:
        os_mkdir("./results")
    path, euro = "./results/result_bruteforce.txt", "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of bruteforce.py:\n\n")
        file.write(f"{'name':^10}{'price':>8} {euro}{'profit':>8} %\n\n")

        for action in data["combination"]:
            file.write(
                f"{action:<10}"
                f"{data_actions[action]['price']:>8.2f} {euro}"
                f"{data_actions[action]['profit']:>8.4f} %\n")

        file.write(f"\n{'Total price: ':<13}{data['price']:>8.2f} {euro}"
                   f"\n{'Profit: ':<13}{data['profit']:>8.2f} {euro}")


def main_bruteforce(path_file_actions, max_line=-1, budget=BUDGET):
    data_actions, line_num = read_actions_file(path_file_actions, max_line)
    print("Searching the most affordable combination")
    best_combination = find_combinations_possible(data_actions, budget)
    write_file(data_actions, best_combination)
    print("Finished")

    for_complexity_memory = [data_actions, best_combination]
    return line_num, for_complexity_memory


if __name__ == "__main__":
    a_budget = BUDGET
    if len(user_args) == 3:
        a_budget = float(user_args[2])
    main_bruteforce(user_args[1], -1, a_budget)
