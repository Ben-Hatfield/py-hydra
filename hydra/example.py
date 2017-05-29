import hydra
import time


def _slow_add(args_object):
        a, b = args_object
        time.sleep(0.3)
        return a + b

def method_a():
    print('Running the slow way....')
    start = time.time()
    numbers = []
    for x in range(10):
        args_object = (0, x)
        numbers.append(_slow_add(args_object))
    print('Slow adding {} took {} seconds.'.format(numbers, time.time()-start))

def method_b():
    print('Creating a 3 headed Hydra! Run for your lives!')
    start = time.time()
    pet_hydra = hydra.Hydra()
    for x in range(10):
        pet_hydra.add_work((0, x))
    pet_hydra.do_work('adder_thread-1', _slow_add)
    pet_hydra.do_work('adder_thread-2', _slow_add)
    pet_hydra.do_work('adder_thread-3', _slow_add)
    numbers = []
    while len(numbers) != 10:
        [numbers.append(x) for x in pet_hydra.get_results()]
    print('slow adding {} took {} seconds.'.format(numbers, time.time() - start))
    pet_hydra.cleanup()

def method_c():
    print('Creating a Crazy 10 headed Hydra! You\'re probably already dead.')
    start = time.time()
    pet_hydra = hydra.Hydra()
    for x in range(10):
        pet_hydra.add_work((0, x))
    pet_hydra.do_parallel_work(thread_number=10, task=_slow_add)
    numbers = pet_hydra.get_results()
    print('slow adding {} took {} seconds.'.format(numbers, time.time() - start))
    pet_hydra.cleanup()

if __name__ == '__main__':
    print('''Adds 10 sets of numbers together.
First all in serial,
then 3 concurently,
then all 10 concurently.''')
    method_a()
    method_b()
    method_c()
