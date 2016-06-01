<<<<<<< HEAD
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
=======
import urllib2
import demo
import models
import time


def test(avvo_id):
    base_url = "https://www.avvo.com/attorneys/"
    url = base_url + str(avvo_id) + ".html"
    request = urllib2.Request(url)
    request.add_header('User-Agent', '''Mozilla/5.0 (Windows NT 10.0; WOW64)
        AppleWebKit/537.36 (KHTML, like Gecko)
        Chrome/50.0.2661.102 Safari/537.36''')
    lawyer_info = demo.LawyerInfo(request, avvo_id)
    if lawyer_info.rescode == 200:
        lawyer = lawyer_info.parse()
        lawyer_db = models.conn.Lawyer(lawyer)
        lawyer_db.save()
        print lawyer['avvo_id'], " is saved"

'test(2)'
'test(688086)'
start = time.time()
for i in range(0, 100):
    test(i + 1)
end = time.time()
print end - start

'''lawyer = models.conn.Lawyer.one({'avvo_id': 2})
print lawyer'''
>>>>>>> database_dev
