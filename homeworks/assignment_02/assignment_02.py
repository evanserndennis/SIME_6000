'''
Assignment 02: DJIA Analysis

1. Plot the DJIA for 2018.
2. Plot the DJIA for Fridays only.
3. Plot the Friday increase/decrease and the Wednesday increase/decrease on the same graph.
   May need to truncate one or two data points to align series.
4. Calculate the average Friday increase/decrease and the average Wednesday increase/decrease.
   Add a comment with both averages and which day is better for investors.
'''

from pathlib import Path
from datetime import datetime
from decimal import Decimal
import matplotlib.pyplot as plt
from statistics import mean


DATA_PATH = Path(__file__).resolve().parent / 'DJIA2018dayofweek.txt'

with open(DATA_PATH, 'r') as f:

    records_raw = f.readlines()
    records_clean = []

    for record in records_raw:
        records_clean.append(record.split())

    date = []
    value = []

    for record in records_clean:
        date.append(datetime.strptime(record[0], '%m/%d/%Y'))  # Converting to a datetime allows us to bypass using the day strings for filtering
        value.append(Decimal(record[2]))  # Will convert back to a float once handing back to matplotlib; floats make be nervous

plt.xlabel('Date')
plt.ylabel('Close')

# Problem 01: Plot all the 2018 DJIA data from the file
plt.title('2018 DJIA Close by Date')
plt.plot(date, [float(v) for v in value])
plt.show()

# Problem 02: Plot the 2018 DJIA data from Fridays only
dates_friday, values_friday = zip(*[(dt, v) for dt, v in zip(date, value) if dt.weekday() == 4])  # Goes through the date and value arrays and searches for Fridays, zips and spits back out friday-only data
plt.title('2018 DJIA Weekly Close')
plt.plot(dates_friday, [float(v) for v in values_friday])
plt.show()

# Problem 03: Plot increase/decrease for Friday and Wednesday on the same graph
delta = []

for i in range(1, len(value)):  # Starts at the second day, avoids value[0] - value[-1] bug, first day is Tuesday anyway
    delta.append(value[i] - value[i - 1])

deltas_friday = [dl for dt, dl in zip(date[1:], delta) if dt.weekday() == 4]
dates_wednesday, deltas_wednesday = zip(*[(dt, dl) for dt, dl in zip(date[1:], delta) if dt.weekday() == 2])

plt.title('2018 Mid-week/End of Week Daily Changes')
plt.ylabel('Increase (Decrease) from Prior Day')
plt.bar(dates_wednesday, [float(v) for v in deltas_wednesday], label='Wed')
plt.bar(dates_friday, [float(v) for v in deltas_friday], label='Fri')
plt.legend()
plt.show()

# Problem 04: Calculate average delta by day of the week
means = {'Wednesday': mean(deltas_wednesday), 'Friday': mean(deltas_friday)}

higher_value = ['', 0]
for key, value in means.items():
    if value > higher_value[1]:
        higher_value = [key, value]

lower_value = ['', 0]
for key, value in means.items():
    if key != higher_value[0]:
        lower_value = [key, value]

print('*' * 90 + '\n' +
    f'Wednesday sees an average change of {round(means["Wednesday"], 2)} dollars from prior day close\n' +
    f'Friday sees an average change of {round(means["Friday"], 2)} dollars from prior day close\n' +
    'Regarding which day is "better" for investors is entirely dependent on the context\n' +
    'If an investor is purchasing, they may prefer the date with the highest average decrease:\n' +
    f'  in this case, {lower_value[0]} is more preferrable with a delta of {round(lower_value[1], 2)} dollars\n' +
    'If an investor is selling, they may prefer the date with the highest average increase:\n' +
    f'  in this case, {higher_value[0]} is more preferrable with a delta of {round(higher_value[1], 2)} dollars\n'
    )

# Friday has a delta of -17.87 dollars, Wednesday has a delta of +15.08 dollars
# Friday is a better day for investors to purchase on average while Wednesday is a better day to sell on average

