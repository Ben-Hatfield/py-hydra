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
    print('Slow function to add {} took {} seconds.'.format(numbers, time.time()-start))

def method_b():
    print('Creating a 3 headed Hydra! Run for your lives!')
    start = time.time()
    with hydra.Hydra() as pet_hydra:
        for x in range(10):
            pet_hydra.add_work((0, x))
        pet_hydra.do_work('adder_thread', _slow_add, thread_number=3)
        numbers = pet_hydra.get_results(10)
        print('slow function to add {} took {} seconds.'.format(numbers, time.time() - start))

def method_c():
    print('Creating a Crazy 10 headed Hydra! You\'re probably already dead.')
    start = time.time()
    with hydra.Hydra() as pet_hydra:
        for x in range(10):
            pet_hydra.add_work((0, x))
        pet_hydra.do_work('blocking', thread_number=10, task=_slow_add, block=True)
        numbers = pet_hydra.get_results()
        print('slow function to add {} took {} seconds.'.format(numbers, time.time() - start))

if __name__ == '__main__':
    print('''Adds 10 sets of numbers together.
First all of them in serial.
Then 3 at a time concurently.
Then all 10 at once in forced parallel.''')
    method_a()
    method_b()
    method_c()
