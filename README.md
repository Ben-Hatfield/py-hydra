# py-hydra
Python Queued stdin/stdout Multi-Threading manager.

Because of the GIL, this is only useful when the time to save from the blocking call is I/O driven, for example network I/O.

This blocking function is internally referred to by hydra as the `task`.

Uses multiple Queues to get data into and out of multiple running threads.

This abstraction is achieved by launching a Hydra class that manages the locking and unlocking of critical sections.

The default critical sections that are managed are: data sent to the task; and results returned from the task. (stdin, stdout)

```
# Time consuming function
requests.get('https://jsonplaceholder.typicode.com/albums')

# Hydra class init and execution
url_list = ['https://jsonplaceholder.typicode.com/albums' for x in range(3)]

with hydra.Hydra() as fast:
    for url in url_list:
        fast.add_work(url)
    fast.do_work('thread_id_root', requests.get, threads=2)
    results = fast.get_results(len(url_list))

INPUT QUEUE   TASK  FUNCTION   OUPUT QUEUE
##########  | ############## | ############
# url    #  | url-> get(url) | # responce #
# url    #  | url-> get(url) | # responce #
# url    #  |                | # responce #
##########  | #############  | ############

# 0 four urls put into work queue;
# 1 two threads running the 'get' task collect waiting url from work queue;
# 2 two results put into output queue
# 3 one thread collects the remaining "args", the other thread dies.
# 4 the last result is put into outbound queue
# 5 the three results are collected
```

### Sample applications:

##### Hydra running up to 31337 http GET requests in parallel.

```
import hydra, requests
url_list = ['https://github.com/Ben-Hatfield','https://docs.python.org/3/library/threading.html', ETC...]
with hydra.Hydra() as bad_idea:
    for url in url_list:
        bad_idea.add_work(url)
    bad_idea.do_work(thread_number=31337, task=requests.get, block=True)
    webpages = bad_idea.get_results(len(url_list))
```
##### Two separate, simultaneous functions. I dont know if this is useful, but it's fun to do.
```
import hydra, time

def _add(number):
    return number + number


def _mult(number):
    return number * number


with hydra.Hydra() as math_hydra:
    for x in range(2**16):
        math_hydra.add_work(x)
    math_hydra.do_work('adder_thread', task=_add)
    # While its working on that, lets add in some multiplication results.
    # because why not?
    math_hydra.do_work('multiplier_thread', task=_mult)
    useless_jumbled_results = math_hydra.get_results(2**16)
```
