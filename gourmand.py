#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from os import path as os_path, mkdir as os_mkdir
from csv import DictReader as csv_DictReader


BUDGET = 500
user_args = sys_argv


# Certaines variables/paramètres sont là uniquement pour l'analyse du script
# avec analyze_optimized.py
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
            utilisées.
        :last_line: La dernière ligne lue du .csv.
    """
    data_shares = []
    last_line = int()  # last_line pour l'analyse
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
    profit = round(float(row["profit"]) / 100, 4)
    gain = round(price * profit, 2)
    return name, price, profit, gain


def copy_data_share(data):
    """Copie les données transformées des actions en mémoire cache."""
    data_share = \
        {"name": data[0], "price": data[1], "profit": data[2], "gain": data[3]}
    return data_share


def sort_by_profit_rate(data_shares):
    """Trie les données des actions par profit décroissant."""
    return data_shares.sort(key=lambda x: x["profit"], reverse=True)


def find_best_combination(data_sorted):
    """
        Construit la meilleur combinaison en parcourant les actions par profit
        décroissant.

    :param data_sorted: Données des actions ordonnées par profit décroissant.
    :return:
    """
    price_comb, gain_comb, comb = 0, 0, []
    for data_share in data_sorted:
        price_temp = price_comb + data_share["price"]
        if price_temp <= BUDGET:
            price_comb = price_temp
            gain_comb = round(gain_comb + data_share["gain"], 2)
            comb.append(data_sorted.index(data_share))

    price_gain_comb_of_best = [price_comb, gain_comb, comb]
    return price_gain_comb_of_best


def write_file_result(data_shares, price_gain_comb_of_best):
    """Écrit le résultat obtenu dans un fichier .txt."""
    if os_path.exists("./results") is False:
        os_mkdir("./results")
    path, euro = "./results/gourmand_result.txt", "\u20AC"

    with open(path, 'w', newline='', encoding="UTF-8") as file:
        file.write("Result of gourmand:\n\n")
        file.write(f"{'name':^10}{'price':>8} {euro}{'profit':>8} %\n\n")

        for idx_share in price_gain_comb_of_best[2]:
            file.write(
                f"{data_shares[idx_share]['name']:<10}"
                f"{data_shares[idx_share]['price']:>8.2f} {euro}"
                f"{data_shares[idx_share]['profit']:>8.4f} %\n"
            )

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
                 "    python gourmand.py shares.csv 226.35")


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
    price_gain_comb_of_best = find_best_combination(data_shares)

    write_file_result(data_shares, price_gain_comb_of_best)

    # Pour l'analyse
    vars_to_analyze = [data_shares, price_gain_comb_of_best]
    return line_num, vars_to_analyze


if __name__ == "__main__":
    try:
        if len(user_args) == 3:
            BUDGET = int(round(float(user_args[2]), 0))
        main_gourmand(user_args[1], -1)

    except IndexError as e:
        print(e)
        description()
