from itertools import combinations as itcombinations
from os import path as ospath
from os import mkdir as osmkdir
from csv import DictReader as csvDictReader
from csv import DictWriter as csvDictWriter
from operator import itemgetter as opitemgetter


what_file = "actions-5"  # Fichier avec les 5 première actions
# what_file = "actions"  # Fichier avec les 20 actions

list_actions = []
data_actions = {}
results_combinations = []
combinations_no_expensive = []
list_of_decision = []


def read_actions_file():
    with open(what_file + ".csv", newline='') as actionsfile:
        reader = csvDictReader(actionsfile)
        for row in reader:
            list_actions.append(row["Action"])
            data_actions[row["Action"]] = {"Cost": row["cost"],
                                           "Profit": row["profit"]}


def find_combinations_possible():
    combinations = []
    for i in range(len(list_actions) + 1):
        temp = itcombinations(list_actions, i)
        for elmt in temp:
            combinations.append(elmt)
    return combinations


def cost_profit(combination):
    result_combination = {}
    cost = 0
    profit = 0
    for action in list_actions:
        result_combination[action] = "No buy"

    for action in combination:
        result_combination[action] = "Buy"
        cost_temp = int(data_actions[action]["Cost"])
        profit_temp = float(data_actions[action]["Profit"])
        cost += cost_temp
        profit += cost_temp * profit_temp
    result_combination["Cost"] = cost
    result_combination["Profit"] = float(format(profit, ".2f"))

    return results_combinations.append(result_combination)


def create_repo():
    if ospath.exists("./csv_file") is False:
        return osmkdir("./csv_file")


def write_file(name_file, data):
    print("Writing csv in progress")
    fieldnames = ["Profit", "Cost"]
    for action in list_actions:
        fieldnames.append(action)
    with open("./csv_file/" + name_file + ".csv", 'w', newline='') as file:
        writer = csvDictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for result in data:
            writer.writerow(result)
    print("Writing csv finished")


def excluding_too_expensive_combination():
    maximum = 500
    for result in results_combinations:
        if result["Cost"] <= maximum:
            combinations_no_expensive.append(result)


def sorting_results_retain():
    no_expensive_sorted = sorted(combinations_no_expensive,
                                 reverse=True, key=opitemgetter("Profit"))
    return no_expensive_sorted


def get_max_profit(liste):
    maxi = max(liste, key=opitemgetter("Profit"))
    list_of_decision.append(maxi)
    return maxi


def excluding_combination_buy(combination_retain, combinations):
    combinations_remaining = []
    actions_buy = []

    for key, value in combination_retain.items():
        if value == "Buy":
            actions_buy.append(key)
    if combination_retain != [] and actions_buy == []:
        return combinations_remaining

    for combination in combinations:
        exclude = "no"
        for action_buy in actions_buy:
            if combination[action_buy] == "Buy":
                exclude = "yes"
        if exclude == "no":
            combinations_remaining.append(combination)
    return combinations_remaining


def generate_list_of_decision():
    combinations_remaining = combinations_no_expensive
    while combinations_remaining != []:
        combination_retain = get_max_profit(combinations_remaining)
        combinations_remaining = excluding_combination_buy(
            combination_retain, combinations_remaining)


def main():
    read_actions_file()
    combinations = find_combinations_possible()
    print("Calculation cost/profit in progress")
    for combination in combinations:
        cost_profit(combination)
    print("Calculation cost/profit finished")
    create_repo()

    write_file("results_all", results_combinations)

    excluding_too_expensive_combination()
    write_file("combination_no_expensive", sorting_results_retain())

    generate_list_of_decision()
    write_file("list_of_decision", list_of_decision)


main()
