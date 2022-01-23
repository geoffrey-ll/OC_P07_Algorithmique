#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from os import path as ospath, mkdir as os_mkdir
from csv import DictReader as csv_DictReader
from sys import setrecursionlimit
from pprint import pprint


BUDGET = 500 * 100
user_args = sys_argv


setrecursionlimit(1500)


def read_actions_file(path, max_line):
    data_shares = [{"dummy": "dummy"}]
    last_line = int()
    with open(path, newline='') as sharesfile:
        reader = csv_DictReader(sharesfile)
        for row in reader:
            if max_line == -1 or reader.line_num <= max_line:
                price = int(float(row["price"]) * 100)
                profit = float(row["profit"]) / 100
                if price <= 0 or profit <= 0:
                    continue
                data_shares.append(
                    {"name": row["name"],
                     "price": price,
                     "profit": profit,
                     "gain": int(price * profit)}
                )
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    sharesfile.close()
    return data_shares, last_line


def knapsack(remaining_shares, budget_total, data_shares, cheapest):
    for remaining in range(remaining_shares + 1):
        for budget in range(budget_total + 1):
            if remaining == 0 or budget < cheapest:
                configurations[remaining][budget] = (0, [])

            elif data_shares[remaining]["price"] > budget:
                configurations[remaining][budget] = \
                    configurations[remaining - 1][budget]

            else:
                temp_1 = configurations[remaining - 1][budget][0]
                temp_2 = \
                    data_shares[remaining]["gain"] + \
                    configurations[remaining - 1]\
                        [budget - data_shares[remaining]["price"]][0]

                if temp_2 > temp_1:
                    configurations[remaining][budget] = \
                        (temp_2,
                         configurations[remaining - 1]\
                             [budget - data_shares[remaining]["price"]][1] +
                         [remaining])
                else:
                    configurations[remaining][budget] = \
                        (temp_1, configurations[remaining - 1][budget][1])

    return configurations[-1][-1]


def write_file(data_shares, data_best):
    if ospath.exists("./results") is False:
        os_mkdir("./results")
    path, euro = "./results/result_knapsack_bottom_up.txt", "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of knapsack bottom-up.py:\n\n")
        file.write(f"{'name':^10}{'price':>8} {euro}{'profit':>8} %\n\n")

        prices = []
        for idx_share in data_best[1]:
            prices.append(data_shares[idx_share]["price"])
            file.write(
                f"{data_shares[idx_share]['name']:<10}"
                f"{data_shares[idx_share]['price'] / 100:>8.2f} {euro}"
                f"{data_shares[idx_share]['profit']:>8.4f} %\n")

        prices_best = sum(prices)
        file.write(f"\n{'Total price: ':<13}{prices_best / 100:>8.2f} {euro}"
                   f"\n{'Profit: ':<13}{data_best[0] / 100:>8.2f} {euro}")


def main_knapsack(path_file_action, max_line=-1, budget=BUDGET):
    global configurations

    data_shares, line_num = read_actions_file(path_file_action, max_line)
    remaining_shares = len(data_shares) - 1

    configurations = [
        [-1 for i in range(budget + 1)]
        for j in range(remaining_shares + 1)
    ]
    configurations[0][0] = (0, [])
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
        a_budget = int(float(user_args[2]) * 100)
    main_knapsack(user_args[1], -1, a_budget)
