import json
import datetime
from typing import List


DAY_MICRO_SECONDS = 24 * 3600 * 1000

def read_file(file_path: str) -> str:
    with open("./resources/records/" + file_path, 'r', encoding='utf-8') as handler:
        lines = handler.readlines()
        return filter_records(lines)
    
def filter_records(lines: List[str]) -> dict:
    res = {}
    for line in lines:
        record = json.loads(line)
        if record['name'] == "张三":
            timestamp = int(record['timestamp'] / 1000)
            datetime_array = datetime.datetime.fromtimestamp(timestamp)
            date = datetime_array.strftime('%Y-%m-%d')
            # TODO::need to optimize
            if date in res:
                res[date].append(record)
            else:
                res[date] = [record]
    return res

def sort_records(date: str, records: dict):
    sorted_records = sorted(records, key=lambda x: x['timestamp'])
    return output_file(date, sorted_records)

def output_file(date: str, records: list):
    """
    TODO:: optimize
    """
    with open(f'./resources/results/{date}.txt', 'w', encoding='utf-8') as handler:
        to_write_records = [json.dumps(record, ensure_ascii=False) + '\n' for record in records]
        handler.writelines(to_write_records)
    return date
