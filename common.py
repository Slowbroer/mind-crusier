import json
import datetime
from typing import List


def read_file_and_filter(file_path: str) -> str:
    """
    Read the file and filter the records
    """
    with open("./resources/records/" + file_path, 'r', encoding='utf-8') as handler:
        lines = handler.readlines()
        return filter_records(lines)

def filter_records(lines: List[str]) -> dict:
    """
    Filter the records
    """
    res = {}
    for line in lines:
        record = json.loads(line)
        if record['name'] == "张三":
            timestamp = int(record['timestamp'] / 1000)
            datetime_array = datetime.datetime.fromtimestamp(timestamp)
            date = datetime_array.strftime('%Y-%m-%d')
            if date in res:
                res[date].append(record)
            else:
                res[date] = [record]
    return res

def sort_and_output_records(date: str, records: dict):
    """
    Sort the records and output to the file
    """
    sorted_records = sorted(records, key=lambda x: x['timestamp'])
    return output_file(date, sorted_records)

def output_file(date: str, records: list):
    """
    Output the records to a file
    """
    with open(f'./resources/results/{date}.txt', 'w', encoding='utf-8') as handler:
        to_write_records = [f'{json.dumps(record, ensure_ascii=False)}\n' for record in records]
        handler.writelines(to_write_records)
    return date
