r"""
Handle frequencies and periods in responses
"""


#[

from __future__ import annotations

# Third-party imports
import datapie as _ap

#]


FREQUENCY_MAP = {
    "Y".casefold(): _ap.Frequency.YEARLY,
    "A".casefold(): _ap.Frequency.YEARLY,
    "H".casefold(): _ap.Frequency.HALFYEARLY,
    "S".casefold(): _ap.Frequency.HALFYEARLY,
    "Q".casefold(): _ap.Frequency.QUARTERLY,
    "M".casefold(): _ap.Frequency.MONTHLY,
    "D".casefold(): _ap.Frequency.DAILY,
    "B".casefold(): _ap.Frequency.DAILY,
}


def clean_sdmx_period_string(
    period_string: str,
) -> str:
    r"""
    Dates in response do not conform to ISO 8601 due to use of "-M" for months
    """
    period_string = period_string.replace("-M", "-")
    period_string = period_string.replace("-S", "-H")
    return period_string

