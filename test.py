from scheduler import Scheduler
import logging
import urllib2


def test():
    schedule_config = {
        'begin': 1,
        'thread_num': 5,
        'end': 20
    }
    logging.basicConfig(filename='spider_info.log', level=logging.DEBUG)
    sd = Scheduler(**schedule_config)
    sd.run()


def single_test(avvo_id):
    logging.basicConfig(filename='spider_info.log', level=logging.DEBUG)
    user_agent = '''Mozilla/5.0 (Windows NT 10.0; WOW64)
        AppleWebKit/537.36 (KHTML, like Gecko)
        Chrome/50.0.2661.102 Safari/537.36'''
    base_url = "https://www.avvo.com/attorneys/"
    url = base_url + str(avvo_id) + ".html"
    request = urllib2.Request(url)
    request.add_header('User-Agent', user_agent)
    from demo import LawyerInfo
    lawyer_info = LawyerInfo(request, avvo_id)
    if lawyer_info.rescode == 200:
        lawyer = lawyer_info.parse()
        logging.debug("%d is parsed" % lawyer['avvo_id'])
        '''print lawyer['id'], " is parsed"'''
        # lawyer_db = models.conn.Lawyer(lawyer)
        # lawyer_db.save()
        import models
        models.save(lawyer)


test()
# single_test(47156)
