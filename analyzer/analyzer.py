#! /usr/bin/env python3
# coding: utf-8


from os import path as os_path, mkdir as os_mkdir
from time import time as t_time
import matplotlib.pyplot as plt
import seaborn as sns


from bruteforce import main_bruteforce
from optimized import main_optimized
from knapsack import main_knapsack


complexity_memory = 0


def performance(path_file_shares, max_line, who, option="none"):
    time_start = t_time()
    if who == "bruteforce":
        line_num, for_complexity_memory = \
            main_bruteforce(path_file_shares, max_line)
    if who == "optimized":
        line_num, for_complexity_memory = \
            main_optimized(path_file_shares, max_line)
    if who == "knapsack":
        line_num, for_complexity_memory = \
            main_knapsack(path_file_shares, option, max_line)
    time_end = t_time()
    runtime = time_end - time_start

    if runtime == float(0):
        return performance(path_file_shares, max_line, who)

    return runtime, line_num, for_complexity_memory


def calculate_spatial_complexity(variable_to_analyze):
    global complexity_memory
    for elmt in variable_to_analyze:
        try:
            if isinstance(elmt, int) is True \
                    or isinstance(elmt, float) is True \
                    or isinstance(elmt, str) is True:
                complexity_memory += elmt.__sizeof__()

            if isinstance(elmt, list) is True:
                calculate_spatial_complexity(elmt)

            if isinstance(elmt, dict) is True:
                for key, value in elmt.items():
                    complexity_memory += key.__sizeof__()
                    if isinstance(value, list) is True \
                            or isinstance(value, dict) is True \
                            or isinstance(value, tuple) is True:
                        calculate_spatial_complexity(elmt)
                    else:
                        complexity_memory += value.__sizeof__()
        except TypeError:
            complexity_memory += elmt.__sizeof__()
            print(f"ERROR : {elmt}\n"
                  f"{type(elmt)}")
            print(f"transitional error : {complexity_memory}")
            input()


def graph(number_shares, runtimes, who):
    sns.set_style("darkgrid",
                  {"axes.facecolor": "#282722",
                   "grid.color": "gray",
                   "edgecolor": "blue"}
                  )

    fig, ax1 = plt.subplots(facecolor="#272822", edgecolor="blue")
    color_gen = "#66d9ef"
    color_runtime = "red"
    color_ref = "yellow"
    ax1.set_title(f"Complexité de {who}.py", color=color_gen)

    # Abscisse
    ax1.set_xlabel("Nombres d'shares", color=color_gen)
    # Pour déterminer les valeurs en abscisse
    if who == "knapsack":
        end_abscissa = number_shares[-1] + 1
        step_abscissa = max(int(end_abscissa / 10), 1)
    else:
        end_abscissa = len(number_shares) + 1
        step_abscissa = max(int(len(number_shares) / 10), 1)
    plt.xticks(range(0, end_abscissa, step_abscissa))
    ax1.tick_params(axis='x', labelcolor=color_gen)

    # Ordonnée
    ax1.scatter(number_shares, runtimes,
                marker="x", label="Durée", color=color_runtime)
    plt.annotate(f"{runtimes[-1]:.2f}", color=color_runtime,
                 xy=(number_shares[-1], runtimes[-1]), xycoords="data",
                 xytext=(50, -20), textcoords="offset pixels")
    ax1.set_ylabel("Durée du script (s)", color=color_gen)
    ax1.tick_params(axis='y', labelcolor=color_gen)

    if who == "bruteforce":
        y3 = []
        for i in number_shares:
            y3.append(2 ** i)

        ax3 = ax1.twinx()
        ax3.plot(number_shares, y3, label="O(2^n)", color=color_ref)
        ax3.axis(False)
        ax3.grid(False)

    if who == "knapsack":
        y3 = []
        for i in number_shares:
            y3.append(i)

        ax3 = ax1.twinx()
        ax3.plot(number_shares, y3, label="O(n)", color=color_ref)
        ax3.axis(False)
        ax3.grid(False)

    plt.show()


def data_optimized(number_shares, runtimes):
    if os_path.exists("./analyzer") is False:
        os_mkdir("./analyzer")
    path = "./analyzer/data_for_opti_graph_log.txt"

    with open(path, 'w', newline='', encoding="UTF-8") as file:
        file.write("Données pour le graphique de complexité temporelle\n"
                   f"{'de optimized.py':^50}\n"
                   f"{'(en échelle logarithmique)':^50}\n\n")

        file.write(f"{'runtimes':^21}\n\n")
        for i in range(len(runtimes) - 1):
            file.write(f"{number_shares[i]:0>3};"
                       f"0,{str(runtimes[i])[2:]:0<19}\n")
    file.close()


def main_analyzer(path_file_shares, who, option="none"):
    number_shares, runtimes, size = [], [], 0
    max_line, step_kns, count_iteration_kns = -1, 0, 1

    while max_line >= 2 or max_line == -1:
        runtime, line_num, vars_to_analyze = \
            performance(path_file_shares, max_line, who, option)

        if max_line == -1:
            calculate_spatial_complexity(vars_to_analyze)
            size = complexity_memory

        if who == "knapsack":
            if max_line == -1:
                step_kns = int((line_num - 1) / 19)
            if count_iteration_kns == 1:
                max_line = line_num - 1
            elif count_iteration_kns == 20:
                max_line = 2
            else:
                max_line = line_num - step_kns
            count_iteration_kns += 1

        else:
            max_line = line_num - 1

        if max_line >= 2:
            runtimes.append(runtime)
            number_shares.append(max_line)

    number_shares_reverse = list(reversed(number_shares))
    runtimes_reverse = list(reversed(runtimes))

    if who == "optimized":
        data_optimized(number_shares_reverse, runtimes_reverse)
    else:
        graph(number_shares_reverse, runtimes_reverse, who)

    print(f"\nSpatial complexity for entire file: {size:,} octet")
