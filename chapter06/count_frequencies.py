import asyncio
import concurrent.futures
import time
from collections import defaultdict
from typing import DefaultDict, TypeAlias
import functools
from multiprocessing import Value

# We can't define count_progress = Value('i',0) here
# because when each process is created, the script we create
# it from is run again per each process.
# This means each script will recreate count_progress.
count_progress: Value

Frequencies: TypeAlias = DefaultDict[str, int]


def init(progress: Value):
    global count_progress
    count_progress = progress


def partition(data: list, chunk_size: int) -> list:
    for i in range(0, len(data), chunk_size):
        yield data[i: i + chunk_size]


def count_frequencies(lines: list[str]) -> Frequencies:
    frequencies = defaultdict(int)
    for line in lines:
        word, _, count, _ = line.split('\t')
        frequencies[word] += int(count)

    with count_progress.get_lock():
        count_progress.value += 1

    return frequencies


def merge_two_frequencies(first: Frequencies, second: Frequencies) -> Frequencies:
    merged = first
    for key, value in second.items():
        merged[key] += value
    return merged


def merge_frequencies(frequencies_list: list[Frequencies]) -> Frequencies:
    return functools.reduce(merge_two_frequencies, frequencies_list)


async def reduce(loop, executor, frequencies_list, chunk_size) -> Frequencies:
    while len(frequencies_list) > chunk_size:
        tasks = []
        for chunk in partition(frequencies_list, chunk_size):
            merge_frequencies_in_chunk = functools.partial(merge_frequencies, chunk)
            task = loop.run_in_executor(executor, merge_frequencies_in_chunk)
            tasks.append(task)
        frequencies_list: list[Frequencies] = await asyncio.gather(*tasks)

    return merge_frequencies(frequencies_list)


async def progress_reporter(n_partitions: int):
    while count_progress.value < n_partitions:
        print(f'Finished {count_progress.value} / {n_partitions} map operations')
        await asyncio.sleep(1)


async def main(partition_size: int):
    global count_progress

    with open('googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        lines = f.readlines()
    print(len(lines))

    loop = asyncio.get_running_loop()
    count_progress = Value('i', 0)
    with concurrent.futures.ProcessPoolExecutor(initializer=init, initargs=(count_progress,)) as executor:
        start = time.time()

        # 1. Map
        n_partitions = len(lines) // partition_size
        reporter = asyncio.create_task(progress_reporter(n_partitions))
        tasks = []
        for chunk in partition(lines, partition_size):
            count_frequencies_in_chunk = functools.partial(count_frequencies, chunk)
            task = loop.run_in_executor(executor, count_frequencies_in_chunk)
            tasks.append(task)
        frequencies_list = await asyncio.gather(*tasks)
        await reporter

        # 2. Reduce
        # frequencies = merge_frequencies(frequencies_list)
        frequencies = await reduce(loop, executor, frequencies_list, chunk_size=1500)
        print(f'Aardvark has appeard {frequencies["Aardvark"]} times.')

        end = time.time()
        print(f"Time taken to process the file: {end - start} seconds")


if __name__ == "__main__":
    asyncio.run(main(partition_size=60000))
