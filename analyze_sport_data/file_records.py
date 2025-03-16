from datetime import datetime, timedelta
from analyze_sport_data.heart_rate_record import HeartRateRecord
from garmin_fit_sdk import Decoder, Stream
from xml.etree import ElementTree


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


def from_fit_file(
    file_path: str,
    friendly_name: str | None = None,
    heart_rate_time_offset: timedelta = timedelta()
) -> FileRecords:
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
                       heart_rate_records, heart_rate_time_offset)


def from_tcx_file(
    file_path: str,
    friendly_name: str | None = None,
    heart_rate_time_offset: timedelta = timedelta()
) -> FileRecords:
    empty_file_records = FileRecords(file_path, [])
    heart_rate_records: list[HeartRateRecord] = []

    activities_tag = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activities'
    activity_tag = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Activity'
    lap_tag = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Lap'
    track_tag = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Track'
    trackpoint_tag = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Trackpoint'
    time_tag = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Time'
    heart_rate_bpm_tag = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}HeartRateBpm'
    value_tag = '{http://www.garmin.com/xmlschemas/TrainingCenterDatabase/v2}Value'

    activities = ElementTree.parse(file_path).getroot().find(activities_tag)
    if activities == None:
        return empty_file_records

    for activity in activities.findall(activity_tag):
        for lap in activity.findall(lap_tag):
            for track in lap.findall(track_tag):
                for trackpoint in track.findall(trackpoint_tag):
                    heart_rate = trackpoint.find(heart_rate_bpm_tag)
                    if heart_rate == None:
                        continue
                    if type(heart_rate) is not ElementTree.Element:
                        continue
                    heart_rate_value = heart_rate.find(value_tag)
                    if heart_rate_value is None or heart_rate_value.text is None:
                        continue

                    iso_time_element = trackpoint.find(time_tag)
                    if type(iso_time_element) is not ElementTree.Element:
                        continue
                    if iso_time_element.text is None:
                        continue

                    record_at = datetime.fromisoformat(iso_time_element.text)
                    heart_rate_records.append(
                        HeartRateRecord(record_at,
                                        float(heart_rate_value.text)))

    return FileRecords(friendly_name if friendly_name != None else file_path,
                       heart_rate_records, heart_rate_time_offset)
