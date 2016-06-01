from scheduler import Scheduler
import logging


def test():
    schedule_config = {
        'thread_num': 5,
        'end': 100
    }
    logging.basicConfig(filename='spider_info.log', level=logging.DEBUG)
    sd = Scheduler(**schedule_config)
    sd.run()

test()
