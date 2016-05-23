from scheduler import Scheduler


def test():
    schedule_config = {
        'thread_num': 3,
        'end': 100
    }
    sd = Scheduler(**schedule_config)
    sd.run()

test()
