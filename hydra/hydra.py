import queue
import threading


class HydraThread(threading.Thread):
    """HydraThread adds the Hydra data management to threading.Thread
    Note that a HydraThread is killed by setting self.keep_alive to False from parent process/thread"""

    def __init__(self, thread_name, task, data_queue, result_queue, keep_alive=True, *args, **kwargs):
        """task is the function to perform.
        data_queue to pipe data/args in (Thread safe)
        results_queue to pipe results out (Thread safe)
        keep_alive is used to let the thread live even if the work queue is empty
        Initializing keep_alive as False will ensure the thread does at most one unit of work"""
        threading.Thread.__init__(self, name=thread_name, args=args, kwargs=kwargs)
        self.task = task
        self.data_queue = data_queue
        self.result_queue = result_queue
        self.keep_alive = keep_alive

    def run(self):
        """Emulates DO UNTIL. Starts a loop that will take one object of work and perform the task.
    Populates the results queue when the result of the task is returned.
    If an Exception occurs, it is returned to the results_queue.
    If the data_queue is empty AND keep_alive is set to False, the thread exits."""
        execute = True
        while execute is True:
            if not self.data_queue.empty():
                data = self.data_queue.get()
                try:
                    result = self.task(data)
                except Exception as e:
                    result = e
                self.result_queue.put(result)
                execute = self.keep_alive
            else:
                execute = self.keep_alive
        return


class Hydra:
    """Queued stdin/stdout Multi-Threading manager class.
    Uses Queue to get data into and out of running threads.
    thread_number sets the numbers of threads to run simultaneously."""

    def __init__(self, verbose=False):

        self.work_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.threads = {}

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        self.cleanup(wait=True)

    def add_work(self, work):
        """work is usually a tuple of args to be sent to the task.
        True can be sent if the task is meant to be a daemon that does not require arguments.
        Thread Safe"""
        self.work_queue.put(work)

    def do_work(self, thread_name, task=print, keep_alive=True, thread_number=1, block=False, *args, **kwargs):
        """Starts HydraThread(s)."""
        for n in range(thread_number):
            t_name = '{}-{}'.format(thread_name, n)
            thread = HydraThread(t_name, task, self.work_queue, self.result_queue, args=args, kwargs=kwargs, keep_alive=keep_alive)
            self.threads[t_name] = thread
            thread.start()
        if block is True:
            self.cleanup(thread_names=[thread_name], wait=True)
            # Blocks until all work is done, and therefore all results have returned
        return

    def get_result(self):
        """Returns a single result from result_queue, or None if no results have queued.
        Thread Safe"""
        if self.result_queue.qsize() != 0:
            return self.result_queue.get()
        else:
            return None

    def get_results(self, number=None, timeout=None):
        """Returns a list of all results from result_queue, or [] if no results have queued.
        This function can be safely be called if results are still being added to the queue.
        `number` is the number of results to wait for. `timeout` gets passed to queue.
        Just remember to check that you got all of the results you expected.
        Thread Safe"""
        results = []
        if number is not None:
            while len(results) != number:
                try:
                    results.append(self.result_queue.get(timeout=timeout))
                except queue.Empty:
                    return results
        else:
            while self.result_queue.qsize() != 0:
                try:
                    results.append(self.result_queue.get(timeout=timeout))
                except queue.Empty:
                    return results
        return results

    def kill_worker(self, thread_id):
        """Sets the thread.keepalive to false.
        Returns False if thread_id does not exist.
        Returns True if successful."""
        try:
            self.threads[thread_id].keep_alive = False
            return True
        except KeyError:
            print('thread_id {} does not exist')
            return False

    def cleanup(self, thread_names=[], wait=False):
        """Sets the thread_id.keep_alive to False.
        If wait is set to true, Thread.join is called for all thread_ids.
        If no thread_names are sent, all of the Hydra's threads are killed."""
        thread_ids = []
        if thread_names == []:
            for t in self.threads.keys():
                self.threads[t].keep_alive = False
                thread_ids.append(t)
        for name in thread_names:
            for t in self.threads.keys():
                if name in t:
                    self.threads[t].keep_alive = False
                    thread_ids.append(t)
        if wait is True:
            for t in thread_ids:
                if self.threads[t].is_alive():
                    self.threads[t].join()
        return thread_ids
