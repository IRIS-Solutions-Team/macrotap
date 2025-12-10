
#[

from __future__ import annotations

# Third-party imports
import datapie as _ap
import requests as _rq

# Local imports
from ._imf_requests import build_request_urls, build_grouped_request_urls
from ._imf_response import parse_response_json

#]


REQUEST_DISPATCH = {
    True: build_grouped_request_urls,
    False: build_request_urls,
}

_HEADERS = {"accept": "application/json", }


def from_imf(
    request_strings: str | Iterable[str],
    group_requests: bool = True,
    group_by: Callable | None = None,
    merge_strategy: str = "error",
    return_info: bool = False,
) -> _ap.Databox:
    r"""
    """
    if isinstance(request_strings, str):
        request_strings = (request_strings, )
    request_strings = tuple(set(request_strings, ))

    build_request_urls = REQUEST_DISPATCH[group_requests]
    urls = build_request_urls(request_strings, group_by=group_by, )

    output_db = _ap.Databox()

    for url in urls:
        response = _rq.get(url, headers=_HEADERS, )
        response_json = response.json()
        response_db = parse_response_json(response_json, )
        output_db.merge(
            response_db,
            strategy=merge_strategy,
        )

    if return_info:
        info = {
            "urls": urls,
        }
        return output_db, {"urls": urls, }

    return output_db

