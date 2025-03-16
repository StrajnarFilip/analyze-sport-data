from datetime import timedelta
from analyze_sport_data.heart_rate_record import HeartRateRecord
from garmin_fit_sdk import Decoder, Stream


class FileRecords:

    def __init__(self,
                 name: str,
                 heart_rate_records: list[HeartRateRecord],
                 heart_rate_time_offset: timedelta = timedelta()):
        self.name = name
        self.heart_rate_records = [
            HeartRateRecord((record.recorded_at + heart_rate_time_offset),
                            record.heart_rate) for record in heart_rate_records
        ]
        self.heart_rate_time_offset = heart_rate_time_offset


def from_fit_file(file_path: str,
                  friendly_name: str | None = None) -> FileRecords:
    stream = Stream.from_file(file_path)
    decoder = Decoder(stream)
    messages, _errors = decoder.read()
    records = messages["record_mesgs"]
    heart_rate_records: list[HeartRateRecord] = [
        HeartRateRecord(record["timestamp"], record["heart_rate"])
        for record in records
        if "heart_rate" in record.keys() and record["heart_rate"] != None
    ]
    return FileRecords(friendly_name if friendly_name != None else file_path,
                       heart_rate_records)
