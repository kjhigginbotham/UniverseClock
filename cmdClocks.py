"""
Created on Wed Nov 9 22:01:00 2017

@author: Kenny Higginbotham, Adam Kull
"""

import argparse
import time
import math

# take input for base time
parser = argparse.ArgumentParser()
parser.add_argument("input_date", help='Input date to start clocks from. Format example: Thu Nov 25 12:00:00 1915', type=str)
args = parser.parse_args()

# Find and print base and start time
base = args.input_date
start = time.asctime()

print("Base time: {}".format(base))
print("Starting time: {}".format(start))