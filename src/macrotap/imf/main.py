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


_DEFAULT_CONTEXT = "dataflow"
_DEFAULT_AGENCY = "IMF.STA"
_DEFAULT_VERSION = "+"


_URL_TEMPLATE = (
    r"https://api.imf.org/external/sdmx/3.0/data/"
    r"{context}/"
    r"{agency}/"
    r"{resource}/"
    r"{version}/"
    r"{{series_key}}?"
    r"detail=dataonly"
)


_HEADERS = {"accept": "application/csv", }


def from_imf(
    resource: str,
    request_strings: Iterable[str],
    *,
    context: str = _DEFAULT_CONTEXT,
    agency: str = _DEFAULT_AGENCY,
    version: str = _DEFAULT_VERSION,
    #
    **kwargs,
) -> _ap.Databox:
    r"""
    """
    #[
    url_template = _URL_TEMPLATE.format(
        resource=resource,
        context=context,
        agency=agency,
        version=version,
    )
    return _wf.run_sdmx_csv_workflow(
        request_strings=request_strings,
        url_template=url_template,
        headers=_HEADERS,
        build_extractors={
            "build_key_extractor": _build_key_extractor,
        },
        **kwargs,
    )
    #]


def _build_key_extractor(
    header: Iterable[str],
) -> Callable:
    r"""
    """
    #[
    action_index = header.index("ACTION", )
    time_period_index = header.index("TIME_PERIOD", )
    dim_separator = _dr.DIM_SEPARATOR
    #
    def db_key_extractor(row: Iterable[str], ) -> str:
        return dim_separator.join(row[action_index+1:time_period_index], )
    #
    return db_key_extractor
    #]

