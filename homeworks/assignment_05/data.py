from pathlib import Path
from typing import Literal, get_args

import pandas as pd

# Files renamed to match pollutant keys (e.g. COthreelocations.csv -> co.csv)
# NO2/ozone/SO2threelocations.csv -> no2/o3/so2.csv; weather.csv unchanged

Pollutant = Literal['co', 'no2', 'o3', 'so2']
_SENSOR_NAMES = get_args(Pollutant)

_HEADERLESS = {'co'}

_SENSOR_FIELDS = (
    'date_county_raw', 'latitude', 'longitude', 'parameter',
    'date_local', 'time_local', 'value', 'units', 'units_2',
    'null',
)

_RELEVANT_FIELDS = (
    'latitude', 'longitude', 'parameter', 'date_local',
    'time_local', 'value', 'units',
)

_WEATHER_FIELDS = (
    'index', 'datetime', 'temperature', 'dew_point',
    'relative_humidity', 'wind_speed', 'pressure',
)

_RELEVANT_WEATHER_FIELDS = (
    'datetime', 'temperature', 'dew_point', 'relative_humidity',
    'wind_speed', 'pressure',
)

_MERGE_KEYS = ['datetime', 'latitude', 'longitude']


class Data:
    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.co: pd.DataFrame | None = None
        self.no2: pd.DataFrame | None = None
        self.o3: pd.DataFrame | None = None
        self.so2: pd.DataFrame | None = None
        self.weather: pd.DataFrame | None = None
        self.merged: pd.DataFrame | None = None

    def load_sensor(self, dataset: Pollutant) -> None:
        # Unlike other files, co.csv has no header
        header = None if dataset in _HEADERLESS else 0
        df = pd.read_csv(
            self.directory / f'{dataset}.csv', header=header,
            names=_SENSOR_FIELDS, usecols=_RELEVANT_FIELDS)
        df.rename(columns={'value': dataset}, inplace=True)
        self._build_datetime(df)
        setattr(self, dataset, df)

    def load_weather(self) -> None:
        self.weather = pd.read_csv(
            self.directory / 'weather.csv', header=0,
            parse_dates=['datetime'], names=_WEATHER_FIELDS,
            usecols=_RELEVANT_WEATHER_FIELDS)

    def load(self) -> None:
        for pollutant in _SENSOR_NAMES:
            self.load_sensor(pollutant)
        self.load_weather()

    def merge_sensors(self) -> None:
        self.merged = self._average_duplicates(_SENSOR_NAMES[0])
        for pollutant in _SENSOR_NAMES[1:]:
            self.merged = self.merged.merge(
                self._average_duplicates(pollutant),
                on=_MERGE_KEYS, how='outer', validate='1:1')

    @staticmethod
    def _build_datetime(df: pd.DataFrame) -> None:
        # Rows are keyed by datetime (year/month/day/hour) and sensor location
        df['datetime'] = pd.to_datetime(
            df['date_local'] + ' ' + df['time_local'],
            format='%m/%d/%Y %H:%M')
        df.drop(columns=['date_local', 'time_local'], inplace=True)

    def _average_duplicates(
            self, pollutant: Pollutant) -> pd.DataFrame:
        # Datasets not one-to-one, duplicates are averaged
        return getattr(self, pollutant).groupby(
            _MERGE_KEYS, as_index=False)[pollutant].mean()
