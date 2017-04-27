# -*- coding: utf-8 -*-
"""Hydra tries to abstract the use of multiple threads to speed up performance by running in bulk "blocking" functions.
This function is internally referred to as the task.
This is achieved by launching a Hydra class that manages the locking and unlocking of critical sections.
The "default" critical sections that are managed, is data sent to the task, and the results returned from the task.
Hydra adds a threading.Lock object and uses it throughout the HydraThreads and HydraQueues to maintain thread safety.
Additional critical data sections can be managed by making HydraQueues using the parent Hydra.

Sample applications:

# Hydra running lots of http GET requests in parallel.
import hydra, requests
url_list = ['https://github.com/Ben-Hatfield','https://docs.python.org/3/library/threading.html', ETC...]
bad_idea = hydra.Hydra()
for url in url_list:
    bad_idea.add_work(url)
bad_idea.do_parallel_work(thread_number=31337, task=requests.get)
webpages = bad_idea.get_results()

# Two separate, simultaneous threads
import hydra, time
def _add(number):
    return 0 + number
def _mult(number):
    return 1 * number
adder = hydra.Hydra()
multiplier = hydra.Hydra()
for x in range(2**16):
    adder.add_work(x)
    multiplier.add_work(x)
adder.do_work('adder_thread', task=_add)
multiplier.do_work('multiplier_thread', task=_mult)
adder.cleanup(wait=True)
multiplier.cleanup(wait=True)
useless = adder.get_results()
also_useless = multiplier.get_results()"""

from .hydra import *

__author__ = "Ben Hatfield (https://github.com/Ben-Hatfield)"
__version__ = "1.0.0"
__license__ = "GNU General Public License v3.0"
__all__ = ['Hydra', 'HydraQueue', 'HydraThread']
