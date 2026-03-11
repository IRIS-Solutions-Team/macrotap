r"""
"""


#[

from __future__ import annotations

# Third-party imports
import datapie as _ap
import requests as _rq

# Application imports
from . import _dim_requests as _dr
from . import _sdmx_csv_responses as _sr

#]


def run_sdmx_csv_workflow(
    request_strings: str | Iterable[str],
    url_template: str,
    #
    headers: dict | None = None,
    build_extractors: dict | None = None,
    #
    group_requests_by: Callable | None = None,
    merge_strategy: str = "error",
    target_db: _ap.Databox | None = None,
    discard_unwanted: bool = True,
    return_info: bool = False,
) -> _ap.Databox:
    r"""
    """
    #[

    build_extractors = build_extractors or {}

    urls = _dr.build_request_urls(
        request_strings,
        url_template,
        group_requests_by=group_requests_by,
    )

    if target_db is None:
        target_db = _ap.Databox()

    output_db = _ap.Databox()
    info = []

    for url in urls:
        response = _rq.get(url, headers=headers, )
        content = response.content.decode()
        #
        response_db = _sr.parse_response(
            content,
            **build_extractors,
        )
        #
        output_db.merge(
            response_db,
            strategy=merge_strategy,
        )
        info.append({
            "url": url,
            "response": content,
        })

    if discard_unwanted and group_requests_by is not None:
        output_db.keep(request_strings, )

    target_db.merge(
        output_db,
        strategy=merge_strategy,
    )

    if return_info:
        return target_db, info,

    return target_db

    #]

