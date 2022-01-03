from csv import DictReader as csvDictReader
from csv import DictWriter as csvDictWriter

from pprint import pprint as pp


what_file = "dataset1_Python+P7.csv"
# what_file = "dataset2_Python+P7.csv"

data_actions = {}


def read_actions_file():
    with open(what_file, newline='') as actionsfile:
        reader = csvDictReader(actionsfile)
        for row in reader:
            data_actions[row["name"]] = {"price": row["price"],
                                           "profit": row["profit"]}


def main():
    read_actions_file()
    pp(data_actions)
    print("len : ", len(data_actions))


main()
