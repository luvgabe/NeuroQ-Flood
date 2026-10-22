"""
NeuroQ-Flood — USGS Data Quality Investigation

Checks historical discharge measurements for:
1. USGS approval and quality qualifiers
2. Sudden discharge changes
3. Missing measurement intervals
4. Differences between cached and official USGS data

This script does not modify the original dataset.
"""

import csv
import json
import urllib.request

from datetime import datetime, timezone
from pathlib import Path


SITE = "08074000"

START = "2024-05-01"
END = "2024-05-03"

ROOT = Path(__file__).resolve().parent.parent

CACHE = (
    ROOT
    / "data"
    / "historical"
    / f"usgs_{SITE}_{START}_{END}.csv"
)

OUTPUT = (
    ROOT
    / "data"
    / "results"
    / "usgs_quality_report.csv"
)


def parse_timestamp(value):

    return datetime.fromisoformat(
        value.replace("Z", "+00:00")
    ).astimezone(timezone.utc)


def download_official_data():

    url = (
        "https://waterservices.usgs.gov/nwis/iv/"
        f"?sites={SITE}"
        "&parameterCd=00060,00065"
        f"&startDT={START}"
        f"&endDT={END}"
        "&format=json"
    )

    print("\nDownloading official USGS measurements...")

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "NeuroQ-Flood-Research/1.0"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=45
    ) as response:

        data = json.load(response)

    records = {}

    for series in data["value"]["timeSeries"]:

        parameter = (
            series["variable"]["variableCode"][0]["value"]
        )

        if parameter not in ("00060", "00065"):
            continue

        for block in series["values"]:

            for measurement in block["value"]:

                timestamp = parse_timestamp(
                    measurement["dateTime"]
                )

                try:
                    value = float(measurement["value"])
                except (ValueError, TypeError):
                    continue

                record = records.setdefault(
                    timestamp,
                    {"timestamp": timestamp}
                )

                if parameter == "00060":

                    record["discharge_cfs"] = value

                    record["discharge_qualifiers"] = (
                        ",".join(
                            measurement.get("qualifiers", [])
                        )
                    )

                elif parameter == "00065":

                    record["gage_height_ft"] = value

                    record["gage_qualifiers"] = (
                        ",".join(
                            measurement.get("qualifiers", [])
                        )
                    )

    return records


def load_cached_data():

    if not CACHE.exists():

        raise FileNotFoundError(
            f"Historical CSV not found: {CACHE}"
        )

    records = {}

    with CACHE.open(newline="") as handle:

        reader = csv.DictReader(handle)

        for row in reader:

            timestamp = parse_timestamp(
                row["timestamp"]
            )

            records[timestamp] = {

                "timestamp": timestamp,

                "discharge_cfs": float(
                    row["discharge_cfs"]
                ),

                "gage_height_ft": float(
                    row["gage_height_ft"]
                )

            }

    return records


def investigate():

    official = download_official_data()

    cached = load_cached_data()

    OUTPUT.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    print(
        f"\nOfficial timestamps: {len(official)}"
    )

    print(
        f"Cached timestamps: {len(cached)}"
    )

    print("\nInvestigating discharge measurements...\n")

    columns = [
        "timestamp",
        "official_discharge_cfs",
        "cached_discharge_cfs",
        "official_gage_height_ft",
        "cached_gage_height_ft",
        "discharge_qualifiers",
        "gage_qualifiers",
        "discharge_difference_cfs",
        "previous_discharge_change_cfs",
        "minutes_since_previous",
        "flags"
    ]

    previous = None

    flagged = []

    with OUTPUT.open(
        "w",
        newline=""
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=columns
        )

        writer.writeheader()

        for timestamp in sorted(official):

            record = official[timestamp]

            # Evaluate only timestamps with
            # both discharge and gage readings.

            if (
                "discharge_cfs" not in record
                or "gage_height_ft" not in record
            ):
                continue

            old = cached.get(timestamp)

            discharge = record["discharge_cfs"]

            flags = []

            difference = None

            if old is None:

                flags.append(
                    "MISSING_FROM_CACHE"
                )

            else:

                difference = (
                    discharge
                    - old["discharge_cfs"]
                )

                if abs(difference) > 0.001:

                    flags.append(
                        "CACHE_MISMATCH"
                    )

            minutes_elapsed = None
            discharge_change = None

            if previous is not None:

                minutes_elapsed = (
                    timestamp
                    - previous["timestamp"]
                ).total_seconds() / 60

                discharge_change = (
                    discharge
                    - previous["discharge_cfs"]
                )

                if minutes_elapsed > 15:

                    flags.append(
                        "MEASUREMENT_GAP"
                    )

                # Diagnostic threshold only.
                # This does not automatically
                # indicate invalid data.

                if abs(discharge_change) > 500:

                    flags.append(
                        "LARGE_DISCHARGE_CHANGE"
                    )

                if (
                    previous["discharge_cfs"] > 100
                    and discharge < 1
                ):

                    flags.append(
                        "SUDDEN_NEAR_ZERO_DISCHARGE"
                    )

            if discharge < 1:

                flags.append(
                    "NEAR_ZERO_DISCHARGE"
                )

            result = {

                "timestamp":
                    timestamp.isoformat(),

                "official_discharge_cfs":
                    discharge,

                "cached_discharge_cfs":
                    (
                        old["discharge_cfs"]
                        if old else ""
                    ),

                "official_gage_height_ft":
                    record["gage_height_ft"],

                "cached_gage_height_ft":
                    (
                        old["gage_height_ft"]
                        if old else ""
                    ),

                "discharge_qualifiers":
                    record.get(
                        "discharge_qualifiers", ""
                    ),

                "gage_qualifiers":
                    record.get(
                        "gage_qualifiers", ""
                    ),

                "discharge_difference_cfs":
                    (
                        difference
                        if difference is not None
                        else ""
                    ),

                "previous_discharge_change_cfs":
                    (
                        discharge_change
                        if discharge_change is not None
                        else ""
                    ),

                "minutes_since_previous":
                    (
                        minutes_elapsed
                        if minutes_elapsed is not None
                        else ""
                    ),

                "flags":
                    ",".join(flags)

            }

            writer.writerow(result)

            if flags:

                flagged.append(result)

            previous = record

    print("=" * 60)

    print("USGS DATA QUALITY REPORT")

    print("=" * 60)

    print(
        f"\nFlagged measurements: {len(flagged)}"
    )

    for row in flagged[:30]:

        print(
            f"\nTimestamp: {row['timestamp']}"
        )

        print(
            "Discharge: "
            f"{row['official_discharge_cfs']} cfs"
        )

        print(
            "Gage height: "
            f"{row['official_gage_height_ft']} ft"
        )

        print(
            "USGS qualifiers: "
            f"{row['discharge_qualifiers']}"
        )

        print(
            f"Flags: {row['flags']}"
        )

    if len(flagged) > 30:

        print(
            f"\n... {len(flagged) - 30} "
            "additional flagged measurements "
            "are available in the CSV."
        )

    print("\nReport saved to:")

    print(OUTPUT)

    print(
        "\nNOTE: A flagged measurement is not "
        "automatically an invalid measurement."
    )


if __name__ == "__main__":
    investigate()