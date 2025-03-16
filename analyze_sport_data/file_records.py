from datetime import timedelta
from analyze_sport_data.heart_rate_record import HeartRateRecord


class FileRecords:

    def __init__(self,
                 name: str,
                 heart_rate_records: list[HeartRateRecord],
                 heart_rate_time_offset: timedelta = timedelta()):
        self.name = name
        self.heart_rate_records = heart_rate_records
        self.heart_rate_time_offset = heart_rate_time_offset
