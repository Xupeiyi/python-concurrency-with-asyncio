import asyncio
import concurrent.futures
import time
from collections import defaultdict
import functools
from multiprocessing import Value


map_progress: Value


def init(progress: Value):
    global map_progress
    map_progress = progress


def partition(data: list, chunk_size: int) -> list:
    for i in range(0, len(data), chunk_size):
        yield data[i: i + chunk_size]


def map_frequencies(chunk: list[str]) -> dict[str, int]:
    counter = defaultdict(int)
    for line in chunk:
        word, _, count, _ = line.split('\t')
        counter[word] += int(count)

    with map_progress.get_lock():
        map_progress.value += 1

    return counter


def merge_dictionaries(first: dict[str, int], second: dict[str, int]) -> dict[str, int]:
    merged = first
    for key, value in second.items():
        merged[key] += value
    return merged


async def reduce(loop, executor, counters, chunk_size) -> dict[str, int]:
    chunks: list[list[dict]] = list(partition(counters, chunk_size))
    reducers = []

    while len(chunks[0]) > 1:
        for chunk in chunks:
            reducer = functools.partial(functools.reduce,merge_dictionaries, chunk)
            reducers.append(loop.run_in_executor(executor, reducer))

        reducer_chunks = await asyncio.gather(*reducers)
        chunks = list(partition(reducer_chunks, chunk_size))
        reducers.clear()
    return chunks[0][0]


async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f'Finished {map_progress.value} / {total_partitions} map operations')
        await asyncio.sleep(1)


async def main(partition_size: int):
    global map_progress

    with open('googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        contents = f.readlines()
        print(len(contents))
        loop = asyncio.get_running_loop()
        map_progress = Value('i', 0)

        tasks = []
        with concurrent.futures.ProcessPoolExecutor(initializer=init, initargs=(map_progress,)) as executor:
            start = time.time()

            total_partitions = len(contents) // partition_size
            reporter = asyncio.create_task(progress_reporter(total_partitions))

            for chunk in partition(contents, partition_size):
                tasks.append(loop.run_in_executor(executor, functools.partial(map_frequencies, chunk)))

            intermediate_results = await asyncio.gather(*tasks)

            await reporter

            final_result = functools.reduce(merge_dictionaries, intermediate_results)
            # final_result = await reduce(loop, executor, intermediate_results, chunk_size=1500)

            print(f'Aardvark has appeard {final_result["Aardvark"]} times.')

            end = time.time()
            print(f"Time taken to process the file: {end - start} seconds")


if __name__ == "__main__":
    asyncio.run(main(partition_size=300000))
