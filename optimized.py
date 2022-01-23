#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from os import path as os_path, mkdir as os_mkdir
from csv import DictReader as csv_DictReader


BUDGET = 500
user_args = sys_argv


def read_actions_file(file, max_line):
    data_actions = []
    last_line = int()
    with open(file, newline='') as actionsfile:
        reader = csv_DictReader(actionsfile)
        for row in reader:
            if max_line == -1 or reader.line_num <= max_line:
                if float(row["price"]) != 0:
                    data_actions.append(
                        {"name": row["name"],
                         "price": float(row["price"]),
                         "profit": float(float(row["profit"]) / 100)}
                    )
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    actionsfile.close()
    return data_actions, last_line


def sort_by_profit_rate(data_actions):
    data_sorted = sorted(data_actions, key=lambda x: x["profit"] / x["price"],
                         reverse=True)
    return data_sorted


def find_best_combination(data_sorted):
    profit_combination, price_combination, combination = 0, 0, []
    for data_action in data_sorted:
        if data_action["price"] > float(0) \
                and (price_combination + data_action["price"]) <= BUDGET:
            price_combination += data_action["price"]
            profit_combination += data_action["profit"] * data_action["price"]
            combination.append(data_action["name"])

    profit_price_comb_of_best = \
        [profit_combination, price_combination, combination]
    return profit_price_comb_of_best


def write_file(data_actions_reform, profit_price_comb_of_best):
    if os_path.exists("./results") is False:
        os_mkdir("./results")
    path, euro = "./results/optimized_result.txt", "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of optimized:\n\n")
        file.write(f"{'name':^10}{'price':>8} {euro}{'profit':>8} %\n\n")

        for action in profit_price_comb_of_best[2]:
            file.write(
                f"{action:<10}"
                f"{data_actions_reform[action]['price']:>8.2f} {euro}"
                f"{data_actions_reform[action]['profit']:>8.4f} %\n"
            )

        file.write(f"\n{'Total price: ':<13}"
                   f"{profit_price_comb_of_best[1]:8.2f} {euro}"
                   
                   f"\n{'Profit: ':<13}"
                   f"{profit_price_comb_of_best[0]:8.2f} {euro}")


def main_optimized(file, max_line=-1):
    data_actions, line_num = read_actions_file(file, max_line)
    data_sorted = sort_by_profit_rate(data_actions)
    profit_price_comb_of_best = find_best_combination(data_sorted)
    data_actions_reform = {}
    for data in data_sorted:
        data_actions_reform[data["name"]] = {"price": data["price"],
                                             "profit": data["profit"]}

    write_file(data_actions_reform, profit_price_comb_of_best)

    for_complexity_memory = [data_actions, data_sorted,
                             profit_price_comb_of_best, data_actions_reform]
    return line_num, for_complexity_memory


if __name__ == "__main__":
    if len(user_args) == 3:
        BUDGET = int(round(float(user_args[2]), 0))
    main_optimized(user_args[1], -1)
