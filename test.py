import urllib2
import demo


def test(lawyer_id):
    base_url = "https://www.avvo.com/attorneys/"
    url = base_url + str(lawyer_id) + ".html"
    request = urllib2.Request(url)
    request.add_header('User-Agent', '''Mozilla/5.0 (Windows NT 10.0; WOW64)
        AppleWebKit/537.36 (KHTML, like Gecko)
        Chrome/50.0.2661.102 Safari/537.36''')
    lawyerInfo = demo.LawyerInfo(request, lawyer_id)
    lawyer = None
    if lawyerInfo.rescode == 200:
        lawyer = lawyerInfo.parse()
        print lawyer['id'], ": ", lawyer

for i in range(0, 100):
    test(i + 1)
