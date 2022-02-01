#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv


from in_common import read_shares_file
from in_common import write_file_result
from in_common import description


BUDGET = 500
user_args = sys_argv


# Certaines variables/paramètres sont là uniquement pour l'analyse du script
# avec analyze_*.py et analyzer
#
# profit => un pourcentage
# gain => (prix * profit) en euro


def sort_by_profit_rate(data_shares):
    """Ordonne les données des actions par profit décroissant."""
    return data_shares.sort(key=lambda x: x["profit"], reverse=True)


def find_best_combination(data_sorted, cheapest):
    """
        Construit la meilleur combinaison en parcourant les actions par profit
        décroissant.

    :param data_sorted: Données des actions ordonnées par profit décroissant.
    :param cheapest: Prix de l'action la moins chère.

    :return: Les données de la combinaison au meilleur gain.
    """
    budget = BUDGET
    price_comb, gain_comb, comb = 0, 0, []
    for data_share in data_sorted:
        if budget < cheapest:
            break
        if data_share["price"] <= budget:
            budget = round(budget - data_share["price"], 2)
            price_comb = round(price_comb + data_share["price"], 2)
            gain_comb = round(gain_comb + data_share["gain"], 2)
            comb.append(data_sorted.index(data_share))

    price_gain_comb_of_best = [price_comb, gain_comb, comb]
    return price_gain_comb_of_best


def main_gourmand(path_file_shares, max_line=-1):
    """
        Le main de gourmand.py.

    :param path_file_shares:
        Correspond à l'argument[1] donné par l'utilisateur.
    :param max_line: Pour l'analyzer.

    :return: Sont là uniquement pour l'analyzer.
        :line_num: Numéro de la dernière ligne lue du .csv.
        :vars_to_analyze: Variable à peser pour la complexité spatiale.
    """
    # line_num pour l'analyse
    data_shares, line_num = read_shares_file(path_file_shares, max_line)
    sort_by_profit_rate(data_shares)
    cheapest = min(data["price"] for data in data_shares)
    data_best = find_best_combination(data_shares, cheapest)
    write_file_result(data_shares, data_best, main_gourmand.__name__[5:])

    # Pour l'analyse
    vars_to_analyze = [data_shares, data_best]
    return line_num, vars_to_analyze


if __name__ == "__main__":
    try:
        if len(user_args) == 3:
            BUDGET = round(float(user_args[2]), 2)
        main_gourmand(user_args[1], -1)

    except IndexError as e:
        print(e)
        description(user_args[0])
