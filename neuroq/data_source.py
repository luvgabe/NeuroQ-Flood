"""
NeuroQ-Flood — USGS Data Source

Retrieves historical environmental measurements.

Station: 08074000
Location: Buffalo Bayou, Houston

Parameters:
00065 = Gage height
00060 = Stream discharge
"""

import csv
import json

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


STATION = "08074000"

PARAMETERS = {
    "00065": "gage_height_ft",
    "00060": "discharge_cfs"
}

API = "https://waterservices.usgs.gov/nwis/iv/"


def download_usgs(
    start,
    end,
    destination,
    station=STATION
):

    query = urlencode({
        "format": "json",
        "sites": station,
        "startDT": start,
        "endDT": end,
        "parameterCd": "00065,00060",
        "siteStatus": "all"
    })

    request = Request(
        API + "?" + query,
        headers={
            "User-Agent": "NeuroQ-Flood Research Prototype"
        }
    )

    with urlopen(request, timeout=45) as response:
        payload = json.load(response)

    grouped = {}

    for series in payload.get(
        "value", {}
    ).get("timeSeries", []):

        code = (
            series.get("variable", {})
            .get("variableCode", [{}])[0]
            .get("value")
        )

        field = PARAMETERS.get(code)

        if not field:
            continue

        for block in series.get("values", []):

            for item in block.get("value", []):

                try:
                    value = float(item["value"])

                except (
                    ValueError,
                    TypeError,
                    KeyError
                ):
                    continue

                if value < 0:
                    continue

                timestamp = datetime.fromisoformat(
                    item["dateTime"].replace(
                        "Z", "+00:00"
                    )
                )

                timestamp = (
                    timestamp
                    .astimezone(timezone.utc)
                    .isoformat()
                )

                grouped.setdefault(
                    timestamp,
                    {"timestamp": timestamp}
                )[field] = value

    rows = [
        grouped[t]
        for t in sorted(grouped)
        if all(
            field in grouped[t]
            for field in PARAMETERS.values()
        )
    ]

    if not rows:
        raise RuntimeError(
            "No matching USGS measurements found."
        )

    destination = Path(destination)

    destination.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with destination.open(
        "w",
        newline=""
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "timestamp",
                "gage_height_ft",
                "discharge_cfs"
            ]
        )

        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def load_csv(path):

    with Path(path).open(
        newline=""
    ) as handle:

        reader = csv.DictReader(handle)

        required = {
            "timestamp",
            "gage_height_ft",
            "discharge_cfs"
        }

        if not required.issubset(
            reader.fieldnames or []
        ):
            raise ValueError(
                "Historical CSV missing required columns."
            )

        rows = []

        for row in reader:

            try:

                timestamp = datetime.fromisoformat(
                    row["timestamp"].replace(
                        "Z", "+00:00"
                    )
                )

                if timestamp.tzinfo is None:
                    continue

                gage = float(
                    row["gage_height_ft"]
                )

                discharge = float(
                    row["discharge_cfs"]
                )

                if gage < 0 or discharge < 0:
                    continue

                rows.append({
                    "timestamp": timestamp.astimezone(
                        timezone.utc
                    ),
                    "gage_height_ft": gage,
                    "discharge_cfs": discharge
                })

            except (
                ValueError,
                TypeError
            ):
                continue

    rows.sort(
        key=lambda row: row["timestamp"]
    )

    if not rows:
        raise ValueError(
            "No usable historical measurements."
        )

    return rows