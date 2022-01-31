#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from os import path as os_path, mkdir as os_mkdir
from itertools import combinations as it_combinations
from csv import DictReader as csv_DictReader


BUDGET = 500
user_args = sys_argv


# Certaines variables/paramètres sont là uniquement pour l'analyse du script
# avec analyze_bruteforce.py
#
# profit => un pourcentage
# gain => (prix * profit) en euro


def read_shares_file(path, max_line):  # max_line pour l'analyse
    """
        Lit le .csv contenant les données des actions.

    :param path: Chemin relatif du .csv des actions à lire.
    :param max_line: Valeur de la dernière ligne du .csv à lire
        (utile pour l'analyzer)

    :return:
        :data_shares: Les données des actions transformées et prêtes à être
            utilisées
        :last_line: La dernière ligne lue du .csv.
    """
    data_shares = []
    last_line = int()  # Pour l'analyse
    with open(path, newline='') as sharesfile:
        reader = csv_DictReader(sharesfile)
        for row in reader:
            if max_line == -1 or reader.line_num <= max_line:
                data = name, price, profit, gain = transform_data_share(row)
                if price <= 0 or profit <= 0 or gain <= 0:
                    continue
                data_shares.append(copy_data_share(data))
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    sharesfile.close()
    return data_shares, last_line


def transform_data_share(row):
    """
        Transforme les données de la ligne du .csv aux formats voulus.

    :param row: Le contenu d'une ligne du .csv.

    :return:
        :name, price, profit, gain: Les données transformées de la ligne.
    """
    name = row["name"]
    price = round(float(row["price"]), 2)
    profit = round((float(row["profit"]) / 100), 4)
    gain = round(price * profit, 2)
    return name, price, profit, gain


def copy_data_share(data):
    """Copie les données transformées des actions en mémoire cache."""
    data_share = \
        {"name": data[0], "price": data[1], "profit": data[2], "gain": data[3]}
    return data_share


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


def write_file_result(data_shares, price_gain_comb_of_best):
    """Écrit le résultat obtenu dans un fichier .txt."""
    if os_path.exists("./results") is False:
        os_mkdir("./results")
    path, euro = "./results/bruteforce_result.txt", "\u20AC"

    with open(path, 'w', newline='', encoding="UTF-8") as file:
        file.write("Result of bruteforce:\n\n")
        file.write(f"{'name':^10}{'price':>8} {euro}{'profit':>8} %\n\n")

        for idx_share in price_gain_comb_of_best[2]:
            file.write(
                f"{data_shares[idx_share]['name']:<10}"
                f"{data_shares[idx_share]['price']:>8.2f} {euro}"
                f"{data_shares[idx_share]['profit']:>8.4f} %\n")

        file.write(f"\n{'Total price':<11}:"
                   f"{price_gain_comb_of_best[0]:>8.2f} {euro}"
                   
                   f"\n{'Total gain':<11}:"
                   f"{price_gain_comb_of_best[1]:>8.2f} {euro}")
    file.close()


def description():
    """Description des paramètres requis et optionnels pour le script."""
    return print("\nRequiered parameter:\n"
                 "    Shares file (format csv)"
                 "\nOptional parameter:\n"
                 "    Budget (format xx.yy)"
                 "\nExemple:\n"
                 "    python bruteforce.py shares.csv 226.35")


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
    write_file_result(data_shares, data_best)
    print("Finished")

    # Pour l'analyse
    vars_to_analyze = [data_shares, data_best]
    return line_num, vars_to_analyze


if __name__ == "__main__":
    try:
        if len(user_args) == 3:
            BUDGET = (round(float(user_args[2]), 2))
        main_bruteforce(user_args[1], -1)

    except IndexError as e:
        print(e)
        description()
