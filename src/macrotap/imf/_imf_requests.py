
#[

from __future__ import annotations

# Typing imports
from typing import Any, Callable, Self

# Standard library imports
import itertools as _it
import dataclasses as _dc
import time as _ti

# Typing imports
from collections.abc import Iterable

#]


DIM_SEPARATOR = "."


CONTEXT = "dataflow"
AGENCY = "IMF.STA"
VERSION = "+"


URL_TEMPLATE = (
    r"https://api.imf.org/external/sdmx/3.0/data/"
    r"{context}/"
    r"{agency}/"
    r"{resource}/"
    r"{version}/"
    r"{series_key}?"
    r"detail=dataonly"
)


def build_request_urls(
    resource: str,
    request_strings: Iterable[str],
    **kwargs,
) -> tuple[str, ...]:
    r"""
    """
    requests = _get_requests_from_strings(resource, request_strings, )
    return tuple(
        i.url
        for i in requests
    )


def build_grouped_request_urls(
    resource: str,
    request_strings: Iterable[str],
    group_by: Callable | None = None,
) -> tuple[str, ...]:
    r"""
    """
    requests = _get_requests_from_strings(resource, request_strings, )
    grouped_requests = _group_requests(
        requests,
        group_by=group_by,
    )
    return tuple(
        _build_url_for_grouped_requests(i)
        for i in grouped_requests
    )


def _get_requests_from_strings(
    resource: str,
    request_strings: str | Iterable[str], 
) -> tuple[_Request, ...]:
    r"""
    """
    #[
    if isinstance(request_strings, str):
        request_strings = (request_strings, )
    requests = tuple(
        _Request.from_request_string(resource, n, )
        for n in request_strings
    )
    return requests
    #]


def _group_requests(
    requests: tuple[_Request],
    group_by: Callable[tuple[str, ...], Any],
) -> tuple[tuple[_Request, ...], ...]:
    r"""
    """
    def _group_by(request: _Request, ) -> Any:
        return group_by(request.series_key_dims, )
    #
    invalid = next((i for i in requests if "+" in i.series_key), None)
    if invalid:
        raise ValueError(
            f"Invalid series key '{invalid}' found in individual requests. "
            "Use 'build_request_urls' with 'group_requests=False'."
        )
    requests = sorted(requests, key=_group_by, )
    grouped_requests = tuple(
        tuple(group)
        for _, group in _it.groupby(requests, key=_group_by, )
    )
    return grouped_requests


def _build_url_for_grouped_requests(
    grouped_requests: tuple[_Request, ...],
) -> str:
    r"""
    """
    #[
    resource = grouped_requests[0].resource
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
        resource=resource,
        series_key=series_key,
        context=CONTEXT,
        agency=AGENCY,
        version=VERSION,
    )
    return url
    #]


class _Request:
    #[

    __slots__ = (
        "resource",
        "series_key_dims",
    )

    _DIM_SEPARATOR = DIM_SEPARATOR
    _URL_TEMPLATE = URL_TEMPLATE
    series_key_dims_constructor = tuple

    def __init__(
        self,
        resource: str,
        series_key_dims: tuple[str, ...],
    ) -> None:
        self.resource = resource
        self.series_key_dims = series_key_dims

    @classmethod
    def from_request_string(
        klass,
        resource: str,
        request_string: str,
        series_key_dims_constructor: Callable | None = None,
    ) -> Self:
        r"""
        """
        if series_key_dims_constructor is None:
            series_key_dims_constructor = klass.series_key_dims_constructor
        request_string_split = request_string.split(klass._DIM_SEPARATOR, )
        series_key_dims = series_key_dims_constructor(request_string_split, )
        return klass(
            resource=resource,
            series_key_dims=series_key_dims,
        )

    @property
    def series_key(self, ) -> str:
        return self._DIM_SEPARATOR.join(self.series_key_dims, )

    @property
    def url(self, ) -> str:
        return self._URL_TEMPLATE.format(
            resource=self.resource,
            series_key=self.series_key,
            context=CONTEXT,
            agency=AGENCY,
            version=VERSION,
        )

    @property
    def num_dims(self, ) -> int:
        return len(self.series_key_dims)

    #]

