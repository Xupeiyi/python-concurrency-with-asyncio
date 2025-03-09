1. How to encapsulate create_task and await behavior?
2. How to be more flexible and responsive?
3. How to handle errors in some tasks?

gather
- must wait for all coroutines to finish before processing the results
- can't cancel other tasks if one throws an exception
