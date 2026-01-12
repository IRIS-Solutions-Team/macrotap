
#[

from __future__ import annotations

# Third-party imports
import datapie as _ap
import requests as _rq

# Local imports
from ._imf_requests import build_request_urls, build_grouped_request_urls
from ._imf_response import parse_response_csv

#]


REQUEST_DISPATCH = {
    True: build_grouped_request_urls,
    False: build_request_urls,
}

_HEADERS = {"accept": "application/csv", }


def from_imf(
    resource: str,
    request_strings: str | Iterable[str],
    group_requests: bool = True,
    group_by: Callable | None = None,
    merge_strategy: str = "error",
    target_db: _ap.Databox | None = None,
    return_info: bool = False,
) -> _ap.Databox:
    r"""
    """
    if isinstance(request_strings, str):
        request_strings = (request_strings, )
    request_strings = tuple(set(request_strings, ))

    build_request_urls = REQUEST_DISPATCH[group_requests]
    urls = build_request_urls(resource, request_strings, group_by=group_by, )
    responses = []

    if target_db is None:
        target_db = _ap.Databox()

    output_db = _ap.Databox()
    info = []

    for url in urls:
        response = _rq.get(url, headers=_HEADERS, )
        response_csv = response.content.decode()
        response_db = parse_response_csv(response_csv, )
        output_db.merge(
            response_db,
            strategy=merge_strategy,
        )
        if return_info:
            info.append({
                "url": url,
                "response": response_csv,
            })

    if group_requests:
        output_db.keep(request_strings, )

    target_db.merge(
        output_db,
        strategy=merge_strategy,
    )

    if return_info:
        return target_db, info,

    return target_db

