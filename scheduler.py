from demo import LawyerInfo
import time
import urllib2


class Scheduler:
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end
        self.base_url = "https://www.avvo.com/attorneys/"

    def run(self):
        for i in range(self.begin, self.end + 1):
            url = self.base_url + str(i) + ".html"
            request = urllib2.Request(url)
            request.add_header('User-Agent', '''Mozilla/5.0 (Windows NT 10.0; WOW64)
                    AppleWebKit/537.36 (KHTML, like Gecko)
                    Chrome/50.0.2661.102 Safari/537.36''')
            start = time.time()
            LawyerInfo(request, i).parse()
            end = time.time()
            print end - start
