from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from data import Data
from hypothesis_tests import t_test

# Easton measure of air quality = CO * 6 + NO2 / 25 + O3 * 50 + SO2 / 2
EASTON_MEASURE = {'co': 6, 'no2': 1/25, 'o3': 50, 'so2': 1/2}

# Part 01: Load pollutant and weather data into a data structure
data = Data(Path(__file__).resolve().parent)
data.load()

# Part 02: Comparisons

# Problem 01: Compare ozone levels for January across each hour
o3_jan = data.o3[data.o3['datetime'].dt.month == 1]
o3_summary = o3_jan.groupby(
    o3_jan['datetime'].dt.hour)['o3'].agg(['mean', 'var', 'count'])

better = [0] * 24
worse = [0] * 24
significant_pairs = 0

for hour_a in range(24):
    for hour_b in range(hour_a + 1, 24):
        row_a = o3_summary.iloc[[hour_a]]
        row_b = o3_summary.iloc[[hour_b]]

        if t_test(row_a, row_b)[0]:
            significant_pairs += 1
            if row_a['mean'].iloc[0] < row_b['mean'].iloc[0]:
                better[hour_a] += 1
                worse[hour_b] += 1
            else:
                worse[hour_a] += 1
                better[hour_b] += 1

# Out of 276 (= 24 * 23 / 2)
print(f'Problem 1: {significant_pairs} of 276 hour pairs differ '
      'significantly\n')

# 188 pairs of possible 276 pairs differ significantly; ozone is worst
#   midday and afternoon, peaking 1 - 3 PM

hours = range(24)

plt.figure(figsize=(12, 5))
plt.bar(hours, better, color='g', label='Cleaner than (+1)')
plt.bar(hours, [-count for count in worse], color='r',
        label='Dirtier than (-1)')

plt.axhline(0, color='black', linewidth=0.8)
plt.xticks(hours)
plt.xlabel('Hour of the day')
plt.ylabel('Hours beaten (+) / hours lost to (-)')
plt.title('Jan Ozone: Comparison of AQ by hour')
plt.legend()
plt.show()

# Problem 02: Compare carbon monoxide levels between weekdays and weekends
# Prompt says Jan weekday vs Feb weekend; assumed typo and used January
co_jan = data.co[(data.co['datetime'].dt.month == 1)
                     & data.co['datetime'].dt.hour.between(7, 19)]

weekend_mask = co_jan['datetime'].dt.dayofweek >= 5
co_weekend = co_jan[weekend_mask]
co_weekday = co_jan[~weekend_mask]

weekday_summary = co_weekday.groupby(
    co_weekday['datetime'].dt.hour)['co'].agg(['mean', 'var', 'count'])
weekend_summary = co_weekend.groupby(
    co_weekend['datetime'].dt.hour)['co'].agg(['mean', 'var', 'count'])

rejected = pd.Series(
    t_test(weekday_summary, weekend_summary), index=weekday_summary.index)

print('Problem 2: Hours differing significantly:')
print(rejected)
print(f'{rejected.sum()} of 13 hours differ significantly\n')

# 3 of 13 hours (7, 8, 9) show a significant weekday/weekend difference in CO;
#   weekday carbon monoxide is higher

plt.plot(weekday_summary.index, weekday_summary['mean'], color='b',
         label='Weekday')
plt.plot(weekend_summary.index, weekend_summary['mean'], color='r',
         label='Weekend')

significant_hours = rejected[rejected].index
plt.axvspan(significant_hours.min(), significant_hours.max(),
            color='black', alpha=0.1, linewidth=0, 
            label='Significant difference')

plt.xticks(range(7, 20))
plt.xlabel('Hour of day')
plt.ylabel('Mean CO')
plt.title('Jan Carbon Monoxide: Weekday vs Weekend')
plt.legend()
plt.show()

# Problem 03: Compare Easton measure of air quality between 2018 and 2021
data.merge_sensors()
# Dropping incomplete readings, .copy() avoids SettingWithCopyWarning
complete_readings = data.merged.dropna(
    subset=['co', 'no2', 'o3', 'so2']).copy()

complete_readings['easton'] = 0.0
for pollutant, weight in EASTON_MEASURE.items():
    complete_readings['easton'] += complete_readings[pollutant] * weight

easton_dec = complete_readings[
    complete_readings['datetime'].dt.month == 12]

easton_2018 = easton_dec[easton_dec['datetime'].dt.year == 2018]
easton_2018_summary = easton_2018.groupby(
    easton_2018['datetime'].dt.day)['easton'].agg(['mean', 'var', 'count'])

easton_2021 = easton_dec[easton_dec['datetime'].dt.year == 2021]
easton_2021_summary = easton_2021.groupby(
    easton_2021['datetime'].dt.day)['easton'].agg(['mean', 'var', 'count'])

rejected_dates = pd.Series(
    t_test(easton_2018_summary, easton_2021_summary),
    index=easton_2018_summary.index)

print(f'Problem 3: {rejected_dates.sum()} of 31 days differ significantly')

# 22 out of 31 days have a statistically significant difference on the
#   Easton index between December 2018 and December 2021

plt.figure(figsize=(12, 5))
plt.vlines(easton_2021_summary.index, easton_2018_summary['mean'], 
            easton_2021_summary['mean'])
plt.scatter(easton_2018_summary.index, easton_2018_summary['mean'], color='b',
            label='2018', zorder=3)
plt.scatter(easton_2021_summary.index, easton_2021_summary['mean'], color='r',
            label='2021', zorder=3)
plt.xticks(range(1, 32)) # Starts at 1, ends at 31
plt.xlabel('Day in December')
plt.ylabel('Easton Measure of Pollution')
plt.title('Easton Measure: Dec 2018 vs Dec 2021')
plt.legend()
plt.show()
