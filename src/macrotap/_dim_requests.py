r"""
Handle dimensionalized requests
"""


#[

from __future__ import annotations

# Typing imports
from typing import Any, Callable, Self
from collections.abc import Iterable

# Standard library imports
import itertools as _it

#]


DIM_SEPARATOR = "."


def build_request_urls(
    request_strings: Iterable[str],
    url_template: str,
    group_requests_by: Callable | None = None,
) -> tuple[str, ...]:
    r"""
    """
    needs_grouping = group_requests_by is not None
    build = {
        True: _build_grouped_request_urls,
        False: _build_individual_request_urls,
    }[needs_grouping]
    #
    return build(
        request_strings,
        url_template,
        group_requests_by=group_requests_by,
    )


def _build_individual_request_urls(
    request_strings: Iterable[str],
    url_template: str,
    **kwargs,
) -> tuple[str, ...]:
    r"""
    """
    requests = _build_requests_from_strings(
        request_strings,
        url_template,
    )
    return tuple(
        i.url
        for i in requests
    )


def _build_grouped_request_urls(
    request_strings: Iterable[str],
    url_template: str,
    group_requests_by: Callable | None = None,
) -> tuple[str, ...]:
    r"""
    """
    requests = _build_requests_from_strings(
        request_strings,
        url_template,
    )
    request_groups = _group_requests(
        requests,
        group_requests_by=group_requests_by,
    )
    return tuple(
        _build_url_for_request_group(i, )
        for i in request_groups
    )


def _build_requests_from_strings(
    request_strings: str | Iterable[str], 
    url_template: str,
) -> tuple[Request, ...]:
    r"""
    """
    #[
    if isinstance(request_strings, str):
        request_strings = (request_strings, )
    requests = tuple(
        Request.from_request_string(n, url_template, )
        for n in request_strings
    )
    return requests
    #]


def _group_requests(
    requests: tuple[Request],
    group_requests_by: Callable[tuple[str, ...], Any] = lambda x: x,
) -> tuple[tuple[Request, ...], ...]:
    r"""
    """
    def _group_requests_by(request: Request, ) -> Any:
        return group_requests_by(request.series_key_dims, )
    #
    # Throw an error if any request groups multiple values using the + sign
    invalid = next((i for i in requests if "+" in i.series_key), None)
    if invalid:
        raise ValueError(
            f"Invalid series key '{invalid}' found in individual requests. "
            "Use 'build_request_urls' with 'group_requests=False'."
        )
    #
    requests = sorted(
        requests,
        key=_group_requests_by,
    )
    request_groups = tuple(
        tuple(group)
        for _, group in _it.groupby(requests, key=_group_requests_by, )
    )
    return request_groups


def _build_url_for_request_group(
    request_group: tuple[Request, ...],
) -> str:
    r"""
    """
    #[
    url_template = request_group[0].url_template
    dim_lists = tuple(
        request.series_key_dims
        for request in request_group
    )
    grouped_dims = (
        "+".join(set(dim_group))
        for dim_group in zip(*dim_lists)
    )
    grouped_request = Request(
        series_key_dims=grouped_dims,
        url_template=url_template,
    )
    return grouped_request.url
    #]


class Request:
    #[

    __slots__ = (
        "series_key_dims",
        "url_template",
    )

    def __init__(
        self,
        series_key_dims: Iterable[str],
        url_template: str,
    ) -> None:
        self.series_key_dims = tuple(series_key_dims)
        self.url_template = url_template

    @classmethod
    def from_request_string(
        klass,
        request_string: str,
        url_template: str,
    ) -> Self:
        r"""
        """
        request_string_split = request_string.split(DIM_SEPARATOR, )
        series_key_dims = tuple(request_string_split, )
        return klass(
            series_key_dims=series_key_dims,
            url_template=url_template,
        )

    @property
    def series_key(self, ) -> str:
        return DIM_SEPARATOR.join(self.series_key_dims, )

    @property
    def url(self, ) -> str:
        return self.url_template.format(series_key=self.series_key, )

    @property
    def num_dims(self, ) -> int:
        return len(self.series_key_dims)

    #]

