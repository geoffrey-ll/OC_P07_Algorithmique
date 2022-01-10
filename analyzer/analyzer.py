#! /usr/bin/env python3
# coding: utf-8


from time import time as t_time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from bruteforce import main_bruteforce
from optimized import main_optimized


from pprint import pprint as pprint


def perf_of_file(path_file_actions, max_line, who):
    time_start = t_time()
    if who == "bruteforce":
        line_num, for_complexity_memory = \
            main_bruteforce(path_file_actions, max_line)
    if who == "optimized":
        line_num, for_complexity_memory = \
            main_optimized(path_file_actions, max_line)
    time_end = t_time()
    runtime = time_end - time_start
    if runtime == float(0):
        return perf_of_file(path_file_actions, max_line, who)

    print(runtime)
    return runtime, line_num, for_complexity_memory


def main_analyzer(path_file_actions, who):
    number_actions, runtimes = [], []
    max_line = -1
    while max_line >= 2 or max_line == -1:
        runtime, line_num, for_complexity_memory = \
            perf_of_file(path_file_actions, max_line, who)
        runtimes.append(runtime)
        max_line = line_num - 1
        number_actions.append(max_line)

        complexity_memory = float()
        for variable in for_complexity_memory:
            complexity_memory += variable.__sizeof__()
        print(complexity_memory)
    graph(list(reversed(number_actions)), list(reversed(runtimes)), who)

def graph(number_actions, runtime, who):

    sns.set_style("darkgrid", {"axes.facecolor": "#282722", "grid.color": "gray", "edgecolor": "blue"})
    # ax1 = sns.lineplot(x=number_actions, y=runtime, color=color_runtime, ci=None)
    # ax2 = ax1.twinx()
    # sns.lineplot(x=number_actions, y=size, color=color2, ci=None, ax=ax2)
    # ax2.grid(False)

    # plt.show()

    fig, ax1 = plt.subplots(facecolor="#272822", edgecolor="blue")
    color_gen = "#66d9ef"
    color_runtime = "red"
    color_ref = "yellow"
    ax1.set_title(f"Complexité de {who}.py", color=color_gen)

    # Abscisse
    ax1.set_xlabel("Nombres d'actions", color=color_gen)
    end_abscissa = len(number_actions) + 1
    step_abscissa = int(len(number_actions) / 10)
    # step_abscissa = 1
    plt.xticks(range(0, end_abscissa, step_abscissa))  # Pour déterminer les valeurs en abscisse
    ax1.tick_params(axis='x', labelcolor=color_gen)

    # Ordonnée
    line1 = ax1.scatter(number_actions, runtime, marker="x", label="Durée", color=color_runtime)
    plt.annotate(f"{runtime[-1]:.2f}", color=color_runtime,
                 xy=(number_actions[-1], runtime[-1]), xycoords="data",
                 xytext=(50, -20), textcoords="offset pixels")
    ax1.set_ylabel("Durée du script (s)", color=color_gen)
    ax1.tick_params(axis='y', labelcolor=color_gen)



    if who == "bruteforce":
        y3 = []
        for i in number_actions:
            y3.append(2 ** i)

        ax3 =ax1.twinx()
        line3 = ax3.plot(number_actions, y3, label="O(2^n)", color=color_ref)
        ax3.axis(False)
        ax3.grid(False)

    if who == "optimized":
        y3 = []
        for i in number_actions:
            y3.append(i)

        ax3 =ax1.twinx()
        color_ref = "yellow"
        line3 = ax3.plot(number_actions, y3, label="O(2^n)", color=color_ref)
        ax3.axis(False)
        ax3.grid(False)


    # lines = [line1, line2, line3]
    # labels = [l.get_label() for l in lines]
    # ax1.legend(lines, labels, loc=2)

    plt.show()





#_______________________________________________


    # fig, ax = plt.subplots(1, 1, sharex=True)
    # ax.plot(x, y)
    # ax.plot(x, z)
    # plt.show()


    # plt.figure()
    #     # figsize=(inch, inch) -> taille de la figure en inch
    # plt.plot(x, y)  # courbe
    # plt.plot(x, z)
    #     # lw -> épaisseur du trait
    #     # c -> couleur du trait
    #     # ls -> type de trait
    #     # label='' -> sert pour texte pour la légende
    # # plt.xlabel('texte')
    # # plt.ylabel('text')
    # # plt.title('texte')
    # # plt.legend() -> affiche la légende
    # # plt.savefig('name.png') -> enregistrer la figure
    # # plt.scatter(x, y)  # Nuage de points
    #
    # # plt.subplot(int1, int2, int3) -> pour avoir plusieurs graph dans une figure
    #     # int1=lignes int2=colonnes int3=position
    #
    #
    # plt.show()