#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv
from os import path as os_path, mkdir as os_mkdir
from csv import DictReader as csv_DictReader


BUDGET = 50_000
user_args = sys_argv


# Certaines variables/paramètres sont là uniquement pour l'analyse du script
# avec analyze_knapsack.py
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
    data_shares = [{"dummy": "dummy"}]
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
    price = int(round(float(row["price"]) * 100, 0))
    profit = round(float(row["profit"]) / 100, 4)
    gain = int(round(price * profit, 0))
    return name, price, profit, gain


def copy_data_share(data):
    """Copie les données transformées des actions en mémoire cache."""
    data_share = \
        {"name": data[0], "price": data[1], "profit": data[2], "gain": data[3]}
    return data_share


def preparate_knapsack(data_shares, x=0):
    """
        Mets en place les élèments nécessaires et communs pour les deux
        versions de knapsack, dont la matrice initialisé.

    :param data_shares: Données des actions.
    :param x: Pour avoir la matrice à la bonne taille selon l'appel depuis
        top_down ou bottom_up.

    :return:
        :number_shares: Nombres d'actions exploitables.
        :cheapest: Coût de l'action la moins chère.
        :configurations: Matrice initialisé pour débuter le knapsack.
    """
    number_shares = len(data_shares) - 1
    cheapest = min([data["price"] for data in data_shares[1:]])
    configurations = [
        [-1 for i in range(BUDGET + 1)] for j in range(number_shares + x)
    ]
    return number_shares, cheapest, configurations


def top_down(data_shares):
    """
        Le 'main' de la version top-down.

    :param data_shares: Données des actions.

    :return:
        :knapsack(): Le gain de la meilleur configuration.
        :configurations: La matrice des configurations.
        :__name__. Le nom de la fonction. Utile lors de l'écriture du résultat.
    """
    number_shares, cheapest, configurations = preparate_knapsack(data_shares)
    configurations.insert(0, [0])

    def knapsack_td(remaining_shares, budget):
        """
            La fonction récursive pour la version top-down du knapsack.

        :param remaining_shares: Le nombre d'actions restantes pour la
            récursivité en cours.
        :param budget: Le budget restant pour la récursivité en cours.

        :return:
            :configurations[remaining_shares][budget]: Le gain associé à la
                config en cours.
        """
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
            if gain_2 > gain_1:
                gain = gain_2
            else:
                gain = gain_1
        configurations[remaining_shares][budget] = gain
        return configurations[remaining_shares][budget]
    return \
        knapsack_td(number_shares, BUDGET), configurations, top_down.__name__


def bottom_up(data_shares):
    """
        La version bottom-up du knapsack.

    :param data_shares: Données des actions.

    :return:
        :configurations[-1][-1]: Le gain de la meilleur configuration.
        :configurations: La matrice des configurations.
        :__name__: Le nom de la fonction. Utile lors de l'écriture du résultat.
    """
    number_shares, cheapest, configurations = preparate_knapsack(data_shares,
                                                                 1)
    for remaining_shares in range(1, number_shares + 1):
        share_gain = data_shares[remaining_shares]["gain"]
        share_price = data_shares[remaining_shares]["price"]
        for budget in range(BUDGET + 1):
            if remaining_shares == 1 or budget < cheapest:
                current_gain = 0
            elif share_price > budget:
                current_gain = configurations[remaining_shares - 1][budget]
            else:
                previous_and_no_buy = \
                    configurations[remaining_shares - 1][budget]
                previous_and_buy = \
                    configurations[remaining_shares - 1][budget - share_price]
                gain_1 = previous_and_no_buy
                gain_2 = previous_and_buy + share_gain
                if gain_2 > gain_1:
                    current_gain = gain_2
                else:
                    current_gain = gain_1

            configurations[remaining_shares][budget] = current_gain
    return configurations[-1][-1], configurations, bottom_up.__name__


def find_shares_buy(data_shares, configurations):
    """
        En parcourant la matrice des configurations, trouve les index des
        actions qui sont utilisées pour la combinaison la plus rentable.

    :param data_shares: Données des actions.
    :param configurations: Matrice des configurations.

    :return:
        :shares_buy: Index des actions constituant la combinaison la plus
            rentable.
    """
    budget = BUDGET
    remaining_shares = len(data_shares) - 1
    shares_buy = []
    while remaining_shares >= 1:
        current_gain = configurations[remaining_shares][budget]
        share_gain = data_shares[remaining_shares]["gain"]
        share_price = data_shares[remaining_shares]["price"]
        try:
            previous_gain = configurations[remaining_shares - 1][budget -
                                                                 share_price]
        except IndexError:
            previous_gain = 0

        if share_price <= budget:
            if current_gain - share_gain == previous_gain or \
                    current_gain - share_gain == 0:
                shares_buy.append(remaining_shares)
                budget -= share_price
        remaining_shares -= 1
    return shares_buy


def write_file_result(data_shares, shares_buy, gain_best, name_def):
    """Écrit le résultat obtenu dans un fichier .txt."""
    if os_path.exists("./results") is False:
        os_mkdir("./results")
    path, euro = f"./results/{name_def}_result.txt", "\u20AC"

    with open(path, 'w', newline='', encoding="UTF-8") as file:
        file.write(f"Result of knapsack : {name_def.replace('_', '-')}:\n\n")
        file.write(f"{'name':^10}{'price':>8} {euro}{'profit':>8} %\n\n")

        price_best = 0
        for idx_share in shares_buy:
            price_best += data_shares[idx_share]["price"]
            file.write(
                f"{data_shares[idx_share]['name']:<10}"
                f"{data_shares[idx_share]['price'] / 100:>8.2f} {euro}"
                f"{data_shares[idx_share]['profit']:>8.4f} %\n")

        file.write(f"\n{'Total price':<11}:{price_best / 100:>8.2f} {euro}"
                   f"\n{'Total gain':<11}:{gain_best / 100:>8.2f} {euro}")
    file.close()


def description():
    """Description des paramètres requis et optionnels pour le script."""
    return print("\nRequiered parameter:\n"
                 "    Shares file (format csv)\n"
                 "    Option:\n"
                 "        bu => for bottom-up\n"
                 "        td => for top-down"
                 "\nOptional parameter:\n"
                 "    Budget (format xx.yy)"
                 "\nExemple:\n"
                 "    python knapsack.py shares.csv bu 226.35")


def main_knapsack(path_file_shares, option, max_line=-1):
    """
        Le main de knapsack.py.

    :param path_file_shares:
        Correspond à l'argument[1] donné par l'utilisateur.
    :param option: Pour indiquer s'il faut utiliser top_down ou bottom_up.
        Correspond à l'argument[2] donnée par l'utilisateur.
    :param max_line: Pour l'analyzer.

    :return: Sont là uniquement pour l'analyzer.
        :line_num: Numéro de la dernière ligne lue du .csv.
        :vars_to_analyze: Variable à peser pour la complexité spatiale.
    """
    # line_num pour l'analyse
    print("start")
    data_shares, line_num = read_shares_file(path_file_shares, max_line)

    if option == "bu":
        result, configurations, name_def = bottom_up(data_shares)
    elif option == "td":
        result, configurations, name_def = top_down(data_shares)
    else:
        description()
        return exit()

    shares_buy = find_shares_buy(data_shares, configurations)
    write_file_result(data_shares, shares_buy, result, name_def)
    print("Finished")

    # Pour l'analyse
    vars_to_analyze = [data_shares, result, configurations, shares_buy]
    return line_num, vars_to_analyze


if __name__ == "__main__":
    try:
        if len(user_args) == 4:
            BUDGET = int(round(float(user_args[3]) * 100, 0))
        main_knapsack(user_args[1], user_args[2].lower(), -1)

    except IndexError as e:
        print(e)
        description()
