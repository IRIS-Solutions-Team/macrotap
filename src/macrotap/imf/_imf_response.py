
#[

from __future__ import annotations

# Standard library imports
import io
import csv

# Typing imports
from typing import Iterable, Callable

# Third-party imports
import datapie as ap

# Local imports
from ._imf_requests import DIM_SEPARATOR

#]


def parse_response_csv(response_csv: str, ) -> ap.Databox:

    stream = io.StringIO(response_csv, )
    reader = csv.reader(stream, )

    header = next(reader, )
    db_key_extractor = _build_db_key_extractor(header, )
    time_period_extractor = _build_time_period_extractor(header, )
    value_extractor = _build_value_extractor(header, )

    intermediate_db = {}
    for row in reader:
        db_key = db_key_extractor(row, )
        if db_key not in intermediate_db:
            intermediate_db[db_key] = []
        time_period = time_period_extractor(row, )
        value = value_extractor(row, )
        if time_period is not None and value is not None:
            intermediate_db[db_key].append((time_period, value, ), )

    output_db = ap.Databox()

    for db_key, observations, in intermediate_db.items():
        output_db[db_key] = _create_series_from_observations(observations, )

    return output_db


def _build_db_key_extractor(
    header: Iterable[str],
) -> Callable:
    r"""
    """
    #[
    action_index = header.index("ACTION", )
    time_period_index = header.index("TIME_PERIOD", )
    #
    def db_key_extractor(row: Iterable[str], ) -> str:
        return DIM_SEPARATOR.join(row[action_index+1:time_period_index], )
    #
    return db_key_extractor
    #]


_FREQUENCY_MAP = {
    "A": ap.Frequency.YEARLY,
    "Q": ap.Frequency.QUARTERLY,
    "M": ap.Frequency.MONTHLY,
    "D": ap.Frequency.DAILY,
}


def _build_time_period_extractor(
    header: Iterable[str],
) -> Callable:
    r"""
    """
    #[
    time_period_index = header.index("TIME_PERIOD", )
    frequency_index = header.index("FREQUENCY", )
    #
    def time_period_extractor(row: Iterable[str], ) -> str:
        time_period_string = _clean_sdmx_date_string(row[time_period_index].strip(), )
        if not time_period_string:
            return None
        frequency_letter = row[frequency_index].strip()
        frequency = _FREQUENCY_MAP[frequency_letter]
        return ap.Period.from_sdmx_string(
            time_period_string,
            frequency=frequency,
        )
    #
    return time_period_extractor
    #]


_MISSING_VALUE = ("", "NA", )


def _build_value_extractor(
    header: Iterable[str],
) -> Callable:
    r"""
    """
    #[
    value_index = header.index("OBS_VALUE", )
    #
    def value_extractor(row: Iterable[str], ) -> float | None:
        value_string = row[value_index].strip()
        return (
            float(value_string, )
            if value_string not in ("", "NA", )
            else None
        )
    #
    return value_extractor
    #]


def _clean_sdmx_date_string(s: str, ) -> str:
    r"""
    Dates in response do not conform to ISO 8601 due to use of "-M" for months
    """
    s = s.replace("-M", "-")
    return s


def _get_frequency_from_letter(frequency_letter: str, ) -> str:
    r"""
    """
    return _FREQUENCY_MAP[frequency_letter, ]


def _create_series_from_observations(observations: Iterable[tuple], ) -> ap.Series:
    if not observations:
        return ap.Series()
    time_periods, obs_values = zip(*observations, )
    return ap.Series(
        periods=time_periods,
        values=obs_values,
    )

