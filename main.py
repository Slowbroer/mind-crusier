import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from common import read_file_and_filter, sort_and_output_records


def main():
    start_time = time.time()
    all_source_dir = os.listdir("./resources/records/")
    all_source_files = [
        item for item in all_source_dir if (
            item.endswith('.txt') and os.path.isfile("./resources/records/" + item)
        )
    ]

    todo_read_tasks = []
    todo_sort_tasks = {}
    all_records_by_date = {}
    with ProcessPoolExecutor() as process_pool_executor:
        # read the files and filter the records
        for file in all_source_files:
            todo_read_tasks.append(process_pool_executor.submit(read_file_and_filter, file))
        done_read_iter = as_completed(todo_read_tasks)
        for future in done_read_iter:
            records_with_date = future.result()
            for date, records in records_with_date.items():
                if date in all_records_by_date:
                    all_records_by_date[date] += records
                else:
                    all_records_by_date[date] = records

        # sort the records and output to files
        for date, records in all_records_by_date.items():
            future = process_pool_executor.submit(sort_and_output_records, date, records)
            todo_sort_tasks[future] = date
        done_sort_iter = as_completed(todo_sort_tasks)
        for future in done_sort_iter:
            date = future.result()
            print(f'the {date} file is generated successfully')
    print(f'the time cost is: {time.time() - start_time}s')

if __name__ == "__main__":
    main()
