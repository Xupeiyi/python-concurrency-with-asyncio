import asyncio
import functools
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from util import async_timed


def mean_for_row(arr, row):
    return np.mean(arr[row])


data_points = 2400000000
n_rows = 50
n_columns = int(data_points / n_rows)

matrix = np.arange(data_points).reshape(n_rows, n_columns)


@async_timed
async def main():
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor() as pool:
        tasks = []

        for i in range(n_rows):
            calc_row_i_mean = functools.partial(mean_for_row, matrix, i)
            tasks.append(loop.run_in_executor(pool, calc_row_i_mean))

        results = await asyncio.gather(*tasks)


asyncio.run(main())
