from demo import LawyerInfo
import time
import urllib2
import threading
import logging
import models

USER_AGENT = '''Mozilla/5.0 (Windows NT 10.0; WOW64)
    AppleWebKit/537.36 (KHTML, like Gecko)
    Chrome/50.0.2661.102 Safari/537.36'''
BASE_URL = "https://www.avvo.com/attorneys/"


class SpiderThread(threading.Thread):
    def __init__(self, begin, thread_num, end):
        threading.Thread.__init__(self)
        self.begin = begin
        self.thread_num = thread_num
        self.end = end

    def run(self):
        '''print "Thread ", self.getName(), " begins"'''
        logging.info("Thread %s begins", self.getName())
        try:
            for i in range(self.begin, self.end + 1, self.thread_num):
                url = BASE_URL + str(i) + ".html"
                request = urllib2.Request(url)
                request.add_header('User-Agent', USER_AGENT)
                lawyer_info = LawyerInfo(request, i)
                if lawyer_info.rescode == 200:
                    lawyer = lawyer_info.parse()
                    logging.debug("%d is parsed" % lawyer['avvo_id'])
                    '''print lawyer['id'], " is parsed"'''
                    #lawyer_db = models.conn.Lawyer(lawyer)
                    #lawyer_db.save()
                    models.save(lawyer)
        except Exception as e:
            '''print "Thread ", self.getName(), " is terminated due to ", e.message'''
            logging.error("Thread %s is terminated due to %s, url: %s" % (self.getName(), e.message, url))
        else:
            logging.debug("Thread %s ends" % self.getName())
            '''print "Thread ", self.getName(), " ends"'''


class Scheduler:
    def __init__(self, thread_num=2, end=100, begin=0, *arguments, **keywords):
        self.begin = begin
        self.thread_num = thread_num
        self.end = end

    def run(self):
        threads = []
        for i in range(0, self.thread_num):
            threads.append(SpiderThread(self.begin + i + 1, self.thread_num, self.end))

        start = time.time()
        for ts in threads:
            ts.start()

        for ts in threads:
            ts.join()
        end = time.time()
        print "total time: ", end - start
        logging.info("total time: %d" % (end - start))
