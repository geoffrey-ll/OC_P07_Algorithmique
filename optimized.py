#! /usr/bin/env python3
# coding: utf-8


from os import path as os_path, mkdir as os_mkdir
from csv import DictReader as csvDictReader
from operator import itemgetter as op_itemgetter


BUDGET = 500
what_file = "dataset1_Python+P7.csv"
# what_file = "dataset2_Python+P7.csv"


def read_actions_file(file):
    data_actions = []
    with open(file, newline='') as actionsfile:
        reader = csvDictReader(actionsfile)
        for row in reader:
            data_actions.append(
                {"name": row["name"],
                 "price": float(row["price"]),
                 "profit": float(float(row["profit"]) / 100)}
            )
    return data_actions


def sort_by_profit_rate(data_actions):
    data_sorted = \
        sorted(data_actions, key=op_itemgetter("profit"), reverse=True)
    return data_sorted


def find_best_combination(data_sorted):
    profit_combination, price_combination, combination = 0, 0, []
    for data_action in data_sorted:
        if data_action["price"] > float(0) \
                and (price_combination + data_action["price"]) < BUDGET:
            price_combination += data_action["price"]
            profit_combination += data_action["profit"] * data_action["price"]
            combination.append(data_action["name"])

    profit_price_comb = [profit_combination, price_combination, combination]
    return profit_price_comb


def write_file(data_actions_reform, profit_price_comb_of_best):
    if os_path.exists("./results") is False:
        os_mkdir("./results")
    path, euro = "./results/result_optimized.txt", "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of optimized.py:\n\n")
        file.write(f"{'name':^10} {'price':>7} {euro} {'profit':>7} %\n\n")

        for action in profit_price_comb_of_best[2]:
            file.write(
                f"{action:<10}"
                f" {data_actions_reform[action]['price']:>7} {euro}"
                f" {data_actions_reform[action]['profit']:>7.4f} %\n"
            )

        file.write(f"\nTotal price: {profit_price_comb_of_best[1]:.2f} {euro}"
                   f"\nProfit: {profit_price_comb_of_best[0]:.2f} {euro}")


def main(file):
    data_actions = read_actions_file(file)
    data_sorted = sort_by_profit_rate(data_actions)
    profit_price_comb_of_best = find_best_combination(data_sorted)
    data_actions_reform = {}
    for data in data_sorted:
        data_actions_reform[data["name"]] = {"price": data["price"],
                                             "profit": data["profit"]}

    write_file(data_actions_reform, profit_price_comb_of_best)


if __name__ == "__main__":
    main(what_file)
