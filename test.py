from scheduler import Scheduler
import time


def test():
    start = time.time()
    sd = Scheduler(1, 60)
    sd.run()
    end = time.time()
    print "total: ", end - start

test()
