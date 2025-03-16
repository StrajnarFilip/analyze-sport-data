from datetime import datetime


class HeartRateRecord:

    def __init__(self, recorded_at: datetime, heart_rate: float) -> None:
        self.recorded_at: datetime = recorded_at
        self.heart_rate: float = heart_rate
