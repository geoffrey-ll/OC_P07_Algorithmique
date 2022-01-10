#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from os import path as ospath, mkdir as os_mkdir
from csv import DictReader as csv_DictReader


from time import time as t_time
from pprint import pprint


BUDGET = 500
user_args = sys_argv
data_actions = []
values_configuration = {}


def read_actions_file(path, max_line):
    last_line = int()
    with open(path, newline='') as actionsfile:
        reader = csv_DictReader(actionsfile)
        for row in reader:
            if max_line == -1 or reader.line_num <= max_line:
                price = int(row["price"])
                profit = float(float(row["profit"]) / 100)
                data_actions.append(
                    {"name": row["name"], "price": price,
                     "profit": profit, "gain": price * profit}
                )
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    actionsfile.close()
    return last_line


def find_best_combination(remaining_actions, budget):
    if (remaining_actions, budget) not in values_configuration:
        values_configuration[(remaining_actions, budget)] = float()
    if remaining_actions == 0 or budget == 0:
        gain = 0
    elif data_actions[remaining_actions]["price"] > budget:
        gain = find_best_combination(remaining_actions - 1, budget)
    else:
        temp1 = find_best_combination(remaining_actions - 1, budget)
        temp2 = data_actions[remaining_actions]["gain"] + \
            find_best_combination(remaining_actions - 1,
                                  budget - data_actions[remaining_actions]
                                  ["price"])
        gain = round(max(temp1, temp2), 2)
    values_configuration[(remaining_actions, budget)] = gain
    return gain


def find_max():
    print("len de configuration, gain trouvés : "
          f"{len(values_configuration.keys())}")
    # for config, valeur in values_configuration.items():
    #     if valeur == float(91.72):
    #         print(config)
    maxi = max(values_configuration.values())
    maxi2 = max(values_configuration, key=values_configuration.get)
    print(f"maxi {maxi}")
    print(f"maxi2 {maxi2}")


def main_knapsack(path_file_action, max_line=-1, budget=BUDGET):
    start = t_time()
    last_line = read_actions_file(path_file_action, max_line)
    remaining_actions = len(data_actions) - 1
    find_best_combination(remaining_actions, budget)
    find_max()
    end = t_time()
    print(f"runtime = {end - start}")


if __name__ == "__main__":
    a_budget = BUDGET
    if len(user_args) == 3:
        a_budget = float(user_args[2])
    main_knapsack(user_args[1], -1, a_budget)
