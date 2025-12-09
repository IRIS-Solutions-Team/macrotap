

import irispie as ir
import json

json_file_path = "xxx.json"
with open(json_file_path, "r", encoding="utf-8") as f:
    data = json.load(f, )

# Extract the structure information
observation_dims = data["structure"]["dimensions"]["observation"]

if len(observation_dims) != 1 or observation_dims[0]["id"] != "TIME_PERIOD":
    raise ValueError("Unexpected observation dimensions structure")

def _clean_sdmx_string(s: str) -> str:
    s = s.replace("-M", "-")
    return s

time_periods_info = observation_dims[0]["values"]
time_periods_sdmx = tuple(i["id"] for i in time_periods_info)
time_periods_sdmx = tuple(_clean_sdmx_string(i) for i in time_periods_sdmx)
time_periods = {
    str(i): ir.Period.from_sdmx_string(j)
    for i, j in enumerate(time_periods_sdmx, )
}


series_key_dims = data["structure"]["dimensions"]["series"]

def _extract_series_key_dim_value(dim:int, pointer:str) -> str:
    return series_key_dims[dim]["values"][int(pointer)]["id"]

def _extract_series_key_dim_info(dim:int, pointer:str) -> str:
    return series_key_dims[dim]["values"][int(pointer)]["name"]

def _parse_series_key(series_key: str) -> tuple[str, str]:
    pointers = series_key.split(":")
    parsed_series_key = tuple(
        _extract_series_key_dim_value(i, p, )
        for i, p in enumerate(pointers)
    )
    parsed_series_key_description = tuple(
        _extract_series_key_dim_info(i, p, )
        for i, p in enumerate(pointers)
    )
    parsed_series_key = ".".join(parsed_series_key)
    parsed_series_key_description = " | ".join(parsed_series_key_description)
    return parsed_series_key, parsed_series_key_description,

series_data = data["dataSets"][0]["series"]

output_db = ir.Databox()

for series_key, series_record, in series_data.items():
    parsed_series_key, parsed_series_key_description, = _parse_series_key(series_key, )
    series_values = tuple(
        float(i[0]) if i[0] is not None else None
        for i in series_record["observations"].values()
    )
    series_periods = tuple(
        time_periods[i]
        for i in series_record["observations"].keys()
    )
    output_db[parsed_series_key] = ir.Series(
        periods=series_periods,
        values=series_values,
        description=parsed_series_key_description,
    )

