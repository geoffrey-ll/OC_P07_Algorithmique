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

    :param path:
    :param max_line:
    :return:
    """
    data_shares = {}
    last_line = int()  # Pour l'analyse
    with open(path, newline='') as sharesfile:
        reader = csv_DictReader(sharesfile)
        for row in reader:
            if max_line == -1 or reader.line_num <= max_line:
                data = price, profit, gain = transform_data_share(row)
                if price <= 0 or profit <= 0 or gain <= 0:
                    continue
                data_shares[row["name"]] = copy_data_share(data)
                last_line = reader.line_num
            if reader.line_num == max_line:
                break
    sharesfile.close()
    return data_shares, last_line


def transform_data_share(row):
    price = round(float(row["price"]), 2)
    profit = round((float(row["profit"]) / 100), 4)
    gain = round(price * profit, 2)
    return price, profit, gain


def copy_data_share(data):
    data_share = {"price": data[0], "profit": data[1], "gain": data[2]}
    return data_share


def find_combinations_possible(data_shares):
    """

    :param data_shares:
    :return:
    """
    temp_best = {"gain": 0}
    for i in range(len(data_shares) + 1):
        temp = it_combinations(data_shares, i)
        for combination in temp:
            if len(combination) == 0:
                continue
            temp_best = affect_price_gain(data_shares, temp_best, combination)
    return temp_best


def affect_price_gain(data_shares, temp_best, combination):
    price_comb, gain_comb = 0, 0
    for name_share in combination:
        price_share = data_shares[name_share]["price"]
        gain_share = data_shares[name_share]["gain"]
        price_comb += price_share
        gain_comb += gain_share
    if price_comb <= BUDGET and gain_comb >= temp_best["gain"]:
        price_gain_comb = [price_comb, gain_comb, combination]
        temp_best = compare_combinations(temp_best, price_gain_comb)
    return temp_best


def compare_combinations(temp_best, price_gain_comb):
    if price_gain_comb[1] > temp_best["gain"]:
        return change_temp_comb(temp_best, price_gain_comb)
    else:
        if price_gain_comb[0] < temp_best["price"]:
            return change_temp_comb(temp_best, price_gain_comb)


def change_temp_comb(temp_best, price_gain_comb):
    temp_best["price"] = price_gain_comb[0]
    temp_best["gain"] = price_gain_comb[1]
    temp_best["combination"] = price_gain_comb[2]
    return temp_best


def write_file_result(data_shares, data_best):
    if os_path.exists("./results") is False:
        os_mkdir("./results")
    path, euro = "./results/bruteforce_result.txt", "\u20AC"
    with open(path, 'w', newline='', encoding="UTF-8") as file:

        file.write("Result of bruteforce:\n\n")
        file.write(f"{'name':^10}{'price':>8} {euro}{'profit':>8} %\n\n")

        for share in data_best["combination"]:
            file.write(
                f"{share:<10}"
                f"{data_shares[share]['price']:>8.2f} {euro}"
                f"{data_shares[share]['profit']:>8.4f} %\n")

        file.write(f"\n{'Total price':<11}: {data_best['price']:>8.2f} {euro}"
                   f"\n{'Total gain':<11}: {data_best['gain']:>8.2f} {euro}")
    file.close()


def description():
    return print("\nRequiered parameter:\n"
                 "    Shares file (format csv)"
                 "\nOptional parameter:\n"
                 "    Budget (format xx.yy)"
                 "\nExemple:\n"
                 "    python bruteforce.py actions.csv 226.35")


def main_bruteforce(path_file_shares, max_line=-1):
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
