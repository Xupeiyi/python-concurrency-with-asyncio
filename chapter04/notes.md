1. How to encapsulate create_task and await behavior?
2. How to be more flexible and responsive?
3. How to handle errors in some tasks?

gather
- must wait for all coroutines to finish before processing the results
- can't cancel other tasks if one throws an exception

as_completed
- no deterministic order of results, whatever finishes first is returned first
- can't figure out which tasks are running and cancel them when there are errors

wait
- doesn't throw exception
- can execute logic when all tasks are done, one task is done, or when one exception is met
- need to explicitly cancel pending tasks when timeout is reached 
- It's better pass in a list of tasks instead of coroutines, otherwise we cannot see 
  the tasks returned by wait are wrapped from which coroutines
