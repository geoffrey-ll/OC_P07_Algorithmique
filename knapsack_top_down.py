#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from os import path as ospath, mkdir as os_mkdir
from csv import DictReader as csv_DictReader
from sys import setrecursionlimit
from pprint import pprint


BUDGET = 500
user_args = sys_argv


setrecursionlimit(1500)


def read_actions_file(path, max_line):
    data_shares = [{"dummy": "dummy"}]
    last_line = int()
    with open(path, newline='') as sharesfile:
        reader = csv_DictReader(sharesfile)
        for row in reader:
            if max_line == -1 or reader.line_num <= max_line:
                price = float(row["price"])
                profit = float(row["profit"]) / 100
                if price <= 0 or profit <= 0:
                    continue
                data_shares.append(
                    {"name": row["name"],
                     "price": round(price, 2),
                     "profit": round(profit, 2),
                     "gain": round(price * profit, 2)}
                )
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    sharesfile.close()
    return data_shares, last_line


def knapsack(remaining_shares, budget, data_shares, cheapest):
    idx_budget = int(round(budget * 100, 0))

    if remaining_shares != 0 and\
            configurations[remaining_shares][idx_budget] != -1:
        return configurations[remaining_shares][idx_budget]
    if remaining_shares == 0 or budget < cheapest:
        return configurations[0]
    elif data_shares[remaining_shares]["price"] > budget:
        (gain, idx_share) = knapsack(remaining_shares - 1, budget,
                                     data_shares, cheapest)

    else:
        (gain_1, idx_share_1) = knapsack(remaining_shares - 1, budget,
                                         data_shares, cheapest)
        (gain_temp, idx_temp) = \
            knapsack(remaining_shares - 1,
                     round(budget - data_shares[remaining_shares]["price"], 2),
                     data_shares, cheapest)

        gain_2 = data_shares[remaining_shares]["gain"] + gain_temp
        idx_share_2 = [remaining_shares] + idx_temp

        if gain_2 >= gain_1:
            gain = round(gain_2, 2)
            idx_share = idx_share_2
        else:
            gain = gain_1
            idx_share = idx_share_1

    configurations[remaining_shares][idx_budget] = (gain, idx_share)
    return configurations[remaining_shares][idx_budget]


def write_file(data_shares, data_best):
    if ospath.exists("./results") is False:
        os_mkdir("./results")
    path, euro = "./results/result_knapsack_top_down.txt", "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of knapsack top-down.py:\n\n")
        file.write(f"{'name':^10}{'price':>8} {euro}{'profit':>8} %\n\n")

        prices = []
        for idx_share in data_best[1]:
            prices.append(data_shares[idx_share]["price"])
            file.write(
                f"{data_shares[idx_share]['name']:<10}"
                f"{data_shares[idx_share]['price']:>8.2f} {euro}"
                f"{data_shares[idx_share]['profit']:>8.4f} %\n")

        prices_best = sum(prices)
        file.write(f"\n{'Total price: ':<13}{prices_best:>8.2f} {euro}"
                   f"\n{'Profit: ':<13}{data_best[0]:>8.2f} {euro}")


def main_knapsack(path_file_action, max_line=-1, budget=BUDGET):
    global configurations

    data_shares, line_num = read_actions_file(path_file_action, max_line)
    remaining_shares = len(data_shares) - 1

    idx_budget = int(round(budget * 100 + 1, 0))

    configurations = [
        [-1 for i in range(idx_budget)]
        for j in range(remaining_shares)
    ]
    configurations.insert(0, (0, []))
    print("start")

    cheapest = min([item["price"] for item in data_shares[1:]])
    result = knapsack(remaining_shares, budget, data_shares, cheapest)
    print("config fini")
    write_file(data_shares, result)

    for_complexity_memory = [data_shares, configurations, result]
    del configurations
    return line_num, for_complexity_memory


if __name__ == "__main__":
    a_budget = BUDGET
    if len(user_args) == 3:
        a_budget = float(user_args[2])
    main_knapsack(user_args[1], -1, a_budget)
