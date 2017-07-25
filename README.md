# py-hydra
Python Multi-Threading Manager

Hydra tries to abstract the setup of a common use of multiple threads, to reduce time spent waiting for blocking calls.

This blocking function is internally referred to by hydra as the `task`.

This abstraction is achieved by launching a Hydra class that manages the locking and unlocking of critical sections.

The "default" critical sections that are managed are: data sent to the task; and results returned from the task.

Hydra adds a threading.Lock object and uses it throughout the HydraThreads and HydraQueues to maintain thread safety.

Additional critical data sections can be managed by making HydraQueues using the parent Hydra.

```
# Time consuming function
def f(args):
    a,b = args
    time.sleep(10)
    x = a + b
    return x

# Hydra class init and execution
data = [(0,0), (0,1), (0,2)]
with hydra.Hydra() as fast:
    for args in data:
        fast.add_work(args)
    fast.do_work('thread_id_root',f,threads=2)
    results = fast.get_results(3)

INPUT QUEUE   TASK  FUNCTION   OUPUT QUEUE
##########  | ############## | ###########
# args   #  | args-> f(args) | #    x    #
# args   #  | args-> f(args) | #    x    #
# args   #  |                | #    x    #
##########  | #############  | ###########

# 0 three args put into input queue;
# 1 two threads running the 'f' task collect waiting args;
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
    bad_idea.do_parallel_work(thread_number=31337, task=requests.get)
    webpages = bad_idea.get_results()
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
