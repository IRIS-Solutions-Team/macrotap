
#[

from __future__ import annotations

# Standard library imports
import json

# Third-party imports
import datapie as ap

#]


SERIES_KEY_DELIMITER = "."
DESCRIPTION_DELIMITER = " | "


def parse_response_json(response_json: dict, ) -> ap.Databox:

    observation_dims = response_json["structure"]["dimensions"]["observation"]
    series_key_dims = response_json["structure"]["dimensions"]["series"]
    series_data = response_json["dataSets"][0]["series"]

    if len(observation_dims) != 1 or observation_dims[0]["id"] != "TIME_PERIOD":
        raise ValueError("Unexpected observation dimensions structure")

    time_periods_info = observation_dims[0]["values"]
    time_periods_sdmx = tuple(i["id"] for i in time_periods_info)
    time_periods_sdmx = tuple(_clean_sdmx_string(i) for i in time_periods_sdmx)
    time_periods = {
        str(i): ap.Period.from_sdmx_string(j)
        for i, j in enumerate(time_periods_sdmx, )
    }

    def _extract_series_key_dim_value(dim:int, pointer:int) -> str:
        return series_key_dims[dim]["values"][pointer]["id"]

    def _extract_series_key_dim_info(dim:int, pointer:int) -> str:
        return series_key_dims[dim]["values"][pointer]["name"]

    def _series_key_from_pointer(pointers: tuple[int, ...], ) -> tuple[str, str]:
        r"""
        """
        series_key_parts = tuple(
            _extract_series_key_dim_value(i, p, )
            for i, p, in enumerate(pointers)
        )
        return SERIES_KEY_DELIMITER.join(series_key_parts, )

    def _description_from_pointer(pointers: tuple[int, ...], ) -> str:
        description_parts = tuple(
            _extract_series_key_dim_info(i, p, )
            for i, p, in enumerate(pointers)
        )
        return DESCRIPTION_DELIMITER.join(description_parts, )

    output_db = ap.Databox()

    for series_key, series_record, in series_data.items():
        pointers = _pointers_from_numeric_series_key(series_key, )
        series_key = _series_key_from_pointer(pointers, )
        description = _description_from_pointer(pointers, )
        #
        series_periods = tuple(
            time_periods[i]
            for i in series_record["observations"].keys()
        )
        #
        series_values = tuple(
            float(i[0]) if i[0] is not None else None
            for i in series_record["observations"].values()
        )
        #
        time_series = ap.Series(
            periods=series_periods,
            values=series_values,
            description=description,
        )
        output_db[series_key] = time_series

    return output_db


def _clean_sdmx_string(s: str, ) -> str:
    r"""
    Dates in response do not conform to ISO 8601 due to use of "-M" for months
    """
    s = s.replace("-M", "-")
    return s


def _pointers_from_numeric_series_key(numeric_series_key: str) -> tuple[str, str]:
    r"""
    Convert '0:1:2' to (0, 1, 2, ) where each number is an int pointer to
    the dimension value in the series key dimension structure
    """
    return tuple(
        int(i)
        for i in numeric_series_key.split(":")
    )

