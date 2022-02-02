#! /usr/bin/env python3
# coding: utf-8


from os import path as os_path, mkdir as os_mkdir
from csv import DictReader as csv_DictReader


# Certaines variables/paramètres sont là uniquement pour l'analyse du script
# avec analyze_*.py et analyzer
#
# profit => un pourcentage
# gain => (prix * profit) en euro


def read_shares_file(path, max_line, option=''):  # max_line pour l'analyse
    """
        Lit le .csv contenant les données des actions.

    :param path: Chemin relatif du .csv des actions à lire.
    :param max_line: Valeur de la dernière ligne du .csv à lire
        (utile pour l'analyzer)
    :param option: Définit si la fonction est appelée par knapsack.py ou pas.

    :return:
        :data_shares: Les données des actions transformées et prêtes à être
            utilisées
        :last_line: La dernière ligne lue du .csv.
    """
    data_shares = []
    if option == "kns":
        data_shares.insert(0, {"dummy": "dummy"})

    last_line = int()  # Pour l'analyse
    with open(path, newline='') as sharesfile:
        reader = csv_DictReader(sharesfile)
        for row in reader:
            if max_line == -1 or reader.line_num <= max_line:
                data = name, price, profit, gain = \
                    transform_data_share(row, option)
                if price <= 0 or profit <= 0 or gain <= 0:
                    continue
                data_shares.append(copy_data_share(data))
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    sharesfile.close()
    return data_shares, last_line


def transform_data_share(row, option=''):
    """
        Transforme les données de la ligne du .csv aux formats voulus.

    :param row: Le contenu d'une ligne du .csv.
    :param option: Définit si la fonction est appelée par knapsack.py ou pas.

    :return:
        :name, price, profit, gain: Les données transformées de la ligne.
    """
    name = row["name"]
    profit = round((float(row["profit"]) / 100), 4)
    if option == "kns":
        price = int(round(float(row["price"]) * 100, 0))
        gain = int(round(price * profit, 0))
    else:
        price = round(float(row["price"]), 2)
        gain = round(price * profit, 2)
    return name, price, profit, gain


def copy_data_share(data):
    """Copie les données transformées des actions en mémoire cache."""
    data_share = \
        {"name": data[0], "price": data[1], "profit": data[2], "gain": data[3]}
    return data_share


def write_file_result(data_shares, price_gain_comb_of_best, name_def):
    """Écrit le résultat obtenu dans un fichier .txt."""
    if os_path.exists("./results") is False:
        os_mkdir("./results")
    path, euro = f"./results/{name_def}_result.txt", "\u20AC"

    kns, x = from_kns_or_not(name_def)

    with open(path, 'w', newline='', encoding="UTF-8") as file:
        file.write(write_headers(kns, name_def, euro))

        for idx_share in price_gain_comb_of_best[2]:
            if kns is True:
                price_gain_comb_of_best[0] += data_shares[idx_share]["price"]
            file.write(
                f"{data_shares[idx_share]['name']:<10}"
                f"{data_shares[idx_share]['price'] / x:>8.2f} {euro}"
                f"{data_shares[idx_share]['profit']:>8.4f}\n")

        file.write(f"\n{'Total price':<11}:"
                   f"{price_gain_comb_of_best[0] / x:>8.2f} {euro}"
                   f"\n{'Total gain':<11}:"
                   f"{price_gain_comb_of_best[1] / x:>8.2f} {euro}")
    file.close()


def from_kns_or_not(name_def):
    """
        Pour la transformation du format centime utilisé avec kns, en format
        euro,centime. EX : 49995 en 499,99.

    :param name_def: Pour identifier l'appel depuis knapsack.py.

    :return:
        bolééen et valeur de x pour la transformation.
    """
    if name_def == "bottom_up" or name_def == "top_down":
        return True, 100
    else:
        return False, 1


def write_headers(kns, name_def, euro):
    """Définit les deux premières lignes du fichier."""
    if kns is True:
        header_1 = f"Result of knapsack : {name_def.replace('_', '-')}\n\n:"
    else:
        header_1 = f"Result of {name_def}:\n\n"
    header_2 = f"{'name':^10}{'price':>8} {euro}{'profit':>8}\n\n"
    return header_1 + header_2


def description(calling_script):
    """Description des paramètres requis et optionnels pour le script."""
    second_requiered_parameter = ''
    option = ''
    if calling_script == "knapsack.py":
        second_requiered_parameter = f"\n{' '*4}Option:\n"\
                                     f"{' '*8}bu => for bottom-up\n"\
                                     f"{' '*8}td => for top-down"
        option = " bu"

    return print("\nRequiered parameter:\n"
                 "    Shares file (format csv)"
                 f"{second_requiered_parameter}"
                 "\nOptional parameter:\n"
                 "    Budget (format xx.yy)"
                 "\nExemple:\n"
                 f"    python {calling_script} shares.csv{option} 226.35")
