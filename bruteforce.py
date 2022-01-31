#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from itertools import combinations as it_combinations


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


def find_combinations_possible(data_shares):
    """
       Itère sur toutes les combinaisons possibles.

    :param data_shares: Données des actions.

    :return:
        :price_gain_comb_of_best: liste contenant le prix, le gain et la
            combinaison de celle qui est la plus rentable.
    """
    price_gain_comb_of_best = [0, 0, []]
    for i in range(len(data_shares) + 1):
        temp = it_combinations(range(len(data_shares)), i)
        for combination in temp:
            if len(combination) == 0:
                continue
            price_gain_comb_of_best = \
                affect_price_gain(data_shares, price_gain_comb_of_best,
                                  combination)
    return price_gain_comb_of_best


def affect_price_gain(data_shares, price_gain_comb_of_best, combination):
    """
        Détermine le coût et le gain d'une combinaison.

    :param data_shares: Données des actions
    :param price_gain_comb_of_best: liste contenant le prix, le gain et la
            combinaison de celle qui est la plus rentable.
    :param combination: Combinaison en cours d'évaluation.

    :return:
        :price_gain_comb_of_best: liste contenant le prix, le gain et la
            combinaison de celle qui est la plus rentable.
    """
    price_comb, gain_comb = 0, 0
    for idx_share in combination:
        price_comb += data_shares[idx_share]["price"]
        gain_comb += data_shares[idx_share]["gain"]
    if price_comb <= BUDGET and gain_comb >= price_gain_comb_of_best[1]:
        price_gain_comb_temp = (price_comb, round(gain_comb, 2), combination)
        price_gain_comb_of_best = \
            compare_combinations(price_gain_comb_of_best, price_gain_comb_temp)
    return price_gain_comb_of_best


def compare_combinations(price_gain_comb_of_best, price_gain_comb_temp):
    """
        Compare la meilleure combinaison en mémoire avec celle en cours
        d'évaluation.

    :param price_gain_comb_of_best: liste contenant le prix, le gain et la
            combinaison de celle qui est la plus rentable.
    :param price_gain_comb_temp:  liste contenant le prix, le gain et la
            combinaison de celle en cours d'évaluation.

    :return:
        :price_gain_comb_of_best: liste contenant le prix, le gain et la
            combinaison de celle qui est la plus rentable.
    """
    if price_gain_comb_temp[1] == price_gain_comb_of_best[1] \
            and price_gain_comb_temp[0] > price_gain_comb_of_best[0]:
        return price_gain_comb_of_best
    else:
        return change_temp_comb(price_gain_comb_of_best, price_gain_comb_temp)


def change_temp_comb(price_gain_comb_of_best, price_gain_comb_temp):
    """
        Modifie les valeurs de l'ancienne meilleur combinaison, par celles de
        la nouvelle meilleure combinaison.

    :param price_gain_comb_of_best: liste contenant le prix, le gain et la
            combinaison de l'ancienne plus rentable combinaison.
    :param price_gain_comb_temp:  liste contenant le prix, le gain et la
            combinaison de celle en cours d'évaluation.

    :return:
        :price_gain_comb_of_best: liste contenant le prix, le gain et la
            combinaison de la nouvelle plus rentable combinaison.
    """
    price_gain_comb_of_best[0] = price_gain_comb_temp[0]
    price_gain_comb_of_best[1] = price_gain_comb_temp[1]
    price_gain_comb_of_best[2] = price_gain_comb_temp[2]
    return price_gain_comb_of_best


def main_bruteforce(path_file_shares, max_line=-1):
    """
        Le main de bruteforce.py.

    :param path_file_shares:
        Correspond à l'argument[1] donné par l'utilisateur.
    :param max_line: Pour l'analyzer.

    :return: Sont là uniquement pour l'analyzer.
        :line_num: Numéro de la dernière ligne lue du .csv.
        :vars_to_analyze: Variable à peser pour la complexité spatiale.
    """
    # line_num pour l'analyse
    data_shares, line_num = read_shares_file(path_file_shares, max_line)
    print("Searching the most affordable combination")
    data_best = find_combinations_possible(data_shares)
    write_file_result(data_shares, data_best, main_bruteforce.__name__[5:])
    print("Finished")

    # Pour l'analyse
    vars_to_analyze = [data_shares, data_best]
    return line_num, vars_to_analyze


if __name__ == "__main__":
    try:
        if len(user_args) == 3:
            BUDGET = round(float(user_args[2]), 2)
        main_bruteforce(user_args[1], -1)

    except IndexError as e:
        print(e)
        description(user_args[0])
