from itertools import combinations as itcombinations
from csv import DictReader as csvDictReader
from csv import DictWriter as csvDictWriter

from pprint import pprint as pp


what_file = "actions-5" # Fichier avec les 5 première actions
# what_file = "actions" # Fichier avec les 20 actions

list_actions = []
data_actions = {}
results_combinations = []


def read_actions_file():
    with open(what_file + ".csv", newline='') as actionsfile:
        reader = csvDictReader(actionsfile)
        for row in reader:
            list_actions.append(row["Action"])
            data_actions[row["Action"]] = {"Cost": row["cost"], "Profit": row["profit"]}

def find_combinations_possible(list_actions):
    combinations = []
    for i in range(len(list_actions) + 1):
        temp = itcombinations(list_actions, i)
        for elmt in temp:
            combinations.append(elmt)
    return combinations

def cost_profit(list_actions, combination):
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
    result_combination["Profit"] = format(profit, ".2f")

    return results_combinations.append(result_combination)

def main():
    read_actions_file()
    combinations = find_combinations_possible(list_actions)
    print("Calcul des coût/profit en cours")
    for combination in combinations:
        cost_profit(list_actions, combination)
    print("Calculs terminés")

    print_result()


def print_result():
    if len(results_combinations) <= 50:
        for result in results_combinations:
            print(result)
    else:
        for result in results_combinations[0:5]:
            pp(result)
        for result in results_combinations[-5:]:
            pp(result)

        print(""
              "Les 10 premiers et 10 derniers, d'un total de {} résultats"
              .format(len(results_combinations))
              )

main()
