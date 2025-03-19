1. How to encapsulate create_task and await behavior?
2. How to be more flexible and responsive?
3. How to handle errors in some tasks?

gather
- must wait for all coroutines to finish before processing the results
- can't cancel other tasks if one throws an exception

as_completed
- returns an iterator that yields futures as they complete
- no deterministic order of results, whatever finishes first is returned first
- can't figure out which tasks are running and cancel them when there are errors 


wait
- doesn't throw exception
-