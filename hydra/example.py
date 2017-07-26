import hydra
import requests
import time


def method_a():
    print('Running the slow way....')
    start = time.time()
    for x in range(25):
        requests.get('https://jsonplaceholder.typicode.com/albums', headers={'User-Agent':'py-hydra test case'})
    print('25 Consecutive calls to webpage took {} seconds.'.format(time.time()-start))

def method_b():
    print('Creating a 3 headed Hydra! Run for your lives!')
    start = time.time()
    with hydra.Hydra() as pet_hydra:
        for x in range(25):
            pet_hydra.add_work('https://jsonplaceholder.typicode.com/albums')
        pet_hydra.do_work('fibonacii_thread', requests.get, thread_number=3, headers={'User-Agent':'py-hydra test case'})
        rs = pet_hydra.get_results(25)
    print('25 calls to webpage using 3 threads took {} seconds.'.format(time.time() - start))

def method_c():
    print('Creating a Crazy 25 headed Hydra! You\'re probably already dead.')
    start = time.time()
    with hydra.Hydra() as pet_hydra:
        for x in range(25):
            pet_hydra.add_work('https://jsonplaceholder.typicode.com/albums')
        pet_hydra.do_work('blocking', thread_number=25, task=requests.get, block=True, headers={'User-Agent':'py-hydra test case'})
    print('25 calls using 25 threads to webpage took {} seconds.'.format(time.time() - start))

if __name__ == '__main__':
    print('''Gets 25 webpages of data.
First all of them in serial.
Then 3 at a time concurently.
Then all 25 at once in a blocking parallel.''')
    method_a()
    method_b()
    method_c()

