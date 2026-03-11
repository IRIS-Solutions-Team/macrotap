r"""
"""


#[

from __future__ import annotations

# Third-party imports
import datapie as _ap

# Application imports
from .. import _dim_requests as _dr
from .. import _workflows as _wf

#]


_RESOURCE = "data"
_AGENCY = "all"
_VERSION = "latest"


_URL_TEMPLATE = (
    r"https://data-api.ecb.europa.eu/service/"
    r"{resource}/"
    r"{agency},{dataflow},{version}/"
    r"{{series_key}}?"
    r"format=csvdata&detail=dataonly"
)


_FREQUENCY_HEADER = "FREQ"
_KEY_HEADER = "KEY"


def build_request_urls_for_ecb(
    dataflow: str,
    request_strings: Iterable[str],
    group_requests_by: Callable | None = None,
) -> tuple[str, ...]:
    r"""
    """
    #[
    url_template = _URL_TEMPLATE.format(
        dataflow=dataflow,
        resource=_RESOURCE,
        agency=_AGENCY,
        version=_VERSION,
    )
    return _dr.build_request_urls(
        request_strings,
        url_template,
        group_requests_by=group_requests_by,
    )
    #]


def from_ecb(
    dataflow: str,
    request_strings: Iterable[str],
    **kwargs,
) -> _ap.Databox:
    r"""
    """
    #[

    url_template = _URL_TEMPLATE.format(
        dataflow=dataflow,
        resource=_RESOURCE,
        agency=_AGENCY,
        version=_VERSION,
    )

    return _wf.run_sdmx_csv_workflow(
        request_strings=request_strings,
        url_template=url_template,
        build_extractors={
            "build_frequency_extractor": _build_frequency_extractor,
            "build_key_extractor": _build_key_extractor,
        },
        **kwargs,
    )

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


def _build_key_extractor(
    header: Iterable[str],
) -> Callable:
    r"""
    """
    #[
    key_index = header.index(_KEY_HEADER, )
    #
    def db_key_extractor(row: Iterable[str], ) -> str:
        return _remove_dataflow_from_key(row[key_index].strip(), )
    #
    return db_key_extractor
    #]


def _remove_dataflow_from_key(
    key: str,
) -> str:
    r"""
    """
    #[
    split_key = key.split(_dr.DIM_SEPARATOR, )
    return _dr.DIM_SEPARATOR.join(split_key[1:], )
    #]

