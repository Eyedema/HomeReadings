def rename_import_columns(dict_row: dict) -> dict:
    header_map = {
        "Timestamp": "timestamp",
        "Temperature_Celsius(°C)": "temperature",
        "Relative_Humidity(%)": "relative_humidity",
        "Absolute_Humidity(g/m³)": "absolute_humidity",
        "DPT_Celsius(°C)": "dew_point",
        "VPD(kPa)": "vapor_pressure_deficit",
    }
    ret = {}

    for k, v in dict_row.items():
        new_k = header_map.get(k)
        if new_k:
            ret[new_k] = v

    return ret
