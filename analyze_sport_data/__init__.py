from datetime import datetime
from typing import Iterable
from analyze_sport_data.file_records import FileRecords
from pandas import DataFrame, Series


def heart_rate_at_datetime(file_records: FileRecords,
                           recorded_at: datetime) -> float | None:
    for heart_rate_record in file_records.heart_rate_records:
        if heart_rate_record.recorded_at == recorded_at:
            return heart_rate_record.heart_rate

    return None


def heart_rate_dataframe(
        file_records_iterable: Iterable[FileRecords]) -> DataFrame:
    recorded_at_points_set: set[datetime] = set()

    for file_records in file_records_iterable:
        for record in file_records.heart_rate_records:
            recorded_at_points_set.add(record.recorded_at)

    recorded_at_index = sorted(recorded_at_points_set)
    heart_rate_measurements: dict[str, list[float | None]] = {}

    for file_records in file_records_iterable:
        heart_rate_measurements[file_records.name] = [
            heart_rate_at_datetime(file_records, recorded_at)
            for recorded_at in recorded_at_index
        ]

    return DataFrame(data=heart_rate_measurements)
