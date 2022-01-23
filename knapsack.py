#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from os import path as ospath, mkdir as os_mkdir
from csv import DictReader as csv_DictReader
from sys import setrecursionlimit
from time import time as t_time


BUDGET = 50_000
user_args = sys_argv


setrecursionlimit(1500)


def read_actions_file(path, max_line):
    data_shares = [{"dummy": "dummy"}]
    last_line = int()
    with open(path, newline='') as sharesfile:
        reader = csv_DictReader(sharesfile)
        for row in reader:
            if max_line == -1 or reader.line_num <= max_line:
                price = int(round(float(row["price"]) * 100, 2))
                profit = float(row["profit"]) / 100
                gain = int(round(price * profit, 0))
                if price <= 0 or profit <= 0:
                    continue
                data_shares.append(
                    {"name": row["name"],
                     "price": price,
                     "profit": round(profit, 4),
                     "gain": gain}
                )
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    sharesfile.close()
    return data_shares, last_line


def top_down(data_shares):
    number_shares = len(data_shares) - 1
    cheapest = min([data["price"] for data in data_shares[1:]])
    configurations = [
        [-1 for i in range(BUDGET + 1)] for j in range(number_shares)
    ]
    configurations.insert(0, [0])

    def knapsack_td(remaining_shares, budget):
        if remaining_shares != 0 and\
                configurations[remaining_shares][budget] != -1:
            return configurations[remaining_shares][budget]
        if remaining_shares == 0 or budget < cheapest:
            return configurations[0][0]
        elif data_shares[remaining_shares]["price"] > budget:
            gain = knapsack_td(remaining_shares - 1, budget)

        else:
            gain_1 = knapsack_td(remaining_shares - 1, budget)
            gain_2 = knapsack_td(remaining_shares - 1, budget -
                                 data_shares[remaining_shares]["price"]) \
                + data_shares[remaining_shares]["gain"]
            if gain_2 >= gain_1:
                gain = gain_2
            else:
                gain = gain_1

        configurations[remaining_shares][budget] = gain
        return configurations[remaining_shares][budget]

    return \
        knapsack_td(number_shares, BUDGET), configurations, top_down.__name__


def bottom_up(data_shares):
    number_shares = len(data_shares) - 1
    cheapest = min([item["price"] for item in data_shares[1:]])
    configurations = [
        [-1 for i in range(BUDGET + 1)] for j in range(number_shares + 1)
    ]

    for remaining_shares in range(1, number_shares + 1):
        for budget in range(BUDGET + 1):
            action_gain = data_shares[remaining_shares]["gain"]
            action_price = data_shares[remaining_shares]["price"]
            previous_and_no_buy = configurations[remaining_shares - 1][budget]
            previous_and_buy = configurations[remaining_shares - 1][
                budget - action_price]

            if remaining_shares == 1 or budget < cheapest:
                current_gain = 0
            elif action_price > budget:
                current_gain = previous_and_no_buy
            else:
                gain_1 = previous_and_no_buy
                gain_2 = previous_and_buy + action_gain
                if gain_2 > gain_1:
                    current_gain = gain_2
                else:
                    current_gain = gain_1

            configurations[remaining_shares][budget] = current_gain

    return configurations[-1][-1], configurations, bottom_up.__name__


def find_shares_buy(budget, data_shares, configurations):
    remaining_shares = len(data_shares) - 1
    shares_buy = []
    while remaining_shares >= 1:
        current_gain = configurations[remaining_shares][budget]
        action_gain = data_shares[remaining_shares]["gain"]
        action_price = data_shares[remaining_shares]["price"]
        try:
            previous_gain = configurations[remaining_shares - 1][budget -
                                                                 action_price]
        except IndexError:
            previous_gain = 0

        if action_price < budget:
            if current_gain - action_gain == previous_gain or \
                    current_gain - action_gain == 0:
                shares_buy.append(remaining_shares)
                budget -= action_price
        remaining_shares -= 1
    return shares_buy


def write_file(data_shares, shares_buy, profit_best, name_def):
    if ospath.exists("./results") is False:
        os_mkdir("./results")
    path, euro = f"./results/{name_def}_result.txt", "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write(f"Result of knapsack : {name_def.replace('_', '-')}:\n\n")
        file.write(f"{'name':^10}{'price':>8} {euro}{'profit':>8} %\n\n")

        prices = []
        for idx_share in shares_buy:
            prices.append(data_shares[idx_share]["price"])
            file.write(
                f"{data_shares[idx_share]['name']:<10}"
                f"{data_shares[idx_share]['price'] / 100:>8.2f} {euro}"
                f"{data_shares[idx_share]['profit']:>8.4f} %\n")

        prices_best = sum(prices)
        file.write(f"\n{'Total price: ':<13}{prices_best / 100:>8.2f} {euro}"
                   f"\n{'Profit: ':<13}{profit_best / 100:>8.2f} {euro}")


def main_knapsack(path_file_action, max_line=-1):
    data_shares, line_num = read_actions_file(path_file_action, max_line)

    print("start")
    if user_args[2].lower() == "bu":
        start = t_time()
        result, configurations, name_def = bottom_up(data_shares)
    elif user_args[2].lower() == "td":
        start = t_time()
        result, configurations, name_def = top_down(data_shares)
    end = t_time()
    print(f"Résultat en : {end - start} secondes.")

    shares_buy = find_shares_buy(BUDGET, data_shares, configurations)
    write_file(data_shares, shares_buy, result, name_def)

    for_complexity_memory = [data_shares, shares_buy, result]
    return line_num, for_complexity_memory


if __name__ == "__main__":
    if len(user_args) == 4:
        BUDGET = int(round(float(user_args[3]) * 100, 0))
    main_knapsack(user_args[1], -1)
