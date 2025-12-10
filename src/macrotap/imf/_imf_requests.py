
#[

from __future__ import annotations

# Typing imports
from typing import Any, Callable

# Standard library imports
import itertools as _it
import dataclasses as _dc
import time as _ti

# Typing imports
from collections.abc import Iterable

#]


DATA_FLOW_SEPARATOR = "/"

DIM_SEPARATOR = "."

URL_TEMPLATE = (
    r"https://api.imf.org/external/sdmx/2.1/data/"
    r"{data_flow}"
    r"{data_flow_separator}"
    r"{series_key}"
    r"?TIME_PERIOD&dataonly"
)


def build_request_urls(
    request_strings: Iterable[str],
    **kwargs,
) -> tuple[str, ...]:
    r"""
    """
    requests = _get_requests_from_strings(request_strings, )
    return tuple(
        i.url
        for i in requests
    )


def build_grouped_request_urls(
    request_strings: Iterable[str],
    group_by: Callable | None = None,
) -> tuple[str, ...]:
    r"""
    """
    requests = _get_requests_from_strings(request_strings, )
    grouped_requests = _group_requests(
        requests,
        group_by=group_by,
    )
    return tuple(
        _build_url_for_grouped_requests(i)
        for i in grouped_requests
    )


def _get_requests_from_strings(
    request_strings: str | Iterable[str], 
) -> tuple[_Request, ...]:
    r"""
    """
    #[
    if isinstance(request_strings, str):
        request_strings = (request_strings, )
    requests = tuple(
        _Request.from_request_string(n, )
        for n in request_strings
    )
    return requests
    #]


def _group_requests(
    requests: tuple[_Request],
    group_by: Callable | None = None,
) -> tuple[tuple[_Request, ...], ...]:

    if group_by is None:
        group_by = _group_by

    invalid = next((i for i in requests if "+" in i.series_key), None)
    if invalid:
        raise ValueError(
            f"Invalid series key '{invalid}' found in individual requests. "
            "Use 'build_request_urls' with 'group_requests=False'."
        )
    requests = sorted(requests, key=group_by, )
    grouped_requests = tuple(
        tuple(group)
        for _, group in _it.groupby(requests, key=group_by, )
    )
    return grouped_requests


def _group_by(request: _Request, ) -> Any:
    return request.data_flow


def _build_url_for_grouped_requests(
    grouped_requests: tuple[_Request, ...],
) -> str:
    r"""
    """
    #[
    data_flow = grouped_requests[0].data_flow
    dim_lists = tuple(
        request.series_key_dims
        for request in grouped_requests
    )
    combined_dims = (
        "+".join(set(dim_group))
        for dim_group in zip(*dim_lists)
    )
    series_key = _Request._DIM_SEPARATOR.join(combined_dims, )
    url = _Request._URL_TEMPLATE.format(
        data_flow=data_flow,
        data_flow_separator=_Request._DATA_FLOW_SEPARATOR,
        series_key=series_key,
    )
    return url
    #]


class _Request:
    #[

    __slots__ = (
        "data_flow",
        "series_key_dims",
    )

    _DATA_FLOW_SEPARATOR = DATA_FLOW_SEPARATOR

    _DIM_SEPARATOR = DIM_SEPARATOR

    _URL_TEMPLATE = URL_TEMPLATE

    def __init__(
        self,
        data_flow: str = "",
        series_key_dims: Iterable[str] = (),
    ) -> None:
        self.data_flow = data_flow
        self.series_key_dims = tuple(series_key_dims)

    @classmethod
    def from_request_string(klass, request_string: str) -> _Request:
        data_flow, series_key, = request_string.split(klass._DATA_FLOW_SEPARATOR, )
        series_key_dims = tuple(series_key.split(klass._DIM_SEPARATOR, ))
        return klass(
            data_flow=data_flow,
            series_key_dims=series_key_dims,
        )

    @property
    def series_key(self, ) -> str:
        return self._DIM_SEPARATOR.join(self.series_key_dims, )

    @property
    def url(self, ) -> str:
        return self._URL_TEMPLATE.format(
            data_flow=self.data_flow,
            data_flow_separator=self._DATA_FLOW_SEPARATOR,
            series_key=self.series_key,
        )

    @property
    def num_dims(self, ) -> int:
        return len(self.series_key_dims)

    #]

