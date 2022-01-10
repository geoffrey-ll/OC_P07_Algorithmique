#! /usr/bin/env python3
# coding: utf-8


from sys import argv as sys_argv

from analyzer.analyzer import main_analyzer


user_args = sys_argv


main_analyzer(user_args[1], "bruteforce")
