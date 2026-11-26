
#[

from __future__ import annotations

# Standard library imports
import io
import csv

# Typing imports
from typing import Iterable, Callable, Literal

# Third-party imports
import datapie as _da

# Application imports
from . import _adaptations as _ad

#]


_MISSING_VALUE_STRINGS = ("", "NA", )

_KEY_HEADER = "KEY"
_FREQUENCY_HEADER = "FREQUENCY"
_TIME_PERIOD_HEADER = "TIME_PERIOD"

OutputFormat = Literal["series", "values", "observations"]

def _build_key_extractor(
    header: Iterable[str],
) -> Callable:
    r"""
    """
    #[
    key_index = header.index(_KEY_HEADER, )
    #
    def db_key_extractor(row: Iterable[str], ) -> str:
        return row[key_index].strip()
    #
    return db_key_extractor
    #]


def _build_frequency_extractor(
    header: Iterable[str],
) -> Callable:
    r"""
    """
    #[
    frequency_index = header.index(_FREQUENCY_HEADER, )
    #
    def frequency_extractor(row: Iterable[str], ) -> str:
        return row[frequency_index].strip()
    #
    return frequency_extractor
    #]


def _build_time_period_extractor(
    header: Iterable[str],
) -> Callable:
    r"""
    """
    #[
    time_period_index = header.index(_TIME_PERIOD_HEADER, )
    #
    def time_period_extractor(row: Iterable[str], ) -> str:
        time_period_string = row[time_period_index].strip()
        return _ad.clean_sdmx_period_string(time_period_string, )
    #
    return time_period_extractor
    #]


def _build_value_extractor(
    header: Iterable[str],
) -> Callable:
    r"""
    """
    #[
    value_index = header.index("OBS_VALUE", )
    #
    def value_extractor(row: Iterable[str], ) -> float | None:
        return row[value_index].strip()
    #
    return value_extractor
    #]


def parse_response(
    csv_response: str,
    build_key_extractor: Callable = _build_key_extractor,
    build_frequency_extractor: Callable = _build_frequency_extractor,
    build_time_period_extractor: Callable = _build_time_period_extractor,
    build_value_extractor: Callable = _build_value_extractor,
    output_format: OutputFormat = "series",
) -> _da.Databox:

    stream = io.StringIO(csv_response, )
    reader = csv.reader(stream, )

    header = next(reader, )
    db_key_extractor = build_key_extractor(header, )
    frequency_extractor = build_frequency_extractor(header, )
    time_period_extractor = build_time_period_extractor(header, )
    value_extractor = build_value_extractor(header, )

    intermediate_db = {}
    for row in reader:
        db_key = db_key_extractor(row, )
        if db_key not in intermediate_db:
            intermediate_db[db_key] = []
        frequency_letter = frequency_extractor(row, )
        time_period_string = time_period_extractor(row, )
        value_string = value_extractor(row, )
        #
        if not _is_valid_period(time_period_string, frequency_letter, ):
            continue
        #
        time_period = _da.Period.from_sdmx_string(
            time_period_string,
            frequency=_ad.FREQUENCY_MAP[frequency_letter.casefold()],
        )
        value = (
            float(value_string, )
            if not _is_missing_value(value_string, ) else None
        )
        intermediate_db[db_key].append((time_period, value, ), )

    output_db = _da.Databox()

    create_final_output = _FINAL_OUTPUT_MAP[output_format]

    for db_key, observations, in intermediate_db.items():
        output_db[db_key] = create_final_output(observations, )

    return output_db


def _is_valid_period(
    time_period_string: str,
    frequency_letter: str,
) -> bool:
    if time_period_string == "":
        return False
    if frequency_letter.casefold() not in _ad.FREQUENCY_MAP:
        return False
    return True


def _is_missing_value(
    value_string: str,
) -> bool:
    return value_string in _MISSING_VALUE_STRINGS


def _create_series_from_observations(
    observations: list[tuple[_da.Period, float | None]],
) -> _da.Series:
    r"""
    """
    if not observations:
        return _da.Series.void()
    periods, values, = zip(*observations, )
    return _da.Series(
        periods=periods,
        values=values,
    )


def _create_values_from_observations(
    observations: list[tuple[_da.Period, float | None]],
) -> list[float | None]:
    r"""
    """
    if not observations:
        return ()
    _, values, = zip(*observations, )
    return values


def _create_observations_from_observations(
    observations: list[tuple[_da.Period, float | None]],
) -> list[tuple[_da.Period, float | None]]:
    r"""
    """
    return observations


_FINAL_OUTPUT_MAP = {
    "series": _create_series_from_observations,
    "values": _create_values_from_observations,
    "observations": _create_observations_from_observations,
}

