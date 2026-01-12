"""
"""


#[

from __future__ import annotations

# Typing imports
from typing import Iterable, Any

# Third-party imports
import requests as _rq
import datapie as _ap

#]


_FRED_FREQ_MAP = {
    "A".casefold(): _ap.Frequency.YEARLY,
    "Q".casefold(): _ap.Frequency.QUARTERLY,
    "M".casefold(): _ap.Frequency.MONTHLY,
    "D".casefold(): _ap.Frequency.DAILY,
}


_BASE_URL = r"https://api.stlouisfed.org/fred/series"
_OBSERVATIONS_URL = _BASE_URL + r"/observations"
_API_KEY = r"951f01181da86ccb9045ce8716f82f43"
_PARAMETERS = r"?series_id={series_id}&api_key={api_key}&file_type=json"
_MISSING_VALUE = r"."


def from_fred(
    request_strings: str | Iterable[str],
    target_db: _ap.Databox | None = None,
    return_info: bool = False,
) -> _ap.Databox:
    r"""
................................................................................

==Download time series from FRED (St Louis Fed Database)==

This method downloads time series data from the FRED database. The data is
downloaded using the FRED API. The method requires an API key, which is provided
by the FRED website. The API key is stored in the `_API_KEY` variable in the
`_fred.py` module. The method downloads the data for the specified series IDs
and returns a `Databox` object with the downloaded series.

db = Databox.from_fred(
    request_strings,
)


### Input arguments ###

???+ input "request_strings"
    A list or dictionary of series IDs to download from FRED. If a dictionary is
    provided, the keys are used as the FRED codes and the values are used for
    the names of the time series in the Databox. If list of strings is provided,
    the series IDs are used as the names of the series in the `Databox` object.


### Returns ###

???+ returns "db"
    A `Databox` object containing the downloaded time series data.

................................................................................
    """
    #[
    if isinstance(request_strings, str):
        request_strings = (request_strings, )
    #
    if target_db is None:
        target_db = _ap.Databox()
    info = []
    for i in request_strings:
        target_db[i], current_info, = _get_series(i, )
        if return_info:
            info.append(current_info)
    #
    if return_info:
        return target_db, info,
    #
    return target_db
    #]


def _request_from_series_ids(series_ids: Iterable[str], ):
    """
    """
    #[
    return {
        series_id.strip(): series_id.strip()
        for series_id in series_ids
    }
    #]


def _get_series(series_id: str, ) -> tuple[_ap.Series, dict[str, Any]]:
    """
    """
    #[
    urls = _get_series_urls(series_id, )
    meta_response = _rq.get(urls["meta_url"], ).json()
    data_response = _rq.get(urls["data_url"], ).json()
    #
    if "seriess" not in meta_response or "observations" not in data_response:
        raise ValueError(f"Invalid response from FRED API for {series_id}", )
    #
    freq = _get_freq_from_meta_response(meta_response, )
    iso_dates, str_values = _get_dates_and_values_from_data_response(data_response, )
    values = tuple( (float(x) if x != _MISSING_VALUE else None) for x in str_values )
    dates = _ap.periods_from_iso_strings(iso_dates, frequency=freq, )
    info = {
        "meta_url": urls["meta_url"],
        "data_url": urls["data_url"],
        "meta_response": meta_response,
        "data_response": data_response,
    }
    return _ap.Series(periods=dates, values=values, ), info,
    #]


def _get_freq_from_meta_response(meta_response: dict, ):
    """
    """
    #[
    freq_letter = meta_response["seriess"][0]["frequency_short"].casefold()
    return _FRED_FREQ_MAP[freq_letter]
    #]


def _get_dates_and_values_from_data_response(data_response: dict, ):
    """
    """
    #[
    date_value_pairs = (
        (obs["date"], obs["value"], )
        for obs in data_response["observations"]
    )
    return zip(*date_value_pairs, )
    #]


def _get_series_urls(series_id: str, ):
    """
    """
    #[
    parameters = _PARAMETERS.format(series_id=series_id, api_key=_API_KEY, )
    meta_url = _BASE_URL + parameters
    data_url = _OBSERVATIONS_URL + parameters
    return {"meta_url": meta_url, "data_url": data_url, }
    #]

