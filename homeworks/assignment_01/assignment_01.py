"""
Assignment 01

Problem 01: Writes the numbers 0-2000 to problem_01.txt, once using a for
loop and once using a while loop, printing each value as it's written.

Problem 02: Reads data.txt and finds the second largest and second
smallest values using a single pass over the file (no sorting, no
storing all values in an array).

Problem 03: Reads data.txt and reports the count and average of the
positive and negative values.
"""

from pathlib import Path
import operator


# Problem 01

PROBLEM_01_PATH = Path(__file__).resolve().parent / 'problem_01.txt'
UPPER_LIMIT = 2000  # Defined by the assignment

# Using the for loop

for_loop_array = range(0,UPPER_LIMIT + 1)

print('*' * 20, 'PROBLEM 01', '*' * 20)
print('Using the for loop:')
for i in for_loop_array: print(i)

with open(PROBLEM_01_PATH, 'w') as f:
    f.writelines(f'{item}\n' for item in for_loop_array)

# Using the while loop

iteration = 0

print('Using the while loop:')
with open(PROBLEM_01_PATH, 'a') as f:
    while (UPPER_LIMIT + 1) > iteration:
        print(iteration)
        f.write(f'{iteration}\n')
        iteration += 1

print('*' * 52, '\n')


# Problem 02

PROBLEM_02_PATH = Path(__file__).resolve().parent / 'data.txt'

# One comparison function rather than two blocks of code with similar logic; uses operator module to evaluate
def _second_x(f, op):
    first_place = float(f.readline().split()[0])  # Initializes the largest/smallest value as the first line
    second_place = first_place
    for line in f:
        if op(float(line.split()[0]), first_place):
            second_place = first_place
            first_place = float(line.split()[0])
        elif op(float(line.split()[0]), second_place):
            second_place = float(line.split()[0])
    return second_place

with open(PROBLEM_02_PATH, 'r') as f:
    print('*' * 20, 'PROBLEM 02', '*' * 20)
    print(f'The second largest number was {_second_x(f, operator.gt)}')

with open(PROBLEM_02_PATH, 'r') as f:  # Opens the file a second time so that the index resets back to the first line
    print(f'The second smallest number was {_second_x(f, operator.lt)}')
    print('*' * 52, '\n')


# Problem 03

count_pos = 0
count_neg = 0
sum_pos = 0
sum_neg = 0

with open(PROBLEM_02_PATH, 'r') as f:
    for line in f:
        value = float(line.split()[0])
        if value >= 0:
            count_pos += 1
            sum_pos += value
        else:
            count_neg += 1
            sum_neg += value

print('*' * 20, 'PROBLEM 03', '*' * 20)
print(f'There are {count_pos} positive numbers present averaging {sum_pos/count_pos}')
print(f'There are {count_neg} negative numbers present averaging {sum_neg/count_neg}')
print('*' * 52, '\n')

    